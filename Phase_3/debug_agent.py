#!/usr/bin/env python3
"""
Debug script to test the agent functions directly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend", "src"))

from intelligence.agent import TodoAgent, list_tasks_skill, delete_task_skill

def test_functions():
    print("=== Testing Agent Functions Directly ===")

    # Test listing tasks
    print("\n1. Testing list_tasks_skill directly:")
    try:
        tasks = list_tasks_skill()
        print(f"   Found {len(tasks)} tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"   {i}. ID: {task.get('id')} - Title: {task.get('title')}")
    except Exception as e:
        print(f"   Error listing tasks: {e}")

    # Test deleting a specific task by name
    print("\n2. Testing delete_task function manually:")
    try:
        # First list tasks to find a target
        tasks = list_tasks_skill()
        target_task = None

        for task in tasks:
            if 'milk' in task.get('title', '').lower():
                target_task = task
                break

        if target_task:
            print(f"   Found target task: {target_task.get('title')} with ID: {target_task.get('id')}")

            # Now try to delete it
            result = delete_task_skill(id=target_task.get('id'))
            print(f"   Delete result: {result}")
        else:
            print("   No task with 'milk' in the title found")
    except Exception as e:
        print(f"   Error in manual test: {e}")

if __name__ == "__main__":
    test_functions()