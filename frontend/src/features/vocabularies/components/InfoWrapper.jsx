import React, { useState } from 'react';
import '../../styles/InfoWrapper.css';

function InfoWrapper({ children, onAdd }) {
  const [newText, setNewText] = useState('');

  const handleAdd = () => {
    if (newText.trim() !== '') {
      onAdd(newText);
      setNewText('');
    }
  };

  return (
    <div>
      {/* Container for existing items */}
      <div className="info-container">
        {children}
      </div>

      {/* Add New Input and Button */}
      <div className="info-wrapper">
        <input
          type="text"
          value={newText}
          onChange={(e) => setNewText(e.target.value)}
          className="info-wrapper-input"
          placeholder="Add new..."
        />
        <button onClick={handleAdd} className="info-wrapper-btn save">
          Add
        </button>
      </div>
    </div>
  );
}

export default InfoWrapper;
