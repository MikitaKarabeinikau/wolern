import React from 'react'; // Removed unused useState, useEffect
import Collapsible from './Collapsible';

function Word({ wordData, translations, definitions, examples, synonyms, warnings, tags }) {
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
            <div key={pos}>
              <strong>{pos}:</strong>
              <ul>
                {definitionsByPartOfLanguage[pos].map(def => (
                  <li key={def.id}>
                    {def.id}. {def.definition}
                  </li>
                ))}
              </ul>
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
                    {console.log("Example sentence:", ex.example_sentence)}
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