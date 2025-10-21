import React,{useState} from "react";
import QuizAnswerUnit from "./QuizAnswerUnit";
function QuizWord({word, wordTranslation, wordDefinition, wordExample, wordSynonym}) {

  const translationsByLanguage = (wordTranslation || []).reduce((acc, trans) => {
    const lang = trans.language || 'Unknown';
    if (!acc[lang]) {
      acc[lang] = [];
    }
    acc[lang].push(trans);
    return acc;
  }, {});

  const definitionsByPartOfLanguage = (wordDefinition || []).reduce((acc, def) => {
    const pos = def.part_of_speech || 'Unknown';
    if (!acc[pos]) {
      acc[pos] = [];
    }
    acc[pos].push(def);
    return acc;
  }, {});

  const examplesByPartOfLanguage = (wordExample || []).reduce((acc, ex) => {
    const pos = ex.part_of_speech || 'Unknown';
    if (!acc[pos]) {
      acc[pos] = [];
    }
    acc[pos].push(ex);
    return acc;
  }, {});
  return (
    <div>
      <QuizAnswerUnit hintType={'Definition'} hintInfo={
        Object.keys(definitionsByPartOfLanguage).length > 0 ? (
          Object.keys(definitionsByPartOfLanguage).map(partOfSpeech => (
            <div key={partOfSpeech}>
              <h4>{partOfSpeech}</h4>
            <ul>
              {definitionsByPartOfLanguage[partOfSpeech].map((definition, index) => (
                <li key={index}>{definition.definition}</li>
              ))}
            </ul>
          </div>
        ))
      ) : (
        <p>No definitions available.</p>
      )}
      isFirst={true}
      />
      <QuizAnswerUnit hintType={'Translation'} hintInfo={
        Object.keys(translationsByLanguage).length > 0 ? (
          Object.keys(translationsByLanguage).map(language => (
            <div key={language}>
              <h4>{language}</h4>
              <ul>
              {translationsByLanguage[language].map((translation, index) => (
                <li key={index}>{translation.translation}</li>
              ))}
            </ul>
          </div>
        
        ))
      ) : (
        <p>No translations available.</p>
      )}
      />
      
      <QuizAnswerUnit hintType={'Examples'} hintInfo={  
        Object.keys(examplesByPartOfLanguage).length > 0 ? (
          Object.keys(examplesByPartOfLanguage).map(partOfSpeech => (
            <div key={partOfSpeech}>
              <h4>{partOfSpeech}</h4>
              <ul>
              {examplesByPartOfLanguage[partOfSpeech].map((example, index) => (
                <li key={index}>{example.example}</li>
              ))}
            </ul>
          </div>
        ))
      ) : (
        <p>No examples available.</p>
      )}  />
      <QuizAnswerUnit hintType={'Synonyms'} hintInfo=
      {wordSynonym && wordSynonym.length > 0 ? (
        <ul>
          {wordSynonym.map((synonym, index) => (
            <li key={index}>{synonym.synonym}</li>
          ))}
        </ul>
      ) : (
        <p>No synonyms available.</p>
      )}
      />
    </div>
  )
}

export default QuizWord;
