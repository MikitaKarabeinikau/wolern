import React, { useState } from 'react';

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
    <div>
      <h3>Add New Word</h3>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Enter a word"
        onKeyDown={handleKeyPress}
      />
      <button onClick={handleClick}>Add Word</button>
    </div>
  );
}

export default AddWord;