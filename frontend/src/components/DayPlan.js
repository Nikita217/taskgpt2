import React, { useState } from 'react';

function DayPlan() {
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);

  const generatePlan = () => {
    setLoading(true);
    fetch('/api/plan')
      .then(res => res.json())
      .then(data => {
        setPlan(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  return (
    <section className="day-plan">
      <h2>План на день</h2>
      <button onClick={generatePlan} disabled={loading}>
        {loading ? 'Генерация...' : 'Сгенерировать план'}
      </button>
      {plan && plan.map((slot, idx) => (
        <div key={idx} className="time-slot">
          <h3>{slot.timeRange}</h3>
          <ul>
            {slot.tasks.map((t,i)=> <li key={i}>{t}</li>)}
          </ul>
        </div>
      ))}
    </section>
  );
}

export default DayPlan;
