import React, {useState} from 'react';
import '../../styles/Word.css';
import Vocabularies from './Vocabularies';


const Collapsible = ({ title, wordId, children, onDelete, onChangeVocabulary, vocabularies }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isVocabularyMenuOpen, setIsVocabularyMenuOpen] = useState(false); // New state


  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  const handleDelete = () => {
    console.log(`Delete requested for item ID: ${wordId}`);
    onDelete(wordId);

  }

  const handleOpenVocabularyMenu = () => {
    setIsVocabularyMenuOpen(true);
  };

  const handleCloseVocabularyMenu = () => {
    setIsVocabularyMenuOpen(false);
  };

  
  const handleChangeVocabulary = (newVocabulary) => {
    console.log(`Change Vocabulary requested for item ID: ${wordId}`);
    onChangeVocabulary(wordId, newVocabulary);
  }
  
  return (
    <div className="collapsible">
      <div>
        <button onClick={handleDelete} className='unit-cell-btn delete'>Delete Word</button>
      </div>
      <div>
        <button onClick={handleOpenVocabularyMenu}>Change Vocabulary</button>
        {isVocabularyMenuOpen && (
          <div className="vocabulary-menu">
            {vocabularies.map((vocabulary) => (
              <button key={vocabulary} onClick={() => handleChangeVocabulary(vocabulary)}>
                {vocabulary}
              </button>
            ))}
            <button onClick={handleCloseVocabularyMenu}>Cancel</button>
          </div>
        )}
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