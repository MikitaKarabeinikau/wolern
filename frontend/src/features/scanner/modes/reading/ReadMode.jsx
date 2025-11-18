import React from "react";
import { prepareWords } from "../../../../utils/wordProcessing";
import Word from "../../components/Word.jsx";
export default function ReadMode({ userWords, text }) {
  console.log("ReadMode:", userWords);
  return (
    <>
      {prepareWords(text).map((word, index) => (
        <Word
          key={index}
          word={word}
          vocabulary={
            userWords.get(word.toLowerCase()) === undefined
              ? "unknown"
              : userWords.get(word.toLowerCase())
          }
        />
      ))}
    </>
  );
}
