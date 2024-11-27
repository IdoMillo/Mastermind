# Mastermind Game

Mastermind is a classic puzzle game where the player tries to guess a secret code within a set number of attempts. This version of the game is built using Pygame.

## Game Features

- **Multiple Code Lengths**: Choose between 4, 5, or 6 digits for the secret code.
- **Mode Options**:
  - **Wordle Mode**: Feedback is place-sensitive, just like Wordle.
  - **Duplicates**: Allows repetitions in the code.
- **Sound Effects**: Various sounds for button clicks, key presses, and game events (winning and losing).
- **Instructions**: Detailed instructions available within the game.

## Installation

### Prerequisites

- Python 3.10.6
- Pygame library

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/MastermindGame.git
   ```
2. Navigate to the project directory:
   ```sh
   cd MastermindGame
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## How to Play

1. **Start the Game**: Run the game script.
   ```sh
   python game.py
   ```
2. **Main Menu**: Choose one of the options: Start Game, Settings, or Instructions.
3. **Settings**: Configure your preferences for the code length, duplicates, and Wordle mode.
4. **Gameplay**: Guess the secret code by entering digits. The game will provide feedback on your guesses:
   - `V` for correct digit in the correct position.
   - `*` for correct digit in the wrong position.
   - `_` for incorrect digit.
5. **Win/Loss**: Win by guessing the code within the allotted attempts. Lose if you run out of attempts.

## File Structure

- `game.py`: Main game script containing the game logic and Pygame setup.
- `constants.py`: File containing all the constant values used in the game.
- `game_classes.py`: File containing the class definitions used in the game, such as `Button`.
- `assets/`: Directory containing assets like fonts, images, and sounds.
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Pygame library
- Inspiration from the classic Mastermind game