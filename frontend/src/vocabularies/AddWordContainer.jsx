import "react"
import { useEffect, useState } from "react";
import AddWord from "./AddWord";
import { useAuth } from "@clerk/clerk-react"


function AddWordContainer({onWordAdded}){

    const [error, setError] = useState(null);
    const { getToken } = useAuth();
    
    const handleAddWord = async (new_word) => {
        try {
            const token = await getToken(); 
            const response = await fetch("http://localhost:8000/user/words", {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`, // Use the token
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({word: new_word}),
            });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);  
        }
        if (onWordAdded){
            onWordAdded();
        } // Refresh words after adding

        } catch (error) {
            setError(error.message);
        }
    };
return (
    <div>
        <AddWord onAdd={handleAddWord} />
    </div>

    );

}

export default AddWordContainer;