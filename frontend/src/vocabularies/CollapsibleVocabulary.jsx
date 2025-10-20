import React from 'react';
import '../../styles/CollapsibleVocabulary.css';

function CollapsibleVocabulary({ title, onClick }) {
  return (
    <div className="collapsible-vocabulary" onClick={onClick}>
      <div className="collapsible-vocabulary-header">
        {title}
      </div>
    </div>
  );
}

export default CollapsibleVocabulary;