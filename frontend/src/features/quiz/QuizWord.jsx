import React, { useMemo } from "react";
import QuizAnswerUnit from "./components/QuizAnswerUnit";
import Row from "./components/Row";
import {
  groupDataByCategoryWithHiddenWord,
  groupDataByCategory,
  filteredSynonyms,
} from "../../utils/wordProcessing";

function QuizWord({
  word,
  wordTranslation = [],
  wordDefinition = [],
  wordExample = [],
  wordSynonym = [],
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
        word?.word || "",
        "definition"
      ),
    [wordDefinition, word?.word]
  );

  const examplesByPartOfSpeech = useMemo(
    () =>
      groupDataByCategoryWithHiddenWord(
        wordExample,
        "part_of_speech",
        word?.word || "",
        "example_sentence"
      ),
    [wordExample, word?.word]
  );

  const synonyms = useMemo(
    () => filteredSynonyms(wordSynonym, word),
    [wordSynonym, word]
  );

  const renderGroupedHint = (groupedData, dataKey, emptyMessage) => {
    if (!groupedData || Object.keys(groupedData).length === 0) {
      return <p>{emptyMessage}</p>;
    }

    return Object.entries(groupedData).map(([category, items]) => (
      <div key={category}>
        <h4>{category}</h4>
        <ul>
          {items.map((item, index) => (
            <Row key={`${category}-${index}`} data={item[dataKey]} />
          ))}
        </ul>
      </div>
    ));
  };

  const renderSynonyms = () => {
    if (!synonyms || synonyms.length === 0) {
      return <p>No synonyms available.</p>;
    }

    return (
      <ul>
        {synonyms.map((synonym, index) => (
          <Row key={`synonym-${index}`} data={synonym.synonym} />
        ))}
      </ul>
    );
  };

  if (!word) {
    return <p>Loading word...</p>;
  }

  return (
    <div>
      <QuizAnswerUnit
        hintType="Definition"
        hintInfo={renderGroupedHint(
          definitionsByPartOfSpeech,
          "definition",
          "No definitions available."
        )}
        isFirst={true}
      />
      <QuizAnswerUnit
        hintType="Translation"
        hintInfo={renderGroupedHint(
          translationsByLanguage,
          "translation",
          "No translations available."
        )}
      />
      <QuizAnswerUnit
        hintType="Examples"
        hintInfo={renderGroupedHint(
          examplesByPartOfSpeech,
          "example_sentence",
          "No examples available."
        )}
      />
      <QuizAnswerUnit hintType="Synonyms" hintInfo={renderSynonyms()} />
    </div>
  );
}

export default QuizWord;
