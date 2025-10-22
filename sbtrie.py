# -*- coding: utf-8 -*-
"""
SBTrie inherits from Trie class and adds functionality for the 
New York Times' Spelling Bee game. It contains additional functions
for implementing rules and functionalities for the game, such as
retrieving letters to be used, point system, checking if words are
pangrams, and if user got a bingo. Additional data members for the
central letter, other six letters, a trie for discovered words by user,
and if pangrams and bingos were found.
"""

from trie import Trie

class SBTrie(Trie):
    """ A class for the Spelling Bee Trie """
    def __init__ (self):
        super().__init__()
        self.centralLetter = "" # Central letter (required letter for all new words)
        self.otherLetters = "" # Other six letters that can be used in all new words
        self.discoveredWords = Trie() # Trie that stores words found by user
        self.score = 0 # Total score based on all new words found
        self.pangramFound = False # If pangram discovered (new word contains all seven letters)
        self.bingoFound = False # If bingo achieved (every letter has a word found by user)
    


    # Purpose: Insert found word into trie of discovered words.
    # Params: Word that was discovered by user.
    # Returns: None (inserts found word into trie of discovered words).
    def addFoundWord(self, word: str):
        self.discoveredWords.insert(word)



    # Purpose: Return a string of seven characters where first character is central letter
    # and next six are other letters in alphabetical order.
    # Params: None
    # Returns: String of all seven letters.
    def getLetters (self) -> str:
        others = "".join(sorted(self.otherLetters)) # Convert letters into list, sort alphabetically, then join together into string
        return self.centralLetter + others # Returns string with central letter concatenated to front



    # Purpose: Point system function for determining how many points user gets from potential word.
    # Params: Word that user is adding.
    # Returns: Number of points earned from word (negatives indicate error in word).
    def isNewSBWord (self, word: str) -> int:
        points = 0

        if len(word) < 4:
            return -1 # Word is too short (length must be at least four)
    
        if self.centralLetter not in word:
            return -2 # Word is missing central letter (must contain it)
        
        for ch in word:
            if ch not in self.getLetters():
                return -3 # Word contains at least one invalid letter (not one of the seven letters)
            
        if not self.search(word):
            return -4 # Word is not in dictionary (invalid word)
        
        if self.discoveredWords.search(word):
            return -5 # Word already found by user
        
        if len(word) == 4:
            points = 1 # User earns one point for a four letter word
        elif len(word) > 4:
            points = len(word) # User earns points equivalent to length of word for any word more than four letters
        
        if self.isPangram(word):
            points += 7 # User earns seven additional points if word is pangram (contains all seven letters)

        return points



    # Purpose: Determines if word contains all seven current letters and no invalid letters.
    # Params: Word that user is adding.
    # Returns: True if word contains all seven current letters and no invalid letters, false if not.
    def isPangram (self, word: str) -> bool:
        letters = self.getLetters()

        # If any letter in word is not one of seven valid letters return false
        for ch in word:
            if ch not in letters:
                return False
        
        # If at least one of seven valid letters is not present in word return false
        for ch in letters:
            if ch not in word:
                return False
        
        return True
    


    # Purpose: Determines if user has achieved a bingo (at least one word has been found for each of the seven letters)
    # Params: None.
    # Returns: True if at least one word has been found for each of the seven letters, false if not.
    def hasBingo (self) -> bool:
        letters = self.getLetters()
        rootChildren = self.discoveredWords.root.children # Root node's children contains first letters of all found words

        # Check root node's children if user found at least one word for all seven letters 
        for ch in letters:
            if ch not in rootChildren:
                return False # Return false if at least one of seven valid letters is not present
        
        return True



    # Purpose: Returns a list of all words that have been found.
    # Params: None.
    # Returns: List of all words that have been found.
    def getFoundWords (self) -> list[str]:
        return self.discoveredWords.words() # Call words() function from Trie superclass to do all the work



    # Purpose: Build a list of strings containing all words in trie that meet criteria of Spelling Bee game.
    # Params: String for central letter, string for other six letters.
    # Returns: List of strings containing all words in trie that are at least four letters long, 
    # contains central letter, and does not contain letters outside of the seven valid letters.
    def sbWords(self, centralLetter: str, otherLetters: str) -> list[str]:
        foundWords = []
        validLetters = self.getLetters();
        self._sbWords(self.root, "", validLetters, foundWords) # Recursively collect all valid words starting from root
        return foundWords



    # Purpose: Recursively traverse trie to collect all words that meet criteria of Spelling Bee game.
    # Params: Current node, string of word so far after recursive call, string of seven valid letters, list to store all valid words found.
    # Returns: None (adds words to word list)
    def _sbWords(self, curr, wordSoFar, letters, wordList):
        if len(wordSoFar) >= 4 and letters[0] in wordSoFar and curr.isWord:
            wordList.append(wordSoFar) # If word is at least four letters, contains central word, and is a valid word add to list
        
        # Depth-first search for all potential paths
        for ch in curr.children:
            if ch in letters: # Only traverse to paths that use one of seven valid letters
                self._sbWords(curr.children[ch], wordSoFar + ch, letters, wordList) # Add letter to word so far and recursively call function again