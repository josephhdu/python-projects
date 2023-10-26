#----------------------------------------------------
# Assignment 2, Task 2
# 
# Author: Joseph Du
# Collaborators: Zenan Kaminskas
#----------------------------------------------------

import random

class ScrabbleDict():

    # Initializes some varibles and creates dictionary from text file
    def __init__(self, size, filename):
        self.dict = {}
        self.size = size
        self.filename = filename

        # creates the dictionary
        file = open('scrabble5.txt', 'r')
        data = file.readlines()
        for line in data: # for loop to read text file contents
            line = line.strip('\n')
            key = line[:self.size]
            self.dict[key] = line

    def check(self, word):
        '''
        Checks if inputed word is in dictionary
        :word: a string that is a word
        :returns: True
        '''
        if word in self.dict.values():
            return True

    def getSize(self):
        """
        Returns the size of the dictionary
        :returns: value of the number of words in the dictionary
        """
        return len(self.dict.values())

    def getWords(self, letter):
        '''
        Uses the inputed letter and returns a list with all the words that have that letter as its first letter in the word
        :letter: a letter
        :returns: a list of words
        '''
        sortedList = []
        for i in self.dict.values(): # iterates through dictionary
            fLetter = i[0]
            if fLetter == letter: # Checks word for first letter
                sortedList.append(i)
        return sortedList

    def getWordSize(self):
        '''
        Returns the size of the word
        :returns: size of the word
        '''
        return self.size

    def returnDict(self):
        '''
        Returns the dictionary as a dictionary
        :returns: dictionary
        '''
        return self.dict

    def returnList(self):
        """
        Returns the dictionary as a list
        :returns: list
        """
        words = []
        for i in self.dict.values(): # iterates through dictionary to create list
            words.append(i)
        return words

    def randomWord(self):
        """
        Chooses a random word from the dictionary
        :returns: a random word
        """
        words = []
        for i in self.dict.values():
            words.append(i)
        word = random.choice(words) # choose random word
        return word

    def getMaskedWords(self, template):
        """
        Gets the list of possible words with the inputed template
        :template: incomplete word with *'s
        :returns: list of possible words that could fill in the *'s
        """
        wList = []
        words = self.returnList()

        for i in template.lower(): # makes the template a list
            wList.append(i)
        starNum = 0
        for i in wList: # iterates through the template
            if i != '*':
                if starNum > 0:
                    words = possibleWords
                index = wList.index(i)
                possibleWords = []
                for j in words: # goes through the words to check for possible words
                    if j[index] == i:
                        possibleWords.append(j)
                starNum += 1

        possibleWords = sorted(possibleWords)
        return possibleWords

    def getConstrainedWords(self, template, letters):
        """
        Uses the letters inputed to give possible words with the template
        :template: incomplete word with *'s
        :letters: list with letters
        :returns: list of possible words
        """

        wList = []
        words = self.returnList()

        for i in template.lower(): # makes the template a list
            wList.append(i)
        starNum = 0
        for i in wList: # iterates through the template
            if i != '*':
                if starNum > 0:
                    words = possibleWords
                index = wList.index(i)
                possibleWords = []
                for j in words: # goes through the words to check for possible words
                    if j[index] == i:
                        possibleWords.append(j)
                starNum += 1

        possibleWords = sorted(possibleWords)

        for i in wList: # iterates through template
            if i == '*': # checks for the *
                index = wList.index(i)
                possibleWords2 = []
                for j in possibleWords: # iterates through possible words
                    if j[index] in letters: # gives possible words with the letters
                        possibleWords2.append(j)
        
        return possibleWords2

if __name__ == '__main__':
    '''
    main function that is was used to test the class while buidling
    '''
    wordle = ScrabbleDict(5,'scrabble5.txt')
    print(wordle.randomWord())
    print(wordle.getMaskedWords('T**ER'))
    print(wordle.getConstrainedWords('t**er',['i','g']))