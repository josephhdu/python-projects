#----------------------------------------------------
# Assignment 2, Task 3
# 
# Author: Joseph Du
# Collaborators: Zenan Kaminskas
#----------------------------------------------------

# imported modules
from Wordle175 import ScrabbleDict
from clean import uncorrupt

def userInput(guessNum):
    """
    Asks the user for an input
    :guessNum: the number of the guess the user is on
    :returns: the users input
    """
    guessNum = str(guessNum)
    userGuess = input('Attempt ' + guessNum + ': Please enter a 5 five-letter word:')
    return userGuess

def validWord(word, wordList):
    """
    Checks if the user input is valid word
    :word: the users inputed word
    :wordList: the dictionary
    :returns: returns a string or boolean
    """
    if len(word) < 5:
        length = 'short'
        return length
    elif len(word) > 5:
        length = 'long'
        return length
    else:
        if word in wordList:
            return True
        else:
            return 'invalid'


def colours(guess, word):
    """
    Handles the green, orange, and red spaces of the words
    :guess: users guess as a list
    :word: the chosen random word as list
    :returns: green, orange, and red lists in a tuple
    """
    green = []
    orange = []
    red = []
    index = 0 

    # manages the green list
    for char in guess:
        if char[0] == word[index]:
            green.append(char.upper())
        index += 1

    # manages the orange list partially
    for char in guess:
        if char[0] in word:
            orange.append(char.upper())

    # manages the red list
    for char in guess:
        if char[0] not in word:
            red.append(char.upper())

    # fixes the orange list based on the green list
    orangeRemove = []
    for char in orange:
        if char in green:
            orangeRemove.append(char)
    for i in orangeRemove:
        orange.remove(i)
    
    # fixes the end condition issue
    if guess == word:
        green = []
        orange = []
        red = []
        for char in guess:
            green.append(char.upper())
        return(green, orange, red)

    return(green,orange,red)

def format(result, word):
    """
    Formats the outputs
    :results: green, orange, and red lists in a tuple
    :word: the randome chosen word
    :returns: formatted string
    """
    green = ', '.join(result[0])
    green = '{' + green + '}'
    orange = ', '.join(result[1])
    orange = '{' + orange + '}'
    red = ', '.join(result[2])
    red = '{' + red + '}'
    word = word.upper()
    
    string = f'{word} Green={green} - Orange={orange} - Red={red}'
    return string

# Main function
def main():
    
    uncorrupt() # creates the text file

    # initiates some varibles
    wordle = ScrabbleDict(5,'scrabble5.txt')
    word = wordle.randomWord()
    wordList = wordle.returnList()
    sameGuess = []
    guesses = 1 
    continueGame = True
    stringList = []
    print(word)

    # adds integers to duplicate letters
    guessList = []
    duplicate = 1
    for char in word:
        if char in guessList:
            index = word.index(char)
            guessList[index] = char + str(duplicate)
            duplicate += 1
            guessList.append(char + str(duplicate))
        elif char + str(1) in guessList:
            duplicate += 1
            guessList.append(char + str(duplicate))
        else:
            guessList.append(char)

    # game loop
    while continueGame:
        userGuess = userInput(guesses)
        validity = validWord(userGuess, wordList)

        # adds integers to duplicate letters
        userGuessList = []
        duplicate2 = 1
        for char in userGuess:
            if char in userGuessList:
                index2 = userGuess.index(char)
                userGuessList[index2] = char + str(duplicate2)
                duplicate2 += 1
                userGuessList.append(char + str(duplicate2))
            elif char + str(1) in userGuessList:
                duplicate2 += 1
                userGuessList.append(char + str(duplicate2))
            else:
                userGuessList.append(char)
        
        # for if the inputs are wrong
        if validity == 'short':
            print(userGuess.upper() + ' is too ' + validity)
        elif validity == 'long':
            print(userGuess.upper() + ' is too ' + validity)
        elif validity == 'invalid':
            print(userGuess.upper() + ' is not a recognized word')
        elif userGuess in sameGuess:
            print(userGuess.upper() + ' was already entered')
        # handles right input
        else:
            sameGuess.append(userGuess)

            result = colours(userGuessList, guessList)
            string = format(result, userGuess)
            stringList.append(string)
            for string in stringList:
                print(string)

            # game end conditions
            guesses += 1
            if guesses == 7:
                continueGame = False
                print('Sorry you lose. The word is ' + word.upper())
            elif userGuess == word:
                continueGame = False
                print('Found in ' + str(guesses - 1) + ' attempts. Well done. The Word is ' + word.upper())

main()