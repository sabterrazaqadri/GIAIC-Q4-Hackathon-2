export const filterTasks = (tasks, filters = {}) => {
  let filtered = [...(tasks || [])];

  if (filters.status) {
    filtered = filtered.filter(task => task.status === filters.status);
  }

  if (filters.priority) {
    filtered = filtered.filter(task => task.priority === filters.priority);
  }

  if (filters.search) {
    const searchTerm = filters.search.toLowerCase();
    filtered = filtered.filter(task =>
      task.title?.toLowerCase().includes(searchTerm) ||
      task.description?.toLowerCase().includes(searchTerm)
    );
  }

  return filtered;
};

export const sortTasks = (tasks, sortBy = 'created') => {
  const sorted = [...tasks];

  switch (sortBy) {
    case 'title':
      sorted.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
      break;
    case 'priority':
      const priorityOrder = { high: 0, medium: 1, low: 2 };
      sorted.sort((a, b) => (priorityOrder[a.priority] || 3) - (priorityOrder[b.priority] || 3));
      break;
    case 'status':
      sorted.sort((a, b) => {
        const statusOrder = { pending: 0, 'in-progress': 1, completed: 2 };
        return (statusOrder[a.status] || 3) - (statusOrder[b.status] || 3);
      });
      break;
    case 'created':
    default:
      sorted.sort((a, b) => new Date(b.createdAt || 0) - new Date(a.createdAt || 0));
  }

  return sorted;
};

export const calculateTaskStats = (tasks = []) => {
  console.log('📊 calculateTaskStats called with tasks:', tasks);
  const total = tasks.length;
  const completed = tasks.filter(t => t.status === 'completed' || t.is_complete).length;
  const pending = tasks.filter(t => t.status === 'pending' || !t.is_complete).length;
  const highPriority = tasks.filter(t => t.priority === 'high').length;

  const stats = {
    total,
    completed,
    pending,
    highPriority,
    completionPercentage: total > 0 ? Math.round((completed / total) * 100) : 0,
  };

  console.log('📈 Stats calculated:', stats);
  return stats;
};

export const groupTasksByStatus = (tasks = []) => {
  const grouped = {
    pending: [],
    'in-progress': [],
    completed: [],
  };

  tasks.forEach(task => {
    const status = task.status || (task.is_complete ? 'completed' : 'pending');
    if (grouped[status]) {
      grouped[status].push(task);
    }
  });

  return grouped;
};

export const getPriorityColor = (priority) => {
  switch (priority?.toLowerCase()) {
    case 'high':
      return { bg: 'bg-red-500/20', text: 'text-red-300', border: 'border-red-500/30' };
    case 'medium':
      return { bg: 'bg-yellow-500/20', text: 'text-yellow-300', border: 'border-yellow-500/30' };
    case 'low':
      return { bg: 'bg-green-500/20', text: 'text-green-300', border: 'border-green-500/30' };
    default:
      return { bg: 'bg-blue-500/20', text: 'text-blue-300', border: 'border-blue-500/30' };
  }
};

export const getStatusColor = (status) => {
  switch (status?.toLowerCase()) {
    case 'completed':
      return { bg: 'bg-green-500/20', text: 'text-green-300', border: 'border-green-500/30' };
    case 'pending':
      return { bg: 'bg-yellow-500/20', text: 'text-yellow-300', border: 'border-yellow-500/30' };
    case 'in-progress':
      return { bg: 'bg-blue-500/20', text: 'text-blue-300', border: 'border-blue-500/30' };
    default:
      return { bg: 'bg-slate-500/20', text: 'text-slate-300', border: 'border-slate-500/30' };
  }
};
