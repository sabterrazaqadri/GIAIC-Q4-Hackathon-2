import { useState, useCallback, useRef, useEffect } from 'react';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001';

export const useChat = (onTasksUpdate) => {
  const [messages, setMessages] = useState([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI-powered Todo Assistant. You can ask me to add, update, delete, or list your tasks. What would you like to do?',
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const sendMessage = useCallback(
    async (userMessage) => {
      if (!userMessage.trim()) return;

      // Add user message to chat
      const userMsg = {
        id: Date.now().toString(),
        role: 'user',
        content: userMessage,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, userMsg]);
      setIsLoading(true);
      setError(null);

      try {
        // Send to backend /chat endpoint
        const response = await fetch(`${BACKEND_URL}/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userMessage }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Parse response
        const assistantContent = data.message || 'I processed your request.';

        // Add assistant message
        const assistantMsg = {
          id: `assistant-${Date.now()}`,
          role: 'assistant',
          content: assistantContent,
          timestamp: new Date(),
          action: data.data?.action,
        };

        setMessages(prev => [...prev, assistantMsg]);

        // Trigger task update with delay to allow backend to process
        if (onTasksUpdate) {
          setTimeout(() => {
            onTasksUpdate();
          }, 500);
        }
      } catch (err) {
        console.error('Chat error:', err);
        setError(err.message);

        // Add error message
        const errorMsg = {
          id: `error-${Date.now()}`,
          role: 'assistant',
          content: `Sorry, I encountered an error: ${err.message}. Please try again.`,
          timestamp: new Date(),
          isError: true,
        };

        setMessages(prev => [...prev, errorMsg]);
      } finally {
        setIsLoading(false);
      }
    },
    [onTasksUpdate]
  );

  const clearMessages = useCallback(() => {
    setMessages([
      {
        id: '1',
        role: 'assistant',
        content: 'Chat cleared. How can I help you with your tasks?',
        timestamp: new Date(),
      },
    ]);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
    messagesEndRef,
  };
};
