# AI-based Tic Tac Toe Game 🤖🎮

### Intelligent Move Prediction with Multiple Difficulty Levels

---

## 📌 Overview

This project is an **AI-powered Tic Tac Toe game** developed as part of the *Artificial Intelligence Lab (CSE_412)* course.

The system allows a human player to compete against an intelligent AI opponent in both **3×3 and 5×5 game modes**, with varying difficulty levels. The AI adapts its strategy using algorithms ranging from basic logic to advanced decision-making techniques.

---

## 🎯 Project Objective

* Build an intelligent AI opponent capable of strategic gameplay
* Implement multiple difficulty levels (Easy, Medium, Hard)
* Demonstrate AI progression from simple logic to advanced prediction
* Provide an interactive and user-friendly gaming experience

---

## 🎮 Game Features

### 🧩 Game Modes

* **3×3 Board**

  * Classic Tic Tac Toe
  * Win condition: 3 in a row

* **5×5 Board**

  * Advanced gameplay
  * Win condition: 4 in a row

---

### 🧠 AI Difficulty Levels

* **Easy** → Basic/random moves
* **Medium** → Semi-strategic decisions
* **Hard** → Advanced AI (Minimax + optimization)

---

### 💡 User Features

* Interactive graphical interface
* Real-time move updates
* Score tracking system
* Replay option after each game
* Winning combination highlighting

---

## ⚙️ AI Algorithm Implementation

### 🔹 3×3 Tic Tac Toe

* Uses **Minimax Algorithm**
* Explores all possible game states
* Guarantees:

  * AI never loses
  * Always results in win or draw

**How it works:**

* Simulates all moves
* Assigns scores:

  * +1 → AI win
  * -1 → Player win
  * 0 → Draw
* Selects optimal move

---

### 🔹 5×5 Tic Tac Toe

Due to larger complexity, optimizations are applied:

#### ✅ Alpha-Beta Pruning

* Cuts unnecessary branches
* Improves performance

#### ✅ Depth Limiting

* Limits search depth (4–6 moves ahead)
* Ensures fast response time

#### ✅ Heuristic Evaluation

* Scores board based on patterns:

  * AI advantage → positive score
  * Player advantage → negative score

👉 This balances performance and intelligence effectively.

---

## 🖥️ User Interaction

### Input:

* Select board size (3×3 or 5×5)
* Choose difficulty level
* Click cells to play

### Output:

* Instant AI response
* Score updates
* Highlighted winning line
* Replay option

---

## 🎨 User Interface

* Designed using **HTML, CSS, and JavaScript**
* Responsive layout
* Smooth navigation between screens
* Modern UI with animations

---

## 🛠️ Technologies Used

* HTML
* CSS
* JavaScript
* AI Algorithms (Minimax, Alpha-Beta Pruning)
* Visual Studio Code

---

## ⚙️ How to Run

1. Clone the repository:

```
git clone https://github.com/isfak1537/ai-project.git
```

2. Open the project folder

3. Run:

* Open `index.html` in your browser

---

## 📊 Key Achievements

* Implemented intelligent AI opponent
* Supported multiple board sizes
* Optimized performance for complex gameplay
* Created interactive UI with smooth experience

---

## ⚠️ Limitations

* No online multiplayer support
* AI does not learn from past games
* Limited to predefined strategies

---

## 🔮 Future Improvements

* Online multiplayer mode
* AI learning from player behavior
* Neural-network-based AI
* Mobile app version

---



## 🎓 Academic Information

* Course: Artificial Intelligence Lab (CSE_412)
* Institution: Daffodil International University
* Instructor: Atiqur Rahman

---

## 📜 License

This project is developed for academic purposes.

---
