class WordleUI {
  constructor() {
    this.game = new WordleGame();
    this.board = document.getElementById("board");
    this.keyboard = document.getElementById("keyboard");
    this.message = document.getElementById("message");
    this.resetButton = document.getElementById("resetButton");
    this.hintButton = document.getElementById("hintButton");
    
    this.createBoard();
    this.createKeyboard();
    this.setupEventListeners();
    this.updateStats();
    this.setupPopup();
  }

  createBoard() {
    this.board.innerHTML = "";
    for (let r = 0; r < this.game.rows; r++) {
      const row = document.createElement("div");
      row.classList.add("row");
      for (let c = 0; c < this.game.cols; c++) {
        const tile = document.createElement("div");
        tile.classList.add("tile");
        tile.setAttribute("id", `tile-${r}-${c}`);
        row.appendChild(tile);
      }
      this.board.appendChild(row);
    }
  }

  createKeyboard() {
    const rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];
    this.keyboard.innerHTML = "";
    
    rows.forEach(row => {
      const rowDiv = document.createElement("div");
      rowDiv.classList.add("key-row");
      
      row.split("").forEach(letter => {
        const key = document.createElement("div");
        key.textContent = letter;
        key.classList.add("key");
        key.addEventListener("click", () => this.handleInput(letter));
        rowDiv.appendChild(key);
      });
      
      this.keyboard.appendChild(rowDiv);
    });

    // Add Enter and Delete keys
    const lastRow = document.createElement("div");
    lastRow.classList.add("key-row");
    
    ["Enter", "Delete"].forEach(key => {
      const keyDiv = document.createElement("div");
      keyDiv.textContent = key;
      keyDiv.classList.add("key", "wide");
      keyDiv.addEventListener("click", () => this.handleInput(key === "Delete" ? "Backspace" : key));
      lastRow.appendChild(keyDiv);
    });
    
