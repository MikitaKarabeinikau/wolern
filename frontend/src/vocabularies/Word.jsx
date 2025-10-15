import React from 'react'; // Removed unused useState, useEffect
import Collapsible from './Collapsible';
import '../../styles/Word.css';
import UnitCell from './UnitCell';

function Word({ wordData, translations, definitions, examples, synonyms, warnings, tags, onDataChange, getToken }) {
  const { word } = wordData;

  // This logic correctly groups your flat list of translations into an
  // object where each key is a language.
  const translationsByLanguage = (translations || []).reduce((acc, trans) => {
    const lang = trans.language || 'Unknown';
    if (!acc[lang]) {
      acc[lang] = [];
    }
    acc[lang].push(trans);
    return acc;
  }, {});
  const definitionsByPartOfLanguage = (definitions || []).reduce((acc, def) => {
    const pos = def.part_of_speech || 'Unknown';
    if (!acc[pos]) {
      acc[pos] = [];
    }
    acc[pos].push(def);
    return acc;
  }, {});

  const examplesByPartOfLanguage = (examples || []).reduce((acc, ex) => {
    const pos = ex.part_of_speech || 'Unknown';
    if (!acc[pos]) {
      acc[pos] = [];
    }
    acc[pos].push(ex);
    return acc;
  }, {});
  return (
    <Collapsible title={word}>
      <div>
        <h4>Translations</h4>
        {/* This correctly checks if there are any translations to display */}
        {Object.keys(translationsByLanguage).length > 0 ? (
          // This maps over each language (e.g., "Spanish", "French")
          Object.keys(translationsByLanguage).map(language => (
            <div key={language}>
              <strong>{language}:</strong>
              <ul>
                {translationsByLanguage[language].map(trans => (
                  <li key={trans.id}>
                    {trans.id}. {trans.translation}
                  </li>
                ))}
              </ul>
            </div>
          ))
        ) : (

          <p>No translations available.</p>
        )}
      </div>
      <div style={{ marginTop: '1rem' }}>
        <h4>Definitions</h4>
        {Object.keys(definitionsByPartOfLanguage).length > 0 ? (
          Object.keys(definitionsByPartOfLanguage).map(pos => (
            // FIX: Add a return statement before the inner map.
            // Or, ensure the inner map implicitly returns the component.
            // The simplest fix is to wrap the inner map's content in a div.
            <div key={pos}>
              <strong>{pos}:</strong>
              {definitionsByPartOfLanguage[pos].map(def => (
                <UnitCell
                  key={def.id}
                  item={{ id: def.id, text: def.definition }}
                  onUpdate={async (id, newText) => {
                    try{
                      const token = await getToken();
                      const response = await fetch(`http://localhost:8000/user/words/definitions/${id}`, {
                        method: 'PUT',
                        headers: {
                          'Content-Type': 'application/json',
                          Authorization: `Bearer ${token}`,
                        },
                        body: JSON.stringify({ definition: newText, id: id, word_id: def.word_id }), // Adjust payload as needed
                      });
                      if (response.ok) {
                        console.log(`Definition ${id} updated successfully`);
                        onDataChange(); // Notify parent to refresh data
                      } else {
                        console.error('Failed to update definition');
                      }
                    } catch (error) {
                      console.error('Error updating definition:', error);
                    }

 
                    console.log(`Update ${id} with new text: ${newText}`);
                  }}
                  onDelete={async (id) => {
                    console.log(`Delete button clicked for definition ID: ${id}`);
                    console.log('getToken function:', getToken);
                    try {
                      const token = await getToken();
                      const response = await fetch(`http://localhost:8000/user/words/definitions/${id}`, {
                        method: 'DELETE',
                        headers: {
                          'Content-Type': 'application/json',
                          Authorization: `Bearer ${token}`,
                        },
                      });
                      if (response.ok) {
                        console.log(`Definition ${id} deleted successfully`);
                        onDataChange(); // Notify parent to refresh data
                      } else {
                        console.error('Failed to delete definition');
                      } 
                    } catch (error) {
                      console.error('Error deleting definition:', error);
                    }
                  }}
                />  
              ))}
            </div>
          ))
        ) : (
          <p>No definitions available.</p>
        )}
      </div>
      <div style={{ marginTop: '1rem' }}>
        <h4>Examples</h4>
        {Object.keys(examplesByPartOfLanguage).length > 0 ? (
          Object.keys(examplesByPartOfLanguage).map(pos => (
            <div key={pos}>
              <strong>{pos}:</strong>
              <ul>
                {examplesByPartOfLanguage[pos].map(ex => (
                  <li key={ex.id}>
                    {ex.id}. {ex.example_sentence}
                  </li>
                ))}
              </ul>
            </div>
          ))
        ) : (
          <p>No examples available.</p>
        )}
      </div>
      <div>
        <h4>Synonyms</h4>
        {synonyms && synonyms.length > 0 ? (
          <ul>
            {synonyms.map(syn => (
              <li key={syn.id}>
                {syn.id}. {syn.synonym}
              </li>
            ))}
          </ul>
        ) : (
          <p>No synonyms available.</p>
        )}
      </div>
      <div>
        <h4>Tags</h4>
        {tags && tags.length > 0 ? (
          <ul>
            {tags.map(tag => (
              <li key={tag.id}> {tag.tag} </li>
            ))}
          </ul>
        ) : (
          <p>No tags available.</p>
        )}  
      </div>
      <div>
        <h4>Warnings</h4>
        {warnings && warnings.length > 0 ? (
          <ul>
            {warnings.map(warn => (
              <li key={warn.id}>
                {warn.id}. {warn.warning}
              </li>
            ))}
          </ul>
        ) : (
          <p>No warnings available.</p>
        )}
      </div>
    </Collapsible>
  );
}

export default Word;