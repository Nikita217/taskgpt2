import React from 'react';

function TaskItem({ task, completed = false }) {
  const { title, description, dueDate, frozen } = task;
  const itemClass = 'task-item' + (completed ? ' done' : '') + (frozen ? ' frozen' : '');

  return (
    <div className={itemClass}>
      <input type="checkbox" checked={completed} readOnly />
      <div className="task-info">
        <h4>{title}</h4>
        {description && <p>{description}</p>}
        {dueDate && <span className="due-date">до {dueDate}</span>}
      </div>
      {task.newAchievement && <span className="achievement-badge">🏅</span>}
    </div>
  );
}

export default TaskItem;
