"""Intent classification for the conversational todo management system."""

import re
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel
from models.chat import IntentClassification, IntentType
from utils.logging_config import logger
import uuid


class IntentMatchRule(BaseModel):
    """Rule for matching an intent based on patterns and keywords."""
    intent_type: IntentType
    patterns: List[str]  # Regular expressions
    keywords: List[str]  # Keywords that suggest this intent
    confidence_boost_keywords: List[str]  # Keywords that boost confidence


class IntentClassifier:
    """Classifies user intents in the conversational todo system."""

    def __init__(self):
        self.rules = self._initialize_rules()

    def _initialize_rules(self) -> List[IntentMatchRule]:
        """Initialize the intent matching rules."""
        rules = [
            # DELETE_TASK - Check this first to avoid conflicts with add/update patterns
            IntentMatchRule(
                intent_type=IntentType.DELETE_TASK,
                patterns=[
                    r'delete\s+(.+)',
                    r'remove\s+(.+)',
                    r'cancel\s+(.+)',
                    r'eliminate\s+(.+)',
                    r'get\s+rid\s+of\s+(.+)',
                    r'forget\s+about\s+(.+)',
                ],
                keywords=[
                    'delete', 'remove', 'cancel', 'eliminate', 'forget', 'rid', 'done with', 'finished with'
                ],
                confidence_boost_keywords=[
                    'delete', 'remove', 'done with', 'finished with', 'cancel'
                ]
            ),
            # UPDATE_TASK - Check before ADD to avoid conflicts
            IntentMatchRule(
                intent_type=IntentType.UPDATE_TASK,
                patterns=[
                    r'update\s+(.+)',
                    r'change\s+(.+)',
                    r'modify\s+(.+)',
                    r'edit\s+(.+)',
                    r'mark\s+(.+?)\s+as\s+(.+)',
                    r'set\s+(.+?)\s+to\s+(.+)',
                ],
                keywords=[
                    'update', 'change', 'modify', 'edit', 'mark', 'set', 'status', 'complete', 'done', 'finished'
                ],
                confidence_boost_keywords=[
                    'complete', 'done', 'finished', 'pending', 'in progress', 'started', 'update', 'change'
                ]
            ),
            IntentMatchRule(
                intent_type=IntentType.ADD_TASK,
                patterns=[
                    r'add\s+(a\s+|an\s+|the\s+)?(.+?)(\s+to\s+(my\s+)?(list|todo|tasks?))?$',
                    r'create\s+(a\s+|an\s+|the\s+)?(.+)$',
                    r'make\s+(a\s+|an\s+|the\s+)?(.+)$',
                    r'new\s+(task|todo)\s*:\s*(.+)$',
                    r'i\s+need\s+to\s+(.+)$',
                    r'don\'t\s+forget\s+to\s+(.+)$',
                    r'remind\s+me\s+to\s+(.+)$',
                    r'^buy\s+(.+)$',  # Only match at start of string for shopping tasks
                    r'^get\s+(.+)$',  # Only match at start of string for shopping tasks
                ],
                keywords=[
                    'add', 'create', 'make', 'new', 'need', 'remember', 'remind', 'buy', 'get', 'don\'t forget'
                ],
                confidence_boost_keywords=[
                    'task', 'todo', 'list', 'shopping', 'buy', 'purchase', 'get', 'do', 'complete'
                ]
            ),
            IntentMatchRule(
                intent_type=IntentType.LIST_TASKS,
                patterns=[
                    r'(show|list|display|what.*have|what.*got|what.*to)\s+(.+)?(tasks?|todos?|list|items?)',
                    r'what\s+(is\s+|are\s+)?(on\s+)?(my\s+)?(todo\s+)?(list|tasks?)',
                    r'do\s+i\s+have\s+(any\s+)?(tasks?|todos?)',
                    r'what\s+(should\s+i|can\s+i|do\s+i)\s+(do|work\s+on|focus\s+on)',
                    r'help\s+me\s+organize',
                    r'what\'?s\s+(next|up)',
                ],
                keywords=[
                    'show', 'list', 'display', 'what', 'have', 'got', 'todo', 'tasks', 'list', 'items',
                    'organize', 'next', 'up', 'help'
                ],
                confidence_boost_keywords=[
                    'show me', 'what are', 'what is', 'list my', 'show my', 'what\'s next', 'what\'s up'
                ]
            )
        ]
        return rules

    def classify_intent(self, user_input: str) -> IntentClassification:
        """
        Classifies the intent from user input.

        Args:
            user_input: The raw user input string

        Returns:
            IntentClassification object with the determined intent
        """
        original_text = user_input.strip()
        if not original_text:
            return IntentClassification(
                id=str(uuid.uuid4()),
                type=IntentType.UNKNOWN,
                parameters={},
                confidence=0.0,
                originalText=original_text
            )

        # Normalize the input
        normalized_input = original_text.lower().strip()

        best_match = None
        best_confidence = 0.0

        # Check for direct pattern matches first
        for rule in self.rules:
            for pattern in rule.patterns:
                match = re.search(pattern, normalized_input)
                if match:
                    # Calculate confidence based on pattern match
                    confidence = 0.9  # High confidence for pattern match
                    if self._has_confidence_boost(normalized_input, rule.confidence_boost_keywords):
                        confidence = 0.95  # Very high confidence

                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = self._create_intent_classification(
                            rule.intent_type,
                            original_text,
                            confidence,
                            match
                        )

        # If no pattern matched, use keyword-based classification
        if best_match is None:
            for rule in self.rules:
                keyword_count = self._count_keywords(normalized_input, rule.keywords)
                if keyword_count > 0:
                    # Calculate confidence based on keyword matches
                    confidence = min(0.8, 0.3 + (keyword_count * 0.1))  # Base 0.3 + 0.1 per keyword
                    if self._has_confidence_boost(normalized_input, rule.confidence_boost_keywords):
                        confidence += 0.15  # Boost for confidence keywords

                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = self._create_intent_classification(
                            rule.intent_type,
                            original_text,
                            confidence
                        )

        # If still no match, return unknown
        if best_match is None:
            best_match = IntentClassification(
                id=str(uuid.uuid4()),
                type=IntentType.UNKNOWN,
                parameters={},
                confidence=0.0,
                originalText=original_text
            )

        logger.info(f"Classified intent: {best_match.type.value} with confidence {best_match.confidence} for input: {original_text}")
        return best_match

    def _has_confidence_boost(self, text: str, boost_keywords: List[str]) -> bool:
        """Check if the text contains any confidence boost keywords."""
        text_lower = text.lower()
        for keyword in boost_keywords:
            if keyword.lower() in text_lower:
                return True
        return False

    def _count_keywords(self, text: str, keywords: List[str]) -> int:
        """Count how many keywords from the list appear in the text."""
        text_lower = text.lower()
        count = 0
        for keyword in keywords:
            if keyword.lower() in text_lower:
                count += 1
        return count

    def _create_intent_classification(self, intent_type: IntentType, original_text: str,
                                    confidence: float, match: Optional[re.Match] = None) -> IntentClassification:
        """Create an IntentClassification object."""
        parameters = {}

        # Extract parameters based on match groups if available
        if match and match.groups():
            # For ADD_TASK, try to extract the task title/description
            if intent_type == IntentType.ADD_TASK:
                # Look for the main content of the task
                for group in match.groups():
                    if group and group.strip() and not group.strip() in ['a ', 'an ', 'the ', 'my ', 'to ', 'on ']:
                        parameters['title'] = group.strip()
                        break

        return IntentClassification(
            id=str(uuid.uuid4()),
            type=intent_type,
            parameters=parameters,
            confidence=confidence,
            originalText=original_text
        )


