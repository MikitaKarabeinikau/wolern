import "react"
import React, {useState} from "react"

function AddWord({onAdd}){
    const [inputWord, setInputWord] = useState("");

    const handleInputChange = (event) => {
        setInputWord(event.target.value);
        console.log("Word:",event.target.value);
    }
    
    const handleButtonChange = (event) => {
        event.preventDefault();
        onAdd({word: inputWord});
        setInputWord("");
    };
    
    return (
        <>
        <div>
            <label>Word</label>
            <input type='text' 
            value={inputWord}
            onChange={handleInputChange} />
        </div>
        <button 
        onClick={handleButtonChange}>Add Word
        </button>
        </>
    )
}

export default AddWord;