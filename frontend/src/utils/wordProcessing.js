export function processWords(words, maps) {
  const {
    translationsMap,
    definitionsMap,
    examplesMap,
    synonymsMap,
    warningsMap,
    tagsMap,
  } = maps;

  return words.map((wordObj) => ({
    ...wordObj,
    translations: translationsMap?.[wordObj.id] || [],
    definitions: definitionsMap?.[wordObj.id] || [],
    examples: examplesMap?.[wordObj.id] || [],
    synonyms: synonymsMap?.[wordObj.id] || [],
    warnings: warningsMap?.[wordObj.id] || [],
    tags: tagsMap?.[wordObj.id] || [],
  }));
}

export const createMapByWordId = (items, key) => {
  const map = {};
  if (!items || !items[key]) return map;

  for (const item of items[key]) {
    const wordId = item.word_id;
    if (!map[wordId]) {
      map[wordId] = [];
    }
    map[wordId].push(item);
  }
  return map;
};

export const groupDataByCategory = (data, categoryField) => {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return {};
  }

  return data.reduce((acc, item) => {
    const category = item[categoryField] || "Other";
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(item);
    return acc;
  }, {});
};


export const groupDataByCategoryWithHiddenWord = (
  data,
  categoryField,
  wordToHide,
  contentField
) => {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return {};
  }

  const hiddenWord = "_".repeat(wordToHide.length);
  const regex = new RegExp(`\\b${wordToHide}\\b`, "gi");

  return data.reduce((acc, item) => {
    const category = item[categoryField] || "Other";
    if (!acc[category]) {
      acc[category] = [];
    }

    const hiddenContent = item[contentField]
      ? item[contentField].replace(regex, hiddenWord)
      : "";

    acc[category].push({
      ...item,
      [contentField]: hiddenContent,
    });
    return acc;
  }, {});
};

export const findSeparatePart = (mainWord, wordToCompare) => {
  if (typeof mainWord !== "string" || typeof wordToCompare !== "string") {
    console.error("Invalid input: mainWord and wordToCompare must be strings.");
    return "";
  }

  let longestCommonSubstring = "";
  for (let i = 0; i < mainWord.length; i++) {
    for (let j = i; j < mainWord.length; j++) {
      const substring = mainWord.substring(i, j + 1);
      if (
        wordToCompare.includes(substring) &&
        substring.length > longestCommonSubstring.length
      ) {
        longestCommonSubstring = substring;
      }
    }
  }
  return longestCommonSubstring;
};

export const changeSeparatePart = (text, wordToCompare) => {
  if (typeof text !== "string" || typeof wordToCompare !== "string") {
    console.error("Invalid input: text and wordToCompare must be strings.");
    return text;
  }

  const commonPart = findSeparatePart(text, wordToCompare);
  if (commonPart.length >= 3) {
    return text.replace(commonPart, "...");
  }
  return text;
};

  export const changeSeparatePartInText = (textArray, wordToCompare, property) => {
    return textArray.map((item) => {
      if (item[property]) {
        return {
          ...item,
          [property]: changeSeparatePart(item[property], wordToCompare),
        };
      }
      return item;
    });
  };

  export const filteredSynonyms = (wordSynonym = [], word) => {
    return wordSynonym.reduce((acc, syn) => {
      if (word.word.toLowerCase() !== syn.synonym.toLowerCase()) {
        const modifiedSyn = changeSeparatePartInText([syn], word.word, 'synonym')[0];
        acc.push(modifiedSyn);
      }
      return acc;
    }, []);
  };

  export const calculateIndexes = (correctWord, userAnswer) => {
  const correct = [];
  const incorrect = [];
  const extraCorrect = [];
  const extraIncorrect = [];
  const safeUserAnswer = userAnswer || "";
  const maxLength = Math.max(correctWord.length, safeUserAnswer.length);

  const isEmpty = correctWord.length === 0 && safeUserAnswer.length === 0;

  for (let i = 0; i < maxLength; i++) {
    const wordLetter = correctWord[i] || null;
    const userAnswerLetter = safeUserAnswer[i] || null;

    if (wordLetter && userAnswerLetter) {
      if (wordLetter === userAnswerLetter) {
        correct.push(i);
      } else {
        incorrect.push(i);
      }
    } else if (wordLetter) {
      extraCorrect.push(i);
    } else if (userAnswerLetter) {
      extraIncorrect.push(i);
    }
  }

  return { correct, incorrect, extraCorrect, extraIncorrect, isEmpty };
};

export const prepareWords = (text) => {
    const separatedWords = text.split(" ");
    const cleanedWords = separatedWords.map((word) =>
      word.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "")
    );
    const filteredWords = cleanedWords.filter((word) => word.trim() !== "");
    return filteredWords;
  };

  