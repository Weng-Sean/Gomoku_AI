# Gomoku_AI

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Project Structure](#project-structure)

## Introduction

Gomoku, also known as Five in a Row, is a classic strategy board game where two players take turns placing their pieces on a grid. The objective is to be the first to form an unbroken chain of five of your pieces horizontally, vertically, or diagonally on the board.

This project is an implementation of the Gomoku game using Python and the Pygame library. It supports various gameplay modes, including human vs. human, human vs. AI, AI vs. human, and AI vs. AI. The project also features a graphical user interface (GUI) to provide an interactive gaming experience.

## Features

- Multiple gameplay modes:
  - Human vs. Human
  - Human vs. AI
  - AI vs. Human
  - AI vs. AI
- Interactive graphical user interface (GUI) for easy gameplay.
- An AI opponent powered by decision-making algorithms.
- Visual representation of the game board with a grid and player pieces.
- Option to start a new game or return to the main menu after a game is finished.

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone this repository to your local machine:
   git clone https://github.com/your-username/gomoku-game.git
2. Clone this repository to your local machine:
   ```cd gomoku-game```
3. Install the required dependencies, including Pygame:
   ```pip install pygame```

## How to Play

1. Run the game by executing the following command:
   ```python py_game.py```
2. The game will start with a main menu where you can choose your gameplay mode.
3. In the game, click on the grid cells to make your moves.
4. Follow the on-screen instructions to play the game.
5. After the game is over, you can choose to play again or return to the main menu.


## Project Structure

The project files are organized as follows:

- main.py: The main Python script that launches the Gomoku game and handles user interactions.
- AI.py: Contains the AI player logic, which determines the AI's moves.
- decision_tree_v2.py: Implementation of the decision tree used by the AI player.
- board.py: Defines the Board class, which represents the game board and its state.
