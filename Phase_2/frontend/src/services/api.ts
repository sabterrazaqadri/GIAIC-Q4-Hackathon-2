import axios from 'axios';
import { Todo, CreateTodoData, UpdateTodoData } from '@/types/todo';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function fetchTodos(): Promise<Todo[]> {
  const response = await api.get('/todos');
  return response.data;
}

export async function createTodo(data: CreateTodoData): Promise<Todo> {
  const response = await api.post('/todos', data);
  return response.data;
}

export async function updateTodo(id: number, data: UpdateTodoData): Promise<Todo> {
  const response = await api.put(`/todos/${id}`, data);
  return response.data;
}

export async function patchTodo(id: number, data: UpdateTodoData): Promise<Todo> {
  const response = await api.patch(`/todos/${id}`, data);
  return response.data;
}

export async function completeTodo(id: number): Promise<Todo> {
  const response = await api.patch(`/todos/${id}/complete`);
  return response.data;
}

export async function reopenTodo(id: number): Promise<Todo> {
  const response = await api.patch(`/todos/${id}/incomplete`);
  return response.data;
}

export async function deleteTodo(id: number): Promise<void> {
  await api.delete(`/todos/${id}`);
}
