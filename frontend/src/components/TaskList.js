import React from 'react';
import TaskItem from './TaskItem';

function TaskList({ tasks }) {
  const activeTasks = tasks.filter(t => !t.completed);
  const doneTasks = tasks.filter(t => t.completed);

  return (
    <section className="task-list">
      <h2>Мои задачи</h2>
      {activeTasks.length === 0 && <p>Все задачи выполнены! 🎉</p>}
      {activeTasks.map(t => <TaskItem key={t.id} task={t} />)}
      {doneTasks.length > 0 && (
        <div className="completed-section">
          <h3>Выполненные</h3>
          {doneTasks.map(t => <TaskItem key={t.id} task={t} completed />)}
        </div>
      )}
    </section>
  );
}
export default TaskList;