# Initialize the intent classifier
intent_classifier = IntentClassifier()


def classify_intent(user_input: str) -> IntentClassification:
    """Convenience function to classify intent."""
    return intent_classifier.classify_intent(user_input)


# Urdu language processing support
class UrduIntentClassifier:
    """Classifies intents in Urdu language."""

    def __init__(self):
        self.urdu_rules = self._initialize_urdu_rules()

    def _initialize_urdu_rules(self):
        """Initialize Urdu intent matching rules."""
        # Urdu keywords and patterns for each intent type
        rules = {
            IntentType.ADD_TASK: [
                "شامل کریں",  # add
                "نیا",        # new
                "نیا کام",    # new task
                "کام بنائیں", # create task
                "کام شامل کریں", # add task
                "یاد دہانی",  # reminder
                "یاد رکھیں",  # remember
                "خیال رکھیں", # take care (as in remember to do)
            ],
            IntentType.UPDATE_TASK: [
                "تبدیل کریں",  # update
                "تبدیلی",      # change
                "_UPDATED_",   # placeholder for update patterns
                "مکمل",       # complete
                "ہو گیا",     # done
                "کر دیا",     # completed/done
                "کام مکمل",   # task complete
            ],
            IntentType.DELETE_TASK: [
                "حذف کریں",   # delete
                "ہٹا دیں",    # remove
                "ختم",       # remove/end
                "کام حذف",   # delete task
                "کام ختم",   # end task
            ],
            IntentType.LIST_TASKS: [
                "دکھائیں",   # show
                "فہرست",     # list
                "کیا ہے",    # what is
                "دیکھیں",    # see
                "کام دکھائیں", # show tasks
                "میرے کام",   # my tasks
                "کام کیا ہیں", # what tasks
                "کاموں کی فہرست", # list of tasks
            ]
        }
        return rules

    def classify_urdu_intent(self, user_input: str) -> IntentClassification:
        """Classifies intent for Urdu input."""
        original_text = user_input.strip()
        if not original_text:
            return IntentClassification(
                id=str(uuid.uuid4()),
                type=IntentType.UNKNOWN,
                parameters={},
                confidence=0.0,
                originalText=original_text
            )

        # Check for Urdu keywords in the input
        best_match = IntentType.UNKNOWN
        best_confidence = 0.0

        for intent_type, keywords in self.urdu_rules.items():
            for keyword in keywords:
                if keyword in user_input:
                    # Simple keyword matching for Urdu
                    confidence = 0.7  # Base confidence for Urdu keyword match
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = intent_type

        # If no Urdu keywords found, try to extract meaning using common Urdu task patterns
        if best_match == IntentType.UNKNOWN:
            # Check for common Urdu patterns
            if any(pattern in user_input for pattern in ["کام یاد", "کام یاد دہانی", "کرنا ہے"]):
                best_match = IntentType.ADD_TASK
                best_confidence = 0.6
            elif any(pattern in user_input for pattern in ["کام مکمل", "کام ہو گیا", "ہو گیا"]):
                best_match = IntentType.UPDATE_TASK
                best_confidence = 0.6
            elif any(pattern in user_input for pattern in ["کام حذف", "کام ہٹا دیں"]):
                best_match = IntentType.DELETE_TASK
                best_confidence = 0.6
            elif any(pattern in user_input for pattern in ["کام دکھائیں", "میرے کام", "کام کی فہرست"]):
                best_match = IntentType.LIST_TASKS
                best_confidence = 0.6

        # If still no match, return unknown
        return IntentClassification(
            id=str(uuid.uuid4()),
            type=best_match,
            parameters={},
            confidence=best_confidence,
            originalText=original_text
        )


