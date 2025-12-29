'use client';

import { useState } from 'react';
import { Todo, UpdateTodoData } from '@/types/todo';
import { completeTodo, reopenTodo, deleteTodo, patchTodo } from '@/services/api';
import EditTodoForm from './EditTodoForm';

interface TodoItemProps {
  todo: Todo;
  onUpdate: () => Promise<void>;
}

export default function TodoItem({ todo, onUpdate }: TodoItemProps) {
  const [loading, setLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  const handleToggleComplete = async () => {
    setLoading(true);
    try {
      if (todo.is_complete) {
        await reopenTodo(todo.id);
      } else {
        await completeTodo(todo.id);
      }
      await onUpdate();
    } catch (error) {
      console.error('Failed to toggle todo:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this todo?')) {
      return;
    }

    setLoading(true);
    try {
      await deleteTodo(todo.id);
      await onUpdate();
    } catch (error) {
      console.error('Failed to delete todo:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEdit = async (id: number, data: UpdateTodoData) => {
    setLoading(true);
    try {
      await patchTodo(id, data);
      setIsEditing(false);
      await onUpdate();
    } catch (error) {
      console.error('Failed to update todo:', error);
    } finally {
      setLoading(false);
    }
  };

  const priorityColors = {
    low: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-red-100 text-red-800',
  };

  if (isEditing) {
    return (
      <EditTodoForm
        todo={todo}
        onCancel={() => setIsEditing(false)}
        onSave={handleSaveEdit}
      />
    );
  }

  return (
    <div
      className={`bg-white p-4 rounded-lg shadow-sm border-l-4 transition-all ${
        todo.is_complete
          ? 'border-gray-300 opacity-60'
          : 'border-primary-500'
      }`}
    >
      <div className="flex items-start gap-4">
        <button
          onClick={handleToggleComplete}
          disabled={loading}
          className={`mt-1 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
            todo.is_complete
              ? 'bg-primary-600 border-primary-600 text-white'
              : 'border-gray-300 hover:border-primary-500'
          }`}
        >
          {todo.is_complete && (
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
          )}
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <h3
              className={`text-lg font-medium ${
                todo.is_complete ? 'line-through text-gray-500' : 'text-gray-800'
              }`}
            >
              {todo.title}
            </h3>
            <span
              className={`px-2 py-0.5 text-xs font-medium rounded-full capitalize ${priorityColors[todo.priority]}`}
            >
              {todo.priority}
            </span>
          </div>

          {todo.description && (
            <p
              className={`text-sm ${
                todo.is_complete ? 'text-gray-400 line-through' : 'text-gray-600'
              }`}
            >
              {todo.description}
            </p>
          )}

          <p className="text-xs text-gray-400 mt-2">
            Created: {new Date(todo.created_at).toLocaleDateString()}
          </p>
        </div>

        <div className="flex gap-1">
          <button
            onClick={() => setIsEditing(true)}
            disabled={loading}
            className="text-gray-400 hover:text-primary-600 transition-colors p-1"
            title="Edit todo"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>
          <button
            onClick={handleDelete}
            disabled={loading}
            className="text-gray-400 hover:text-red-600 transition-colors p-1"
            title="Delete todo"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
