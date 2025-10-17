import React, {useState} from 'react';
import '../../styles/Word.css';


const Collapsible = ({ title, wordId, children, onDelete }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  const handleDelete = () => {
    console.log(`Delete requested for item ID: ${wordId}`);
    onDelete(wordId);

  }

  return (
    <div className="collapsible">
      <div>
        <button onClick={handleDelete} className='unit-cell-btn delete' style={{float: 'right', marginTop: '0.5rem', marginRight: '0.5rem'}}>Delete Word</button>
      </div>
      <button className="collapsible-toggle" onClick={handleToggle}>
        {title}
        <span className={`collapsible-icon ${isOpen ? 'open' : ''}`}>▼</span>
      </button>
      <div className={`collapsible-content ${isOpen ? 'open' : ''}`}>
        <div className="collapsible-content-inner">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Collapsible;