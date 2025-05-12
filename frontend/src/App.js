import React, { useState, useEffect } from 'react';
import TaskList from './components/TaskList';
import DayPlan from './components/DayPlan';
import Achievements from './components/Achievements';
import AddTaskModal from './components/AddTaskModal';
import Header from './components/Header';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);

  useEffect(() => {
    fetch('/api/tasks')
      .then(res => res.json())
      .then(data => setTasks(data))
      .catch(err => console.error('Failed to fetch tasks', err));
  }, []);

  const handleTaskAdded = (newTask) => {
    setTasks(prev => [...prev, newTask]);
    setShowAddModal(false);
  };

  return (
    <div className="App">
      <Header onAdd={() => setShowAddModal(true)} />
      <main>
        <TaskList tasks={tasks} />
        <DayPlan tasks={tasks} />
        <Achievements tasks={tasks} />
      </main>
      {showAddModal &&
        <AddTaskModal onClose={() => setShowAddModal(false)} onTaskAdded={handleTaskAdded} />
      }
    </div>
  );
}

export default App;
