import React, {useState} from 'react';
import '../../styles/Word.css';


const Collapsible = ({ title, children }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="collapsible">
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