import React,{useState} from "react";
import QuizAnswerUnit from "./QuizAnswerUnit";
import Row from "./Row";


function QuizWord({word, wordTranslation, wordDefinition, wordExample, wordSynonym}) {

  const findSeparatePart = (mainWord, wordToCompare) => {
    let longestCommonSubstring = "";
    for (let i = 0; i < mainWord.length; i++) {
      for (let j = i; j < mainWord.length; j++) {
        const substring = mainWord.substring(i, j + 1);
        if (wordToCompare.includes(substring) && substring.length > longestCommonSubstring.length) {
          longestCommonSubstring = substring;
        }
      }
    }
    return longestCommonSubstring;
  };
     
  const changeSeparatePart = (text, wordToCompare) => {
    const commonPart = findSeparatePart(text, wordToCompare);
    if (commonPart.length >= 3) {
      return text.replace(commonPart, "...");
    }
    return text;
  };
  
    const changeSeparatePartInText = (textArray, wordToCompare, property) => {
    return textArray.map(item => {
      if (item[property]) {
        return {
          ...item,
          [property]: changeSeparatePart(item[property], wordToCompare)
        };
      }
      return item;
    });
  }

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
    const modifiedDef = changeSeparatePartInText([def], word.word, 'definition')[0];
    acc[pos].push(modifiedDef);
    return acc;
  }, {});

  const examplesByPartOfLanguage = (wordExample || []).reduce((acc, ex) => {
    const pos = ex.part_of_speech || 'Unknown';
    if (!acc[pos]) {
      acc[pos] = [];
    }
    const modifiedEx = changeSeparatePartInText([ex], word.word, 'example_sentence')[0];
    acc[pos].push(modifiedEx);
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
                <Row key={index} data={definition.definition} />
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
                <Row key={index} data={translation.translation} />
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
                <Row key={index} data={example.example_sentence} />
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
            <Row key={index} data={synonym.synonym} />
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
