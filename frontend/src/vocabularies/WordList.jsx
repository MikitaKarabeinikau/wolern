import React from "react";
import Word from "./Word";

function WordList({words}) {
   if (!words || words.length === 0) {
        return (
            <div>
                <h2>Word List</h2>
                <p>No words to display.</p>
            </div>
        );
    }

    return (
        <div>
            <h2>Word List</h2>
            
            {words.map((wordObj) => (
                <Word key={wordObj.id} wordData={wordObj} />
            ))}
        </div>
    )
}

export default WordList;