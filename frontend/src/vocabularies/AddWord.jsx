import React, { useState } from 'react';
import '../../styles/Word.css';

function AddWord({ onAdd }) {
  const [inputValue, setInputValue] = useState('');

  const handleClick = () => {
    if (inputValue.trim()) {
      onAdd(inputValue);
      setInputValue(''); // Clear the input after adding
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      console.log("Enter key pressed");
      handleClick();
    }
  };

  return (
    <div className="add-container">
      <div className='input-section'>
        <h3>Add New Word</h3>
        <div>
          <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Enter a word"
                  onKeyDown={handleKeyPress}
                  className="field"
                />
                <button onClick={handleClick}
                className='btn'

                >Add Word</button>
        </div>

      
      </div>
      
    </div>
  );
}

export default AddWord;