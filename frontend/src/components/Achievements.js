import React, { useEffect, useState } from 'react';

function Achievements() {
  const [achievements, setAchievements] = useState([]);

  useEffect(() => {
    fetch('/api/achievements')
      .then(res => res.json())
      .then(data => setAchievements(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <section className="achievements">
      <h2>Достижения</h2>
      <div className="achievement-list">
        {achievements.map(a => (
          <div key={a.code} className={'achievement ' + (a.unlocked ? 'unlocked' : 'locked')}>
            <span className="icon">{a.icon}</span>
            <span className="name">{a.name}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Achievements;
