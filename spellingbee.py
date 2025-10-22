# -*- coding: utf-8 -*-
"""
New York Times Spelling Bee
This project recreates New York Times' incredibly fun yet simple 
Spelling Bee game. The player's job and rules are as follows:
possible that are:
- Four letters long or longer
- Contains “central letter”
- May contain six “other letters”
- Allowed letters may be used more than once
- Words must exist in current word dictionary
- Player can make as many guesses as they wish when finding possible words 
The goal is to rack up as many points as possible by finding as many words 
as possible! The user can also achieve a pangram by finding a word that uses 
all seven valid letters, and a bingo by finding at least one word for all of 
the seven valid letters (so at seven words starting with each letter). Run 
and follow the program's commands for more information.
"""

from sbtrie import SBTrie 

# Purpose: Clear out existing word dictionary and create new dictionary using words from new file.
# Params: Name of file to process words contained in it.
# Returns: None (updates trie with all words from file).
def getNewDictionary(sbt, filename):
  sbt.clear()
  sbt.getFromFile(filename)



# Purpose: Add to existing word dictionary using words from new file.
# Params: Name of file to process words contained in it.
# Returns: None (updates trie with new words from file).
def updateDictionary(sbt, filename):
  sbt.getFromFile(filename)



# Purpose: Process user-inputted string of letters to be used in game, check for validity, and initialize central and other letters.
# Params: String of letters to be used in game.
# Returns: None (initializes trie data members)
def setupLetters(sbt, letters):
  allLetters = []
  for letter in letters:
    if letter.isalpha() and letter.lower() not in allLetters: # Non-letters and repeats are ignored
      allLetters.append(letter.lower()) # If user enters upper case letter convert to lower case and add it to list
  
  # If user enters seven unique letters, initialize trie's data members to start game
  if len(allLetters) == 7:
    sbt.centralLetter = allLetters[0]
    sbt.otherLetters = "".join(allLetters[1:])
    sbt.discoveredWords.clear()
    sbt.pangramFound = False
    sbt.bingoFound = False
    sbt.score = 0
  else:
    print("Invalid letter set") # If user does not enter seven unique letters display error message



# Purpose: Display current centeral letter and six other letters.
# Params: None.
# Returns: Print statements of central letter and six other letters.
def showLetters(sbt):
  print(f"Central Letter: {sbt.centralLetter}")
  print(f"6 Other Letters: {','.join(sbt.otherLetters)}")



# Purpose: Screens potential word from user to see if it's valid and updates points and prints corresponding messages if so.
# Params: Word that user entered to be checked.
# Returns: None (updates trie data members such as score, discoveredWords, pangramFound, and bingoFound depending on word).
def attemptWord(sbt, word):
  points = sbt.isNewSBWord(word) # Call to isNewSBWord() returns how many points earned

  # All reasons word can be invalid, if so print error message and return without updating data members
  if points == -1:
    print("word is too short")
    return
  elif points == -2:
    print("word is missing central letter")
    return
  elif points == -3:
    print("word contains invalid letter")
    return
  elif points == -4:
    print("word not in dictionary")
    return
  elif points == -5:
    print("word has already been found")
    return

  # If word survives validity screening, insert into discoveredWords and increment score by points earned
  sbt.discoveredWords.insert(word)
  sbt.score += points

  # Assigns singular or plural for word and total points message
  if points == 1:
    printPoint = "point"
  else:
    printPoint = "points"

  if sbt.score == 1:
    printTotal = "point"
  else:
    printTotal = "points"

  message = f"found {word} {points} {printPoint}, total {sbt.score} {printTotal}"

  # Concatenates message if word is pangram
  if sbt.isPangram(word):
    sbt.pangramFound = True
    message += ", Pangram found"

  # Concatenates message if user achieved bingo
  if sbt.hasBingo() and sbt.discoveredWords.count == 7:
    sbt.bingoFound = True
    message += ", Bingo scored"

  print(message)



