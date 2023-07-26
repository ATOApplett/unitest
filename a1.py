"""
Wordle
Assignment 1
Semester 1, 2022
CSSE1001/CSSE7030
"""

from string import ascii_lowercase
from typing import Optional

from a1_support import (
    load_words,
    choose_word,
    VOCAB_FILE,
    ANSWERS_FILE,
    CORRECT,
    MISPLACED,
    INCORRECT,
    UNSEEN,
)


# Replace these <strings> with your name, student number and email address.
__author__ = "Alex Ong, s4744131"
__email__ = "<alex.ong@uqconnect.edu.au>"


# Add your functions here (# Add comments when finished)

def main():
    guesses = 1
    vocab = load_words("vocab.txt")
    answer_lib = load_words("answers.txt")
    answer = choose_word(answer_lib)
    new_vocab = vocab
    history = []
    stats = [0, 0, 0, 0, 0, 0, 0]
    while True:
        guess = prompt_user(guesses, vocab)
        if guess == 'h':
            print("Ah, you need help? Unfortunate.")
        elif guess == 'k':
            print_keyboard(history)    
        elif guess == 'q':
            break
        elif guess == 'Invalid! Guess must be of length 6':
            guesses = guesses
        elif guess == 'Invalid! Unknown word':
            guesses = guesses
        else:
            if has_won(guess, answer) == True:
                print("Congratulations! You won in "+str(guesses)+" guesses!")
                stats[guesses-1] += 1
                print_stats(stats)
                again = input("Would you like to play again (y/n)?")
                again = again.lower()
                if str(again) == 'y':
                    guesses = 1
                    history = []
                    answer_lib = remove_word(answer_lib, answer)
                    answer = choose_word(answer_lib)
                elif str(again) == 'n':
                    break
                else:
                    break
            elif has_lost(guesses) == True:
                print("You lose! The answer was: "+answer)
                stats[6] += 1
                print_stats(stats)
                again = input("Would you like to play again (y/n)?")
                again = again.lower()
                if str(again) == 'y':
                    guesses = 1
                    history = []
                    answer_lib = remove_word(answer_lib, answer)
                    answer = choose_word(answer_lib)
                elif str(again) == 'n':
                    break
                else:
                    break
            elif has_won(guess, answer) == False:
                guesses += 1
                history = update_history(history, guess, answer)
                print_history(history)
                
            
def process_guess(guess: str, answer: str):
    '''
    Determines where letters of the guess are in relation to the answer

    Parameters:
        guess(str): The guess being checked

    Returns:
        (str): Places a '⬛' if not in the answer, '🟨' if misplaced, and '🟩' if correct
    '''
    answer_list = []
    guess_list = []
    for char in answer:
        answer_list.append(char)
    for char in guess:
        guess_list.append(char)
    #creates a list of individual characters for the guess and current answer
    check = 0
    guessed = []
    for i in range(6):
        if guess_list[check] == answer_list[check]:
            guessed.append(CORRECT)
            answer_list[check] = ' ' #prevents 'misplaced' form appearing if the user enters a word containing double letters
            check += 1
        elif guess_list[check] in answer_list:
            guessed.append(MISPLACED)
            index_a = answer_list.index(guess_list[check])
            answer_list[index_a] = ' ' #prevents 'misplaced' form appearing if the user enters a word containing double letters
            check += 1
        else:
            guessed.append(INCORRECT)
            check += 1
    guessed = ' '.join(map(str, guessed)) #turns the boxes into a string
    guessed = guessed.replace(" ", "") #removes all spaces in the string
    return guessed


def remove_word(answer_lib: tuple[str, ...], answer: str):
    '''
    Removes an item from a list with that item in it

    Parameters:
        answer_lib(tuple): A tuple containing all possible answers
        answer(str): The word being removed from answer_lib

    Returns:
        (tuple): A tuple containing all possible answers excluding ones from previous games
    '''
    index = answer_lib.index(answer) #determines where the answer is in the list of possible answers
    new_answer = answer_lib[:index] + answer_lib[index+1:] #removes the answer from the possible list of answers
    return new_answer


def update_history(history: tuple[tuple[str, str], ...], guess: str, answer: str):
    '''
    Updates the current history by storing the current guess

    Parameters:
        history(tuple): a tuple containing previous and current guesses
        guess(str): the word that will be stored in the history
        answer(str): the current answer the user is trying to guess

    Returns:
        (tuple): a tuple with the current guess inside of it as well as previous guesses
    '''
    his_one = process_guess(guess, answer)
    history_list = list(history)
    history_list.append((guess, his_one))
    history = tuple(history_list)
    return history

