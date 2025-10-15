import React from "react";
import Word from "./Word";

// FIX: Accept 'translationsMap' as a prop
function WordList({ words, translationsMap, definitionsMap, examplesMap, synonymsMap, warningsMap, tagsMap, onDataChange, getToken}) {
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
            
            {words.map((wordObj) => {
                const translations = (translationsMap && translationsMap[wordObj.id]) || [];
                const definitions = (definitionsMap && definitionsMap[wordObj.id]) || [];
                const examples = (examplesMap && examplesMap[wordObj.id]) || [];
                const synonyms = (synonymsMap && synonymsMap[wordObj.id]) || [];
                const warnings = (warningsMap && warningsMap[wordObj.id]) || [];
                const tags = (tagsMap && tagsMap[wordObj.id]) || [];
                return (
                    <Word 
                        key={wordObj.id} 
                        wordData={wordObj} 
                        translations={translations} 
                        definitions={definitions}
                        examples={examples}
                        synonyms={synonyms}
                        warnings={warnings}
                        tags={tags}
                        onDataChange={onDataChange}
                        getToken={getToken}
                    />
                );
            })}
        </div>
    )
}

export default WordList;