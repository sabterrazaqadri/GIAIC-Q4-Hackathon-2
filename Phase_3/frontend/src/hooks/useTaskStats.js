import { useMemo } from 'react';
import { calculateTaskStats } from '../utils/taskHelpers';

export const useTaskStats = (tasks = []) => {
  return useMemo(() => {
    return calculateTaskStats(tasks);
  }, [tasks]);
};