# Purpose: Displays all words found and at the end, total word count, points earned, and if pangram and bingos were achieved.
# Params: None.
# Returns: None (prints messages containing information in purpose).
def showFoundWords(sbt):
  foundWords = sbt.getFoundWords()
  foundWords.sort()

  # Call to words() on discoveredWords returns a list to sort and print in alphabetical order
  for word in foundWords:
    print(word)
  
  # Assigns singular or plural for word and total points message
  if len(foundWords) == 1:
    printWord = "word"
  else:
    printWord = "words"

  if sbt.score == 1:
    printPoint = "point"
  else:
    printPoint = "points"

  message = f"{len(foundWords)} {printWord} found, total {sbt.score} {printPoint}"

  # Concatenates message if pangram or bingo achieved
  if sbt.pangramFound:
    message += ", Pangram found"
  if sbt.bingoFound:
    message += ", Bingo scored"

  print(message)



# Purpose: Prints message containing all possible Spelling Bee words from dictionary, their length, if word is pangram, and if a bingo is found with seven valid letters.
# Params: None.
# Returns: None (prints message containing all possible Spelling Bee words from dictionary).
def showAllWords(sbt):
  allWords = sbt.sbWords(sbt.centralLetter, sbt.otherLetters) # call to sbWords() on trie collects all words that are valid from using a combination of valid letters.
  allWords.sort()
  foundLetters = []

  for word in allWords:
    if len(word) > 17:
      line = f"{word} {len(word)}" # One space for words larger than seventeen letters
    else:
      line = f"{word}{' ' * (20 - len(word) - 1)}{len(word)}" # Align words for a right justified column of word lengths
    
    # Manually track for bingo (hasBingo function works only for discoveredWords trie)
    if word[0] not in foundLetters:
      foundLetters.append(word[0])

    # Check if word is pangram and add to message
    if sbt.isPangram(word):
      line += " Pangram"
    print(line)
  
  # Manual check for bingo (hasBingo function works only for discoveredWords trie)
  foundBingo = True
  for letter in sbt.getLetters():
     if letter not in foundLetters:
        foundBingo = False
        break
     
  if foundBingo:
     print("Bingo found")



# Purpose: Display all Spelling Bee game commands to user.
# Params: None.
# Returns: None (prints display menu of commands).
def displayCommands():
  print( "\nCommands are given by digits 1 through 9\n")
  print( "  1 <filename> - read in a new dictionary from a file")
  print( "  2 <filename> - update the existing dictionary with words from a file")
  print( "  3 <7letters> - enter a new central letter and 6 other letters")
  print( "  4            - display current central letter and other letters")
  print( "  5 <word>     - enter a potential word")
  print( "  6            - display found words and other stats")
  print( "  7            - list all possible Spelling Bee words from the dictionary")
  print( "  8            - display this list of commands")
  print( "  9            - quit the program")
  print()



# Purpose: Main function for Spelling Bee game.
# Params: None, requests info from user (described in command menu).
# Returns: None (interactive game with print messages in individual functions).
def spellingBee():
  print("Welcome to New York Times Spelling Bee Game!")
  
  sbt = SBTrie()

  displayCommands()

  while (True):
    line = input ("cmd> ")
    command = line[0]
    args = ""

    
    if(command == '1'):
        args = line[1:].strip()
        getNewDictionary(sbt, args)

    if(command == '2'):
        args = line[1:].strip()
        updateDictionary(sbt, args);
        
    if(command == '3'):
        args = line[1:].strip()
        setupLetters(sbt, args);

    if(command == '4'):
        showLetters(sbt);

    if(command == '5'):
        args = line[1:].strip()
        attemptWord(sbt, args);

    if(command == '6'):
        showFoundWords(sbt);

    if(command == '7'):
        showAllWords(sbt)

    if(command == '8' or command == '?'):
        displayCommands();
    
    if(command == '9' or command == 'q'):
        break
    
  return
  
spellingBee()