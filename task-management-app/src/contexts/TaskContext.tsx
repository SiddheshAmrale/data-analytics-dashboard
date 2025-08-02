import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface Task {
  id: string;
  title: string;
  description: string;
  status: 'todo' | 'in-progress' | 'review' | 'done';
  priority: 'low' | 'medium' | 'high';
  assignee: string;
  dueDate: string;
  createdAt: string;
}

interface TaskContextType {
  tasks: Task[];
  addTask: (task: Omit<Task, 'id' | 'createdAt'>) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  deleteTask: (id: string) => void;
  moveTask: (taskId: string, fromStatus: string, toStatus: string) => void;
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

export const useTasks = () => {
  const context = useContext(TaskContext);
  if (context === undefined) {
    throw new Error('useTasks must be used within a TaskProvider');
  }
  return context;
};

interface TaskProviderProps {
  children: ReactNode;
}

export const TaskProvider: React.FC<TaskProviderProps> = ({ children }) => {
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => {
    // Load tasks from localStorage
    const storedTasks = localStorage.getItem('tasks');
    if (storedTasks) {
      setTasks(JSON.parse(storedTasks));
    } else {
      // Initialize with sample tasks
      const sampleTasks: Task[] = [
        {
          id: '1',
          title: 'Design new landing page',
          description: 'Create a modern and responsive landing page design',
          status: 'todo',
          priority: 'high',
          assignee: 'John Doe',
          dueDate: '2024-01-15',
          createdAt: new Date().toISOString()
        },
        {
          id: '2',
          title: 'Implement user authentication',
          description: 'Add login and registration functionality',
          status: 'in-progress',
          priority: 'high',
          assignee: 'Jane Smith',
          dueDate: '2024-01-20',
          createdAt: new Date().toISOString()
        },
        {
          id: '3',
          title: 'Write API documentation',
          description: 'Document all API endpoints and usage examples',
          status: 'review',
          priority: 'medium',
          assignee: 'Mike Johnson',
          dueDate: '2024-01-25',
          createdAt: new Date().toISOString()
        }
      ];
      setTasks(sampleTasks);
      localStorage.setItem('tasks', JSON.stringify(sampleTasks));
    }
  }, []);

  const addTask = (taskData: Omit<Task, 'id' | 'createdAt'>) => {
    const newTask: Task = {
      ...taskData,
      id: Date.now().toString(),
      createdAt: new Date().toISOString()
    };
    const updatedTasks = [...tasks, newTask];
    setTasks(updatedTasks);
    localStorage.setItem('tasks', JSON.stringify(updatedTasks));
  };

  const updateTask = (id: string, updates: Partial<Task>) => {
    const updatedTasks = tasks.map(task =>
      task.id === id ? { ...task, ...updates } : task
    );
    setTasks(updatedTasks);
    localStorage.setItem('tasks', JSON.stringify(updatedTasks));
  };

  const deleteTask = (id: string) => {
    const updatedTasks = tasks.filter(task => task.id !== id);
    setTasks(updatedTasks);
    localStorage.setItem('tasks', JSON.stringify(updatedTasks));
  };

  const moveTask = (taskId: string, fromStatus: string, toStatus: string) => {
    const updatedTasks = tasks.map(task =>
      task.id === taskId ? { ...task, status: toStatus as Task['status'] } : task
    );
    setTasks(updatedTasks);
    localStorage.setItem('tasks', JSON.stringify(updatedTasks));
  };

  const value = {
    tasks,
    addTask,
    updateTask,
    deleteTask,
    moveTask
  };

  return (
    <TaskContext.Provider value={value}>
      {children}
    </TaskContext.Provider>
  );
}; 