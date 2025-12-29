export type TodoPriority = 'low' | 'medium' | 'high';

export interface Todo {
  id: number;
  title: string;
  description: string | null;
  priority: TodoPriority;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTodoData {
  title: string;
  description?: string;
  priority: TodoPriority;
}

export interface UpdateTodoData {
  title?: string;
  description?: string;
  priority?: TodoPriority;
  is_complete?: boolean;
}
