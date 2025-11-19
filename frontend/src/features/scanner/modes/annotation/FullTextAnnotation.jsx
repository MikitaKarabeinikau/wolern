import React from "react";
import { prepareWords } from "../../../../utils/wordProcessing.js";
import Word from "../../components/Word.jsx";
import "../../../../../styles/Scanner.css";
function FullTextAnnotation({ text, userWords, vocabularies }) {
  return (
    <div className="fulltext-annotation">
      {prepareWords(text).map((word, index) => (
        <Word
          key={index}
          word={word}
          vocabulary={userWords.get(word.toLowerCase()) ?? "unknown"}
          mod={"edit"}
          vocabularies={vocabularies}
        />
      ))}
    </div>
  );
}

export default FullTextAnnotation;
