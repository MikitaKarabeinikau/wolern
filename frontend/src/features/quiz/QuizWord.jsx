import React, { useMemo } from "react";
import QuizAnswerUnit from "./components/QuizAnswerUnit";
import Row from "./components/Row";
import {
  groupDataByCategoryWithHiddenWord,
  groupDataByCategory,
  filteredSynonyms,
  changeSeparatePart,
} from "../../utils/wordProcessing";

function QuizWord({
  word,
  wordTranslation,
  wordDefinition,
  wordExample,
  wordSynonym,
}) {
  const translationsByLanguage = useMemo(
    () => groupDataByCategory(wordTranslation, "language"),
    [wordTranslation]
  );

  const definitionsByPartOfSpeech = useMemo(
    () =>
      groupDataByCategoryWithHiddenWord(
        wordDefinition,
        "part_of_speech",
        word.word,
        "definition"
      ),
    [wordDefinition, word.word]
  );

  const examplesByPartOfSpeech = useMemo(
    () =>
      groupDataByCategoryWithHiddenWord(
        wordExample,
        "part_of_speech",
        word.word,
        "example_sentence"
      ),
    [wordExample, word.word]
  );

  const synonyms = useMemo(
    () => filteredSynonyms(wordSynonym, word),
    [wordSynonym, word]
  );

  const renderHint = (hintType, groupedData, dataKey, emptyMessage) => {
    if (!groupedData || Object.keys(groupedData).length === 0) {
      return <p>{emptyMessage}</p>;
    }

    return Object.keys(groupedData).map((category) => (
      <div key={category}>
        <h4>{category}</h4>
        <ul>
          {groupedData[category].map((item, index) => (
            <Row key={index} data={item[dataKey]} />
          ))}
        </ul>
      </div>
    ));
  };

  return (
    <div>
      <QuizAnswerUnit
        hintType="Definition"
        hintInfo={renderHint(
          "Definition",
          definitionsByPartOfSpeech,
          "definition",
          "No definitions available."
        )}
        isFirst={true}
      />
      <QuizAnswerUnit
        hintType="Translation"
        hintInfo={renderHint(
          "Translation",
          translationsByLanguage,
          "translation",
          "No translations available."
        )}
      />
      <QuizAnswerUnit
        hintType="Examples"
        hintInfo={renderHint(
          "Examples",
          examplesByPartOfSpeech,
          "example_sentence",
          "No examples available."
        )}
      />
      <QuizAnswerUnit
        hintType="Synonyms"
        hintInfo={
          synonyms && synonyms.length > 0 ? (
            <ul>
              {synonyms.map((synonym, index) => (
                <Row key={index} data={synonym.synonym} />
              ))}
            </ul>
          ) : (
            <p>No synonyms available.</p>
          )
        }
      />
    </div>
  );
}

export default QuizWord;
