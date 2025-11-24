import React from "react";
import { prepareWords } from "../../../../utils/wordProcessing";
import Word from "../../components/Word.jsx";

export default function ReadMode({ userWords, text }) {
  return (
    <>
      {prepareWords(text).map((word, index) => {
        return (
          <Word key={index} word={word} mod="read" userWords={userWords} />
        );
      })}
    </>
  );
}