def print_history(history: tuple[tuple[str, str], ...]):
    '''
    Prints the history in an ordered way

    Parameters:
        history(tuple): a tuple containing previous and current guesses

    Returns:
        (str): A string with the guess number and the word guessed for that guess number
    '''
    count = 1
    start = 0
    end = 12
    start_l = 0
    end_l = 6
    history = list(history)
    word = []
    location = []
    for i, k in history: #appends the words into one list and the locations for them in another list
        word.append(i)
        location.append(k)
    word = ' '.join(map(str, word))
    word = word.replace(" ", "")
    word = word.replace("", " ")
    location = ' '.join(map(str, location))
    location = location.replace(" ", "")
    for i in range(0, len(history)):
        print("---------------\nGuess "+str(count)+": "+word[start:end])
        print("         "+location[start_l:end_l])
        count += 1
        start += 12
        end += 12
        start_l += 6
        end_l += 6
    print("---------------\n")    

def print_keyboard(history: tuple[tuple[str, str], ...]):
    '''
    Prints the keyboard in an ordered manner

    Parameters:
        history(tuple): a tuple containing previous and current guesses

    Returns:
        (dict): A dictionary with the currently known letters
    '''
    keyboard_dict = {1: UNSEEN, 2: UNSEEN, 3: UNSEEN, 4: UNSEEN, 5: UNSEEN, 6: UNSEEN, 7: UNSEEN, 8: UNSEEN, 9: UNSEEN, 10: UNSEEN, 11: UNSEEN, 12: UNSEEN, 13: UNSEEN, 14: UNSEEN, 15: UNSEEN, 16: UNSEEN, 17: UNSEEN, 18: UNSEEN,  19: UNSEEN,  20: UNSEEN,  21: UNSEEN, 22: UNSEEN,  23: UNSEEN, 24: UNSEEN,  25: UNSEEN, 26: UNSEEN}
    words = []
    location = []
    for i, k in history: #appends the words into one list and the locations for them in another list
        words.append(i)
        location.append(k)
    words = ' '.join(map(str, words))
    words = words.replace(" ", "")
    location = ' '.join(map(str, location))
    location = location.replace(" ", "")
    count = 0
    for char in words:
        if location[count] == CORRECT:
            correct = ord(words[count])-96 #determines the dictionary key number to replace
            keyboard_dict[correct] = CORRECT
            count += 1
        elif location[count] == MISPLACED:
            correct = ord(words[count])-96
            keyboard_dict[correct] = MISPLACED
            count += 1
        elif location[count] == INCORRECT:
            correct = ord(words[count])-96
            keyboard_dict[correct] = INCORRECT
            count += 1
    print("\nKeyboard information\n------------")
    for a in range(0, len(keyboard_dict), 2): #prints the keyboard layout two at a time
        print(chr(a+97)+": "+keyboard_dict[a+1]+"\t"+chr(a+98)+": "+keyboard_dict[a+2])
    print("")

def print_stats(stats: tuple[int, ...]):
    '''
    Prints the current game stats 

    Parameters:
        stats(tuple): a tuple containing the amount of times won in a certain amount of guesses and the amount of times lost

    Returns:
        (tuple): A tuple seperated by a new line each time of games won and lost
    '''
    print("\nGames won in:")
    for numbers in range(6):
        print(str(numbers+1)+" moves: "+str(stats[numbers]))
    print("Games lost: "+str(stats[6]))
          
def prompt_user(guesses: int, vocab: tuple[str, ...]):
    '''
    Prompts the user for a valid input/guess or command

    Parameters:
        guesses(int): the guess the user is currently on
        vocab(tuple): a tuple containing all of the possible valid guesses the user can make

    Returns:
        (str): a string with the guess or command the user has inputted
    '''
    guess_input = input("Enter guess "+str(guesses)+": ")
    guess_input = guess_input.lower()
    if str(guess_input) == 'h':
        return guess_input
    elif str(guess_input) == 'k':
        return guess_input
    elif str(guess_input) == 'q':
        return guess_input
    elif guess_input not in vocab and (len(guess_input)<6 or len(guess_input)>6):
        print('Invalid! Guess must be of length 6')
        return 'answer'
    elif guess_input not in vocab:
        print('Invalid! Unknown word')
        return 'python'
    else:
        return guess_input
            
def has_won(guess: str, answer: str):
    '''
    Determines if the user's guess matches with the answer

    Parameters:
        guess(str): the word being checked
        answer(str): the current answer to the wordle

    Returns:
        (bool): True if the guess matches the answer, False if the guess does not
    '''
    if guess == answer:
        return True
    else:
        return False

def has_lost(guesses: int):
    '''
    Determines if the user's guesses exceeds a certain amount of guesses

    Parameters:
        guesses(int): the amount of guesses the user has had

    Returns:
        (bool): True if the amount of guesses exceeds 6, False if it does not
    '''
    if guesses>=6:
        return True
    elif guesses<6:
        return False

if __name__ == "__main__":
    main()
 

                           

