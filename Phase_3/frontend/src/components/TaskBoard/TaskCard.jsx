import { motion } from 'framer-motion';
import { CheckCircle2, Circle, Trash2, Edit2 } from 'lucide-react';
import { getPriorityColor, getStatusColor } from '../../utils/taskHelpers';

export const TaskCard = ({
  task,
  onComplete,
  onDelete,
  onEdit,
  isCompleted,
}) => {
  const priorityColor = getPriorityColor(task.priority);
  const statusColor = getStatusColor(task.status);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: -100 }}
      transition={{ duration: 0.3 }}
      className="glass-card p-4 md:p-6 hover:shadow-card-hover group"
    >
      <div className="flex gap-4">
        {/* Checkbox */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => {
            if (isCompleted) {
              // Already completed, do nothing or uncomplete
              onComplete?.(task.id);
            } else {
              // Not completed, complete it
              onComplete?.(task.id);
            }
          }}
          className="flex-shrink-0 mt-1 focus:outline-none cursor-pointer"
          aria-label={isCompleted ? 'Task completed' : 'Mark as complete'}
          type="button"
        >
          {isCompleted ? (
            <CheckCircle2 className="w-6 h-6 text-green-400 hover:text-green-300" />
          ) : (
            <Circle className="w-6 h-6 text-slate-400 group-hover:text-slate-300 hover:text-blue-400" />
          )}
        </motion.button>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <motion.h3
            className={`text-base md:text-lg font-semibold truncate group-hover:text-white transition-colors ${
              isCompleted ? 'text-slate-400 line-through' : 'text-white'
            }`}
          >
            {task.title}
          </motion.h3>

          {task.description && (
            <motion.p
              className="text-sm text-slate-400 line-clamp-2 mt-1 group-hover:text-slate-300 transition-colors"
            >
              {task.description}
            </motion.p>
          )}

          {/* Badges */}
          <div className="flex gap-2 mt-3 flex-wrap">
            {task.priority && (
              <span
                className={`badge text-xs font-medium ${priorityColor.bg} ${priorityColor.text} ${priorityColor.border} border`}
              >
                {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
              </span>
            )}

            {task.status && (
              <span
                className={`badge text-xs font-medium ${statusColor.bg} ${statusColor.text} ${statusColor.border} border`}
              >
                {task.status.charAt(0).toUpperCase() + task.status.slice(1)}
              </span>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex-shrink-0 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onEdit?.(task.id)}
            className="btn-ghost p-2"
            aria-label="Edit task"
          >
            <Edit2 className="w-4 h-4" />
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onDelete?.(task.id)}
            className="btn-ghost p-2 text-red-400 hover:text-red-300 hover:bg-red-500/10"
            aria-label="Delete task"
          >
            <Trash2 className="w-4 h-4" />
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
};
