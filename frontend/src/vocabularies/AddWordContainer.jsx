import "react"
import { useEffect, useState } from "react";
import AddWord from "./AddWord";
import { useAuth } from "@clerk/clerk-react"


function AddWordContainer(){
    const [words, setWords] = useState([]);
    const [error, setError ] = useState(null);
    const { getToken } = useAuth();


    const fetchWords = async () => {
        try {
            const token = await getToken();
            const response = await fetch("http://localhost:8000/user/words", {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            setWords(data.words); // Assuming the response is { "words": [...] }
            setError(null);
        } catch (e) {
            setError(e.message);
            setWords([]);
        }
    };

    useEffect(() => {
        fetchWords();
    }, []);

    const handleAddWord = async (new_word) => {
        try {
            const token = await getToken(); // Get the token
            const response = await fetch("http://localhost:8000/user/words", {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`, // Use the token
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(new_word),
            });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);  
        }
        await fetchWords(); // Refresh words after adding
        } catch (error) {
            setError(error.message);
        }
    };
return (
    <>
        {error && <div style={{ color: "red" }}>Error: {error}</div>}
        <AddWord onAdd={handleAddWord} />
        <div>
            <h2>Words List</h2>
            <ul>
                {words.map((word, index) => (
                    <li key={index}>{word.word}</li>
                ))}
            </ul>
        </div>
    </>

    );

}

export default AddWordContainer;