import React from 'react';
function Header({ onAdd }) {
  return (
    <header className="app-header">
      <h1>TaskGPT</h1>
      <button className="add-btn" onClick={onAdd}>＋</button>
    </header>
  );
}
export default Header;
