import React, { useState } from 'react';

function AddTaskModal({ onClose, onTaskAdded }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [aiSuggest, setAiSuggest] = useState([]);

  const save = () => {
    setLoading(True);
  };

  async function save() {
    if (!title) return;
    setLoading(true);
    const res = await fetch('/api/tasks', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({title, description, dueDate})
    });
    const newTask = await res.json();
    onTaskAdded(newTask);
  }

  const getSuggestions = async () => {
    if (!description.trim()) return;
    const res = await fetch('/api/ai_suggest', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({prompt: description})
    });
    const data = await res.json();
    setAiSuggest(data.suggestions || []);
  };

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <h3>Новая задача</h3>
        <input placeholder="Название" value={title} onChange={e=>setTitle(e.target.value)} />
        <textarea placeholder="Описание / цель" value={description} onChange={e=>setDescription(e.target.value)} />
        <input type="date" value={dueDate} onChange={e=>setDueDate(e.target.value)} />
        <button onClick={getSuggestions}>🔮 AI предложения</button>
        {aiSuggest.length>0 && (
          <div className="ai-suggestions">
            {aiSuggest.map((s,i)=><div key={i} onClick={()=>setTitle(s)}>{s}</div>)}
          </div>
        )}
        <button onClick={save} disabled={loading}>{loading?'Сохранение...':'Добавить'}</button>
        <button onClick={onClose}>Отмена</button>
      </div>
    </div>
  );
}
export default AddTaskModal;
