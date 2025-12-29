'use client';

import { useState, useEffect } from 'react';
import TodoForm from '@/components/TodoForm';
import TodoList from '@/components/TodoList';
import { Todo, CreateTodoData } from '@/types/todo';
import { fetchTodos, createTodo } from '@/services/api';

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadTodos = async () => {
    try {
      const data = await fetchTodos();
      setTodos(data);
      setError(null);
    } catch (err) {
      setError('Failed to load todos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTodos();
  }, []);

  const handleCreateTodo = async (todoData: CreateTodoData) => {
    try {
      const newTodo = await createTodo(todoData);
      setTodos([newTodo, ...todos]);
    } catch (err) {
      setError('Failed to create todo');
      console.error(err);
    }
  };

  return (
    <main className="min-h-screen p-8 max-w-4xl mx-auto">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">Todo App</h1>
        <p className="text-gray-600">Manage your tasks with ease</p>
      </header>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="space-y-8">
        <TodoForm onCreate={handleCreateTodo} />

        <section>
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">Your Todos</h2>
          {loading ? (
            <div className="text-center py-8 text-gray-500">Loading...</div>
          ) : todos.length === 0 ? (
            <div className="text-center py-8 text-gray-500 bg-gray-50 rounded-lg">
              No todos yet. Create your first todo above!
            </div>
          ) : (
            <TodoList todos={todos} onUpdate={loadTodos} />
          )}
        </section>
      </div>
    </main>
  );
}
