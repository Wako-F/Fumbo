let WORD_LIST = {}; // Now loaded dynamically

// Asynchronously load the word list from words_cleaned.txt
async function loadWordList() {
  try {
    const response = await fetch('words_cleaned.txt');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const text = await response.text();
    const lines = text.split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      // Split on the first colon to separate word and definition
      const colonIndex = trimmed.indexOf(':');
      if (colonIndex === -1) continue;
      const word = trimmed.substring(0, colonIndex).trim().toLowerCase();
      const definition = trimmed.substring(colonIndex + 1).trim();
      // Only add non-empty words
      if (word) {
        WORD_LIST[word] = definition;
      }
    }
    console.log('Word list loaded. Keys:', Object.keys(WORD_LIST));
  } catch (err) {
    console.error('Failed to load word list', err);
  }
}

// Immediately load the word list and attach the promise globally,
// so that other code can wait for it.
window.wordListPromise = loadWordList();

const getRandomWord = () => {
  const words = Object.keys(WORD_LIST);
  if (words.length === 0) return "";  // If not loaded yet, returns empty string
  return words[Math.floor(Math.random() * words.length)].toLowerCase();
};

const isValidWord = (word) => {
  return Object.prototype.hasOwnProperty.call(WORD_LIST, word.toLowerCase());
};

const getWordMeaning = (word) => {
  return WORD_LIST[word.toLowerCase()] || '';
};

// New function to return the first word of a word's definition (for hints)
const getHint = (word) => {
  const meaning = getWordMeaning(word);
  if (meaning) {
    const firstWord = meaning.split(/\s+/)[0];
    return firstWord;
  }
  return '';
}; 