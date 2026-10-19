import random
import os

# ASCII Art stages for Hangman (0 to 6 mistakes)
HANGMAN_STAGES = [
    """
       ------
       |    |
            |
            |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
            |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
       |    |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|    |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      /     |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      / \\   |
            |
    ---------
    """
]

def load_words(filename="google-10000-english-no-swears.txt"):
    """
    Loads words from the local text file, filtering for valid alphabetic words.
    Falls back to a default list if the file is missing or inaccessible.
    """
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                # Filter for words that are purely alphabetic and at least 3 letters long
                words = [line.strip().lower() for line in file if line.strip().isalpha() and len(line.strip()) >= 3]
            if words:
                return words
        except Exception as e:
            print(f"Warning: Could not read '{filename}' ({e}). Using default word list.")
    
    # Fallback word list for testing if the text file isn't present
    return ["python", "developer", "internship", "programming", "console", "hangman", "variable", "function"]

def display_board(mistakes, secret_word, guessed_letters):
    """Displays the current game state: ASCII art, masked word, and guessed letters."""
    print("\n" + "=" * 45)
    print(HANGMAN_STAGES[mistakes])
    
    # Create the masked word representation (e.g., '_ a _ e')
    masked_word = " ".join([letter if letter in guessed_letters else "_" for letter in secret_word])
    print(f"Word: {masked_word}")
    
    # Display sorted unique guessed letters
    sorted_guesses = sorted(list(guessed_letters))
    print(f"Guessed Letters: {', '.join(sorted_guesses) if sorted_guesses else 'None'}")
    print(f"Attempts Remaining: {len(HANGMAN_STAGES) - 1 - mistakes}")
    print("=" * 45)

def play_hangman():
    """Core game loop implementing control flow, state management, and edge-case handling."""
    word_list = load_words()
    secret_word = random.choice(word_list)
    
    guessed_letters = set()
    mistakes = 0
    max_mistakes = len(HANGMAN_STAGES) - 1
    
    print("\nWelcome to the Hangman Word Guessing Game!")
    
    while mistakes < max_mistakes:
        display_board(mistakes, secret_word, guessed_letters)
        
        # Check for victory condition before requesting input
        if all(letter in guessed_letters for letter in secret_word):
            print(f"\n🎉 Congratulations! You successfully guessed the word: '{secret_word}'!")
            return

        # Prompt user input and strip whitespace/convert to lowercase
        guess = input("\nGuess a letter: ").strip().lower()
        
        # Edge Case 1: Check if input is empty or multiple characters
        if len(guess) != 1:
            print("❌ Invalid input: Please enter exactly a single alphabetical character.")
            continue
            
        # Edge Case 2: Check if input is non-alphabetical (numbers, symbols, spaces)
        if not guess.isalpha():
            print("❌ Invalid input: Numbers and symbols are not allowed. Enter a letter from a-z.")
            continue
            
        # Edge Case 3: Check if letter was already guessed (prevents duplicate penalty deduction)
        if guess in guessed_letters:
            print(f"⚠️ You already guessed '{guess}'. Try a different letter! (No penalty)")
            continue
            
        # Record valid guess
        guessed_letters.add(guess)
        
        # Process correctness of the guess
        if guess in secret_word:
            print(f"✅ Correct! '{guess}' is in the word.")
        else:
            mistakes += 1
            print(f"❌ Incorrect! '{guess}' is not in the word.")
            
    # Defeat Screen (Max mistakes reached)
    print("\n" + "=" * 45)
    print(HANGMAN_STAGES[max_mistakes])
    print("💀 Game Over! You ran out of attempts.")
    print(f"The hidden word was: '{secret_word}'")
    print("=" * 45)

if __name__ == "__main__":
    # Outer loop allowing multiple game sessions without restarting the terminal script
    while True:
        play_hangman()
        replay = input("\nWould you like to play another round? (y/n): ").strip().lower()
        if replay != 'y':
            print("Thank you for playing! Best of luck!")
            break