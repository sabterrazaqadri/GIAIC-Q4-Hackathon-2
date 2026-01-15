import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export const StatCard = ({
  icon: Icon,
  label,
  value,
  percentage,
  color = 'purple',
  variant = 'default',
}) => {
  const [displayValue, setDisplayValue] = useState(0);

  // Animate number counter
  useEffect(() => {
    let currentValue = 0;
    const increment = Math.ceil(value / 30); // Animate over 30 frames
    const interval = setInterval(() => {
      currentValue += increment;
      if (currentValue >= value) {
        setDisplayValue(value);
        clearInterval(interval);
      } else {
        setDisplayValue(currentValue);
      }
    }, 30);

    return () => clearInterval(interval);
  }, [value]);

  const colorClasses = {
    purple: 'from-purple-600 to-purple-400',
    green: 'from-green-600 to-green-400',
    yellow: 'from-yellow-600 to-yellow-400',
    red: 'from-red-600 to-red-400',
    blue: 'from-blue-600 to-blue-400',
  };

  const bgColor = {
    purple: 'bg-purple-500/10',
    green: 'bg-green-500/10',
    yellow: 'bg-yellow-500/10',
    red: 'bg-red-500/10',
    blue: 'bg-blue-500/10',
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      whileHover={{ scale: 1.05, y: -5 }}
      className="glass-card p-6 group"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-sm font-medium text-slate-300 mb-2 group-hover:text-slate-100 transition-colors"
          >
            {label}
          </motion.p>

          <div className="flex items-end gap-2">
            <motion.h3
              key={displayValue}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.2 }}
              className={`text-3xl md:text-4xl font-bold bg-gradient-to-r ${colorClasses[color]} bg-clip-text text-transparent`}
            >
              {displayValue}
            </motion.h3>

            {percentage !== undefined && (
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="text-sm font-medium text-slate-300 mb-1"
              >
                {percentage}%
              </motion.span>
            )}
          </div>
        </div>

        <motion.div
          whileHover={{ rotate: 10, scale: 1.1 }}
          transition={{ type: 'spring', stiffness: 200 }}
          className={`${bgColor[color]} p-3 rounded-xl group-hover:shadow-glow transition-all`}
        >
          <Icon className={`w-6 h-6 text-${color}-400`} />
        </motion.div>
      </div>

      {variant === 'progress' && (
        <motion.div
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ delay: 0.3, duration: 0.6 }}
          className="mt-4 h-1.5 bg-white/10 rounded-full overflow-hidden"
          style={{ transformOrigin: 'left' }}
        >
          <motion.div
            className={`h-full bg-gradient-to-r ${colorClasses[color]}`}
            initial={{ width: 0 }}
            animate={{ width: `${percentage || 0}%` }}
            transition={{ delay: 0.5, duration: 1 }}
          />
        </motion.div>
      )}
    </motion.div>
  );
};