class UrduToEnglishTranslator:
    """Simple translation/detection for Urdu commands to English for processing."""

    def __init__(self):
        # Urdu to English mappings for common commands
        self.urdu_to_english_map = {
            # Add task commands
            "کام شامل کریں": "add task",
            "نیا کام": "new task",
            "کام بنائیں": "create task",
            "یاد دہانی": "reminder",
            "یاد رکھیں": "remember",

            # Update task commands
            "کام تبدیل کریں": "update task",
            "کام مکمل": "complete task",
            "کام ہو گیا": "task done",

            # Delete task commands
            "کام حذف کریں": "delete task",
            "کام ہٹا دیں": "remove task",

            # List task commands
            "کام دکھائیں": "show tasks",
            "میرے کام": "my tasks",
            "کاموں کی فہرست": "list tasks",
        }

    def translate_if_urdu(self, user_input: str) -> tuple[str, bool]:
        """
        Translates Urdu input to English if detected, otherwise returns original.

        Returns:
            tuple: (translated_text, is_urdu)
        """
        # Check if the input contains Urdu characters (Unicode range for Arabic/Persian script used in Urdu)
        contains_urdu = bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]', user_input))

        if contains_urdu:
            # For this implementation, we'll return the original input and let the Urdu classifier handle it
            # A more advanced implementation would translate to English
            return user_input, True

        return user_input, False


# Initialize Urdu intent classifier
urdu_intent_classifier = UrduIntentClassifier()


def classify_urdu_intent(user_input: str) -> IntentClassification:
    """Convenience function to classify Urdu intent."""
    return urdu_intent_classifier.classify_urdu_intent(user_input)