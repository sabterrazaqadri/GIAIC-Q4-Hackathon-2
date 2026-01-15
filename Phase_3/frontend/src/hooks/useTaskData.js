import { useState, useEffect, useCallback } from 'react';

// Use Phase 3 backend as proxy to Phase 2 API (handles CORS)
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001';

// Fetch tasks from Phase 2 API (via Phase 3 proxy)
const fetchTasksFromPhase2 = async () => {
  try {
    console.log('🔄 Fetching tasks from:', `${BACKEND_URL}/todos`);
    const response = await fetch(`${BACKEND_URL}/todos`);
    console.log('📡 Response status:', response.status, response.ok);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('📦 Raw data received:', data);

    // Handle different response formats from Phase 2 API
    let tasks = Array.isArray(data) ? data : data.todos || data.data || [];
    console.log('📝 Tasks after parsing:', tasks.length, 'tasks');

    // Transform Phase 2 data to our format
    tasks = tasks.map(task => ({
      id: String(task.id || task._id),
      title: task.title || 'Untitled',
      description: task.description || '',
      status: task.is_complete ? 'completed' : 'pending',
      is_complete: task.is_complete || false,
      priority: task.priority || 'medium',
      created_at: task.created_at || new Date().toISOString(),
      updated_at: task.updated_at || new Date().toISOString(),
    }));

    console.log('✅ Tasks transformed:', tasks);
    return tasks;
  } catch (err) {
    console.error('❌ Error fetching from Phase 2:', err);
    return [];
  }
};

// Mark task as complete in Phase 2 API (via Phase 3 proxy)
const updateTaskInPhase2 = async (taskId, updates) => {
  try {
    const response = await fetch(`${BACKEND_URL}/todos/${taskId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (err) {
    console.error('Error updating task in Phase 2:', err);
    throw err;
  }
};

// Delete task from Phase 2 API (via Phase 3 proxy)
const deleteTaskFromPhase2 = async (taskId) => {
  try {
    const response = await fetch(`${BACKEND_URL}/todos/${taskId}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok && response.status !== 204) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return true;
  } catch (err) {
    console.error('Error deleting task from Phase 2:', err);
    throw err;
  }
};

export const useTaskData = (pollingInterval = 500) => {
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTasks = useCallback(async () => {
    try {
      console.log('🚀 fetchTasks called');
      setIsLoading(true);
      const fetchedTasks = await fetchTasksFromPhase2();
      console.log('📊 Setting tasks:', fetchedTasks.length, fetchedTasks);
      setTasks(fetchedTasks);
      setError(null);
    } catch (err) {
      console.error('❌ Error in fetchTasks:', err);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Fetch tasks on mount
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Set up polling for real-time updates
  useEffect(() => {
    const interval = setInterval(fetchTasks, pollingInterval);
    return () => clearInterval(interval);
  }, [fetchTasks, pollingInterval]);

  const refreshTasks = useCallback(async () => {
    await fetchTasks();
  }, [fetchTasks]);

  const completeTask = useCallback(async (taskId) => {
    try {
      // Optimistic update
      setTasks(prev =>
        prev.map(task =>
          task.id === taskId
            ? { ...task, status: 'completed', is_complete: true }
            : task
        )
      );

      // Update in backend
      await updateTaskInPhase2(taskId, { is_complete: true });

      // Refresh to ensure sync
      setTimeout(() => fetchTasks(), 500);
    } catch (err) {
      console.error('Error completing task:', err);
      // Revert optimistic update
      await fetchTasks();
    }
  }, [fetchTasks]);

  const uncompleteTask = useCallback(async (taskId) => {
    try {
      // Optimistic update
      setTasks(prev =>
        prev.map(task =>
          task.id === taskId
            ? { ...task, status: 'pending', is_complete: false }
            : task
        )
      );

      // Update in backend
      await updateTaskInPhase2(taskId, { is_complete: false });

      // Refresh to ensure sync
      setTimeout(() => fetchTasks(), 500);
    } catch (err) {
      console.error('Error uncompleting task:', err);
      // Revert optimistic update
      await fetchTasks();
    }
  }, [fetchTasks]);

  const deleteTask = useCallback(async (taskId) => {
    try {
      // Optimistic update
      setTasks(prev => prev.filter(task => task.id !== taskId));

      // Delete from backend
      await deleteTaskFromPhase2(taskId);

      // Refresh to ensure sync
      setTimeout(() => fetchTasks(), 500);
    } catch (err) {
      console.error('Error deleting task:', err);
      // Revert optimistic update
      await fetchTasks();
    }
  }, [fetchTasks]);

  const updateTask = useCallback(async (taskId, updates) => {
    try {
      // Optimistic update
      setTasks(prev =>
        prev.map(task =>
          task.id === taskId
            ? {
                ...task,
                ...updates,
                updated_at: new Date().toISOString(),
              }
            : task
        )
      );

      // Update in backend
      await updateTaskInPhase2(taskId, updates);

      // Refresh to ensure sync
      setTimeout(() => fetchTasks(), 500);
    } catch (err) {
      console.error('Error updating task:', err);
      // Revert optimistic update
      await fetchTasks();
    }
  }, [fetchTasks]);

  const addTask = useCallback((task) => {
    const newTask = {
      id: String(Date.now()),
      ...task,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      status: task.status || 'pending',
      is_complete: false,
    };
    setTasks(prev => [newTask, ...prev]);
    return newTask;
  }, []);

  return {
    tasks,
    isLoading,
    error,
    refreshTasks,
    addTask,
    updateTask,
    deleteTask,
    completeTask,
    uncompleteTask,
  };
};
