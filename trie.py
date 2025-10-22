# -*- coding: utf-8 -*-
"""
This class uses dictionaries to implement a trie data structure, where
words are stored in lowercase and includes typical operations for
insertion, deletion, searching, loading words from a file, and more.
The node's data members include the character stored in it, if the node
is a valid (end) of a word, and a dictionary containing character keys and 
node values of the next possible letters after the current node's character.
"""

class Node:
    def __init__(self, ch: str = "", isWord: bool = False):
        self.ch = ch # Character for the node
        self.isWord = isWord # True if node is end of string
        self.children = {} # Dictionary of character keys and node values

class Trie:
    """ A class for the Trie """
    def __init__ (self):
        self.root = Node() # Initialize root node
        self.count = 0 # Number of words in trie
    


    # Purpose: Retrieve all words from a file and insert them into the trie.
    # Params: Name of file to retrieve from.
    # Returns: True if operation is successful, false if not.
    def getFromFile(self, filename: str) -> bool:
        try:
            with open(filename, "r") as wordFile:
                allWords = wordFile.read().split() # Read all words from file and place into list
        except:
            return False # Opening file unsuccessful
        
        # Words must only contain letters and are lowercased to be inserted into trie
        for word in allWords:
            word = word.lower()
            if word.isalpha():
                self.insert(word)
        
        return True
    


    # Purpose: Insert new word into trie.
    # Params: String for word being added.
    # Returns: True if word successfully inserted, false if not.
    def insert(self, word: str) -> bool:
        curr = self.root

        for ch in word:
            ch = ch.lower()
            if not ch.isalpha():
                return False # Character must not contain non-letters
            
            # If no path exists for current character, create a new node for it
            if ch not in curr.children:
                curr.children[ch] = Node(ch)
            curr = curr.children[ch] # Traverse to next letter in sequence

        if curr.isWord:
            return False # Fails if word already exists
        
        curr.isWord = True # Mark last node as valid end of word
        self.count += 1 # Increment word count
        return True



    # Purpose: Search for word from parameter.
    # Params: String for word being searched.
    # Returns: True if word from parameter exists in trie.
    def search(self, word: str) -> bool:
        curr = self.root
        
        for ch in word:
            ch = ch.lower()
            if ch in curr.children:
                curr = curr.children[ch] # If path exists for current character, traverse to next node
            else:
                return False # Character not found in trie
        
        if curr.isWord:
            return True # Return true if final node is valid end of word
        return False
    


    # Purpose: Remove existing word from trie.
    # Params: String for word being removed.
    # Returns: True if word successfully removed, false if not.
    def remove(self, word: str) -> bool:
        if not self.search(word):
            return False # If word not found return false
        
        self._remove(self.root, word, 0) # Recursively remove word starting from root
    
        self.count -= 1 # Decrement word count
        return True



    # Purpose: Recursive helper function for remove() to delete nodes of removed word.
    # Params: Current node, word being removed, index of current character.
    # Returns: True if current node should be deleted, false if not.
    def _remove(self, curr, word: str, ind: int) -> bool:
        if ind == len(word):
            curr.isWord = False # Word being removed no longer valid
            if len(curr.children) == 0:
                return True # Last node should be removed if no children
            return False # If node has children not safe to delete
        
        ch = word[ind].lower()
        if ch not in curr.children:
            return False # Path invalid if character does not exist
        
        shouldRemove = self._remove(curr.children[ch], word, ind + 1) # Recursive call for next node in sequence
        if shouldRemove:
            del curr.children[ch] # Delete child node from current node's dictionary of children if safe to delete
        
        if len(curr.children) == 0 and not curr.isWord:
            return True # If current node has no children and is not a word then safe to delete
        return False # Otherwise keep it



    # Purpose: Remove all words from trie.
    # Params: None.
    # Returns: True after clearing trie.
    def clear(self) -> bool:
        self.root = Node() # Reset root node to empty
        self.count = 0 # Reset word count
        return True
    


    # Purpose: Return number of words currently stored in trie.
    # Params: None.
    # Returns: Number of words currently stored in trie.
    def wordCount(self) -> int:
        return self.count
    


    # Purpose: Builds and returns a vector of strings containing all words in trie.
    # Params: None.
    # Returns: Vector of strings containing all words in trie.
    def words(self) -> list[str]:
        allWords = []
        self._words(self.root, "", allWords) # Recursively retrieve words starting from root
        return sorted(allWords)



    # Purpose: Recursive helper function for words() to retrieve and store words from trie.
    # Params: Current node, string of word so far after recursive call, and list to store full words.
    # Returns: None (adds word to word list).
    def _words(self, curr, wordSoFar, wordList):
        if curr.isWord:
            wordList.append(wordSoFar) # Adds word to list if current node is valid end of word

        for ch in curr.children:
            child = curr.children[ch] # Traverse all child nodes
            self._words(child, wordSoFar + ch, wordList) # Add letter to word and call recursive function