import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Filter } from 'lucide-react';
import { TaskCard } from './TaskCard';
import { filterTasks, sortTasks } from '../../utils/taskHelpers';
import { useDebounce } from '../../hooks/useDebounce';

export const TaskBoard = ({ tasks = [], onTaskAction }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [sortBy, setSortBy] = useState('created');

  const debouncedSearch = useDebounce(searchTerm, 300);

  // Filter and sort tasks
  const filteredTasks = useMemo(() => {
    let result = tasks;

    // Apply filters
    if (statusFilter !== 'all') {
      result = result.filter(t => (t.status || (t.is_complete ? 'completed' : 'pending')) === statusFilter);
    }

    if (priorityFilter !== 'all') {
      result = result.filter(t => t.priority === priorityFilter);
    }

    if (debouncedSearch) {
      const searchLower = debouncedSearch.toLowerCase();
      result = result.filter(
        t =>
          t.title?.toLowerCase().includes(searchLower) ||
          t.description?.toLowerCase().includes(searchLower)
      );
    }

    // Sort tasks
    return sortTasks(result, sortBy);
  }, [tasks, statusFilter, priorityFilter, debouncedSearch, sortBy]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-2xl md:text-3xl font-bold text-white mb-2">
          Your Tasks
        </h2>
        <p className="text-slate-300">
          {filteredTasks.length} of {tasks.length} tasks
        </p>
      </motion.div>

      {/* Controls */}
      <div className="space-y-4 md:space-y-0 md:flex gap-4">
        {/* Search */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex-1 relative"
        >
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
          <input
            type="text"
            placeholder="Search tasks..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="input-field pl-10 w-full"
          />
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="flex gap-2 flex-wrap md:flex-nowrap"
        >
          <select
            value={statusFilter}
            onChange={e => setStatusFilter(e.target.value)}
            className="input-field text-sm"
          >
            <option value="all">All Status</option>
            <option value="pending">Pending</option>
            <option value="in-progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>

          <select
            value={priorityFilter}
            onChange={e => setPriorityFilter(e.target.value)}
            className="input-field text-sm"
          >
            <option value="all">All Priority</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          <select
            value={sortBy}
            onChange={e => setSortBy(e.target.value)}
            className="input-field text-sm"
          >
            <option value="created">Newest</option>
            <option value="title">Title A-Z</option>
            <option value="priority">Priority</option>
            <option value="status">Status</option>
          </select>
        </motion.div>
      </div>

      {/* Task List */}
      <div className="space-y-3">
        <AnimatePresence mode="popLayout">
          {filteredTasks.length > 0 ? (
            filteredTasks.map((task, index) => (
              <motion.div
                key={task.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -100 }}
                transition={{ delay: index * 0.05 }}
              >
                <TaskCard
                  task={task}
                  isCompleted={task.status === 'completed' || task.is_complete}
                  onComplete={(id) => onTaskAction?.('complete', id)}
                  onDelete={(id) => onTaskAction?.('delete', id)}
                  onEdit={(id) => onTaskAction?.('edit', id)}
                />
              </motion.div>
            ))
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="glass-card p-12 text-center"
            >
              <Filter className="w-12 h-12 text-slate-400 mx-auto mb-4 opacity-50" />
              <p className="text-slate-300">No tasks found</p>
              <p className="text-sm text-slate-400 mt-1">
                Try adjusting your filters or create a new task
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};
