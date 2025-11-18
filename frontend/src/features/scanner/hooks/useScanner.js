import {apiClient} from "../../../api/apiClient";
import {useAuth} from "@clerk/clerk-react";
import {useCallback, useState} from "react";

export  function useScanner() {
  const {getToken} = useAuth();
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [words,setWords]=useState([]);

  const fetchWordData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
        const wordsData = await apiClient("/user/words/vocabularies", getToken, {
            method:"GET"
        });
        setWords(wordsData.words_and_vocabularies);
        console.log("Fetched words data:", wordsData);

        if  (onSuccess){
            onSuccess();
        }
    }catch (e) {
        setError(e.message);
        } finally {
        setIsLoading(false);
        }
    },[getToken]);

  return {fetchWordData,words,isLoading,error};
  }

  