    this.keyboard.appendChild(lastRow);
  }

  setupEventListeners() {
    document.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" || e.key === "Enter" || /^[a-zA-Z]$/.test(e.key)) {
        this.handleInput(e.key);
      }
    });

    if (this.hintButton) {
      this.hintButton.addEventListener("click", () => {
        const hint = getHint(this.game.solution);
        this.showMessage(`Hint: ${hint}`);
      });
    }

    this.resetButton.addEventListener("click", () => {
      this.game.reset();
      this.createBoard();
      this.createKeyboard();
      this.updateStats();
    });
  }

  setupPopup() {
    const newGameButton = document.getElementById("newGameButton");
    const exitButton = document.getElementById("exitButton");

    newGameButton.addEventListener("click", () => {
      document.getElementById("popup").classList.add("hidden");
      this.game.reset();
      this.createBoard();
      this.createKeyboard();
      this.updateStats();
    });

    exitButton.addEventListener("click", () => {
      window.location.reload();
    });
  }

  animateGuess(result, rowIndex) {
    result.forEach((status, i) => {
      const tile = document.getElementById(`tile-${rowIndex}-${i}`);
      setTimeout(() => {
        tile.classList.add("flip");
        setTimeout(() => {
          tile.classList.add(status);
        }, 250);
      }, i * 200);
    });
    
    setTimeout(() => this.updateKeyboardColors(), result.length * 200);
  }

  updateKeyboardColors() {
    const keyElements = document.querySelectorAll(".key");
    const letterStates = new Map();

    this.game.guesses.forEach(guess => {
      // Only process entries that are complete objects with a word property.
      if (guess && typeof guess === "object" && guess.word) {
        guess.word.split("").forEach((letter, i) => {
          const currentState = letterStates.get(letter) || "absent";
          const newState = guess.result[i];
          if (newState === "correct" || 
              (newState === "present" && currentState === "absent")) {
            letterStates.set(letter, newState);
          }
        });
      }
    });

    keyElements.forEach(key => {
      const letter = key.textContent.toLowerCase();
      const state = letterStates.get(letter);
      if (state) {
        key.style.backgroundColor = state === "correct" ? "#6aaa64" : 
                                  state === "present" ? "#c9b458" : "#3a3a3c";
      }
    });
  }

  showMessage(msg) {
    this.message.innerHTML = `<span>${msg}</span>`;
    this.message.classList.add("visible");
    setTimeout(() => {
      this.message.classList.remove("visible");
    }, 2000);
  }

  updateStats() {
    document.getElementById("gamesPlayed").textContent = this.game.stats.gamesPlayed;
    document.getElementById("winPercentage").textContent = 
      this.game.stats.gamesPlayed ? 
      Math.round((this.game.stats.gamesWon / this.game.stats.gamesPlayed) * 100) + "%" : 
      "0%";
    document.getElementById("currentStreak").textContent = this.game.stats.currentStreak;
    document.getElementById("maxStreak").textContent = this.game.stats.maxStreak;
  }

  showPopup(title, scoreInfo) {
    const popup = document.getElementById("popup");
    const resultTitle = document.getElementById("resultTitle");
    const scoreInfoDiv = document.getElementById("scoreInfo");

    resultTitle.textContent = title;
    scoreInfoDiv.innerHTML = scoreInfo;
    popup.classList.remove("hidden");
  }

  handleInput(key) {
    if (this.game.isGameOver) return;
    
    if (key === "Backspace") {
      if (this.game.currentTile > 0) {
        this.game.currentTile--;
        const tile = document.getElementById(`tile-${this.game.currentRow}-${this.game.currentTile}`);
        tile.textContent = "";
        tile.classList.add("pop");
        setTimeout(() => tile.classList.remove("pop"), 100);
        if (this.game.guesses[this.game.currentRow]) {
          this.game.guesses[this.game.currentRow] = 
            this.game.guesses[this.game.currentRow].slice(0, -1);
        }
      }
    } else if (key === "Enter") {
      if (this.game.currentTile === this.game.cols) {
        const guess = this.game.guesses[this.game.currentRow];
        const result = this.game.makeGuess(guess);
        
        if (result === "win") {
          const finalResult = this.game.checkGuess(guess);
          this.animateGuess(finalResult, this.game.currentRow);
          this.updateKeyboardColors();
          this.updateStats();
          setTimeout(() => {
            const scoreHTML = `
              <p>Games Played: ${this.game.stats.gamesPlayed}</p>
              <p>Win Percentage: ${this.game.stats.gamesPlayed ? Math.round((this.game.stats.gamesWon/this.game.stats.gamesPlayed)*100) + "%" : "0%"}</p>
              <p>Current Streak: ${this.game.stats.currentStreak}</p>
              <p>Max Streak: ${this.game.stats.maxStreak}</p>
            `;
            this.showPopup("You win! 🎉", scoreHTML);
          }, this.game.cols * 200);
        } else if (result && result.includes("Game Over")) {
          const finalResult = this.game.checkGuess(guess);
          this.animateGuess(finalResult, this.game.currentRow);
          this.updateKeyboardColors();
          this.updateStats();
          setTimeout(() => {
            const scoreHTML = `
              <p>Games Played: ${this.game.stats.gamesPlayed}</p>
              <p>Win Percentage: ${this.game.stats.gamesPlayed ? Math.round((this.game.stats.gamesWon/this.game.stats.gamesPlayed)*100) + "%" : "0%"}</p>
              <p>Current Streak: ${this.game.stats.currentStreak}</p>
              <p>Max Streak: ${this.game.stats.maxStreak}</p>
            `;
            this.showPopup(result, scoreHTML);
          }, this.game.cols * 200);
        } else if (result && result.includes("not")) {
          this.showMessage(result);
          const row = this.board.children[this.game.currentRow];
          row.classList.add("shake");
          setTimeout(() => row.classList.remove("shake"), 500);
        } else if (Array.isArray(result)) {
          this.animateGuess(result, this.game.currentRow - 1);
          this.updateKeyboardColors();
          this.game.currentTile = 0;
        }
      } else {
        this.showMessage("Not enough letters");
      }
    } else if (this.game.currentTile < this.game.cols) {
      const tile = document.getElementById(`tile-${this.game.currentRow}-${this.game.currentTile}`);
      tile.textContent = key.toLowerCase();
      tile.classList.add("pop");
      setTimeout(() => tile.classList.remove("pop"), 100);
      
      if (!this.game.guesses[this.game.currentRow]) {
        this.game.guesses[this.game.currentRow] = "";
      }
      this.game.guesses[this.game.currentRow] += key.toLowerCase();
      this.game.currentTile++;
    }
  }
}

// Initialize the game once the word list is loaded
window.wordListPromise.then(() => {
    new WordleUI();
}); 