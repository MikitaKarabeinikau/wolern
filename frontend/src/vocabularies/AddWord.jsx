import React, { useState } from 'react';

function AddWord({ onAdd }) {
  const [inputValue, setInputValue] = useState('');

  const handleClick = () => {
    if (inputValue.trim()) {
      // FIX: Pass only the string value from the input field.
      // Do NOT pass an object like { word: inputValue }.
      onAdd(inputValue);
      setInputValue(''); // Clear the input after adding
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
      />
      <button onClick={handleClick}>Add Word</button>
    </div>
  );
}

export default AddWord;