#----------------------------------------------------
# Assignment 2, Task 4 & 5
# 
# Author: Joseph Du
# Collaborators: Zenan Kaminskas
#----------------------------------------------------

# import module
from Wordle175 import ScrabbleDict

def hints():
    """
    Checks if user enters a proper template for their hint
    :returns: users inputed template and letters
    """
    valid = False
    while not valid: # while loop for template
        userInput = input('enter a template:')
        if len(userInput) == 5: # checks length
            sCounter = 0 
            for i in userInput:
                if i == '*':
                    sCounter += 1
            if sCounter > 0: # checks for at least one *
                print('valid input')
                valid2 = False
                while not valid2: # while loop for letters
                    input2 = input('(optional, just enter to skip)enter letters:')
                    if input2 == '':
                        valid2 = True
                        valid = True
                    lCount = 0 
                    letters = []
                    for i in input2: # makes letter list
                        letters.append(i)
                        lCount += 1
                    if lCount > 4: # checks for too many letters
                        print('invalid input')
                        valid2 = False
                    else:
                        valid2 = True
                        valid = True
            else:
                print('invalid input')
        else:
            print('invalid input')

    return userInput, letters

def percent(words):
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    pDict = {}
    for letter in alphabet:
        pDict[letter] = 0
    for letter in pDict:
        lNum = 0
        for word in words:
            for i in word:
                if letter == i:
                    lNum += 1
        pDict[letter] = lNum
    allLetters = len(words) * 5

    for letter in pDict:
        number = pDict[letter]
        percent = number/allLetters * 100
        pDict[letter] = [number, round(percent,2)]

    for letter in pDict:
        pct = pDict[letter][1]
        pct = int(round(pct,0))
        star = '*' * pct
        pDict[letter].append(star)

    return pDict

def main():
    wordle = ScrabbleDict(5,'scrabble5.txt')
    dictionary = wordle.returnList()
    pDict = percent(dictionary)
    for i in pDict:
        number = str(pDict[i][0])
        pct = str(pDict[i][1]) + '%'
        star = pDict[i][2]
        string = f'{i.upper()}: {number: >4}  {pct: <5}  {star}'
        print(string)
        
    input = hints()
    template = input[0]
    letters = input[1]
    wordle = ScrabbleDict(5,'scrabble5.txt')
    print(wordle.getMaskedWords(template))
    print(wordle.getConstrainedWords(template, letters))

main()