import { motion } from 'framer-motion';
import { CheckCircle2, Clock, Zap, ListTodo } from 'lucide-react';
import { StatCard } from './StatCard';
import { useTaskStats } from '../../hooks/useTaskStats';

export const StatsDashboard = ({ tasks = [] }) => {
  const stats = useTaskStats(tasks);

  const statCards = [
    {
      icon: ListTodo,
      label: 'Total Tasks',
      value: stats.total,
      color: 'blue',
      variant: 'default',
    },
    {
      icon: CheckCircle2,
      label: 'Completed',
      value: stats.completed,
      percentage: stats.completionPercentage,
      color: 'green',
      variant: 'progress',
    },
    {
      icon: Clock,
      label: 'Pending',
      value: stats.pending,
      color: 'yellow',
      variant: 'default',
    },
    {
      icon: Zap,
      label: 'High Priority',
      value: stats.highPriority,
      color: 'red',
      variant: 'default',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-2xl md:text-3xl font-bold text-white mb-2">
          Dashboard Overview
        </h2>
        <p className="text-slate-300">
          Track your tasks and stay organized with AI assistance
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
        {statCards.map((card, index) => (
          <motion.div
            key={card.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1, duration: 0.5 }}
          >
            <StatCard {...card} />
          </motion.div>
        ))}
      </div>
    </div>
  );
};
