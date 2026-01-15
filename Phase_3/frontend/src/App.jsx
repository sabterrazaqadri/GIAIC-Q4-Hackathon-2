import { useState, useCallback } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { StatsDashboard } from './components/Dashboard/StatsDashboard';
import { TaskBoard } from './components/TaskBoard/TaskBoard';
import { FloatingChatPanel } from './components/Chat/FloatingChatPanel';
import Navbar from './components/Common/Navbar';
import Footer from './components/Common/Footer';
import { useTaskData } from './hooks/useTaskData';
import './styles/globals.css';

const queryClient = new QueryClient();

function AppContent() {
  const { tasks, refreshTasks, completeTask, deleteTask } = useTaskData(2000);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  console.log('🎯 AppContent rendered with tasks:', tasks);

  const handleTaskAction = useCallback((action, taskId) => {
    switch (action) {
      case 'complete':
        completeTask(taskId);
        break;
      case 'delete':
        deleteTask(taskId);
        break;
      default:
        break;
    }
  }, [completeTask, deleteTask]);

  const handleTasksUpdate = useCallback(() => {
    // Trigger a refresh of tasks
    setRefreshTrigger(prev => prev + 1);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-primary flex flex-col">
      <Navbar />

      {/* Main Content */}
      <main className="flex-grow container mx-auto px-4 py-8 md:py-12 mt-20">
        {/* Dashboard Stats */}
        <StatsDashboard tasks={tasks} />

        {/* Task Board */}
        <div className="mt-12">
          <TaskBoard tasks={tasks} onTaskAction={handleTaskAction} />
        </div>
      </main>

      {/* Floating Chat Panel */}
      <FloatingChatPanel onTasksUpdate={handleTasksUpdate} />

      <Footer />
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}

export default App;