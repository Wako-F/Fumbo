class WordleGame {
  constructor() {
    this.solution = getRandomWord();
    this.rows = 6;
    this.cols = 5;
    this.currentRow = 0;
    this.currentTile = 0;
    this.isGameOver = false;
    this.guesses = [];
    
    this.stats = this.loadStats();
    console.log("Solution:", this.solution); // For debugging
  }

  loadStats() {
    const savedStats = localStorage.getItem('swahiliWordleStats') || JSON.stringify({
      gamesPlayed: 0,
      gamesWon: 0,
      currentStreak: 0,
      maxStreak: 0,
      lastGame: null
    });
    return JSON.parse(savedStats);
  }

  saveStats() {
    localStorage.setItem('swahiliWordleStats', JSON.stringify(this.stats));
  }

  checkGuess(guess) {
    const solutionArray = this.solution.split("");
    const guessArray = guess.split("");
    const result = Array(this.cols).fill("absent");
    
    // Count the letters in the solution
    const letterCount = {};
    solutionArray.forEach(letter => {
      letterCount[letter] = (letterCount[letter] || 0) + 1;
    });

    // First pass: mark correct letters
    guessArray.forEach((letter, i) => {
      if (letter === solutionArray[i]) {
        result[i] = "correct";
        letterCount[letter]--;
      }
    });

    // Second pass: mark present letters
    guessArray.forEach((letter, i) => {
      if (result[i] !== "correct" && letterCount[letter] > 0) {
        result[i] = "present";
        letterCount[letter]--;
      }
    });

    return result;
  }

  makeGuess(guess) {
    if (this.isGameOver) return null;
    if (guess.length !== this.cols) return "Not enough letters";
    if (!isValidWord(guess)) return "Word not in list";

    const result = this.checkGuess(guess);
    this.guesses[this.currentRow] = { word: guess, result };
    
    if (guess === this.solution) {
      this.stats.gamesWon++;
      this.stats.currentStreak++;
      this.stats.maxStreak = Math.max(this.stats.maxStreak, this.stats.currentStreak);
      this.stats.gamesPlayed++;
      this.isGameOver = true;
      this.saveStats();
      return "win";
    }
    
    if (this.currentRow === this.rows - 1) {
      this.stats.currentStreak = 0;
      this.stats.gamesPlayed++;
      this.isGameOver = true;
      this.saveStats();
      return `Game Over! The word was ${this.solution} (${getWordMeaning(this.solution)})`;
    }
    
    this.currentRow++;
    return result;
  }

  reset() {
    const now = new Date().getTime();
    if (!this.stats.lastGame || now - this.stats.lastGame > 3600000) {
      this.stats.lastGame = now;
      this.saveStats();
    }
    
    this.solution = getRandomWord();
    this.currentRow = 0;
    this.currentTile = 0;
    this.isGameOver = false;
    this.guesses = [];
    console.log("New solution:", this.solution);
  }
} 