# 🐝 New York Times Spelling Bee (Python)

A command-line recreation of the **New York Times Spelling Bee** game, built in Python using a **Trie data structure** for efficient word storage, lookup, and validation.

## 🎯 Overview
This project replicates the gameplay and logic of the NYT Spelling Bee, where players must form as many valid words as possible using seven given letters: one **central letter** and six **outer letters**.  

Each word must:
- Be at least **4 letters long**
- Contain the **central letter**
- Use only the **seven allowed letters** (repeats are allowed)
- Exist in the **dictionary file**  

Players earn points for each valid word and can achieve:
- **Pangram** — a word using all seven letters  
- **Bingo** — at least one word found starting with each of the seven letters  

---

## 🧠 Features
- **Trie-based word dictionary** for fast insertion, lookup, and validation  
- **Dynamic scoring system** that awards points by word length and bonuses for pangrams  
- **Interactive command-line interface** for managing gameplay and commands  
- **Automatic tracking** of pangram and bingo achievements  
- **Support for custom dictionary files** (e.g., `words.txt`)  

---

## 🧩 Example Commands
Once you run the program, use these commands during gameplay:

| Command | Description |
|----------|-------------|
| `1 <filename>` | Load a new dictionary file |
| `2 <filename>` | Add more words to existing dictionary |
| `3 <7letters>` | Set a new central and outer letter set |
| `4` | Display current letters |
| `5 <word>` | Submit a word guess |
| `6` | Show all found words and current score |
| `7` | List all possible valid words from dictionary |
| `8` | Display command list |
| `9` | Quit game |

---

## 🏗️ Implementation Details
- Built with **Python**
- Core data structure: **Trie** (`Trie` and `SBTrie` classes)
- Recursive traversal for word validation, prefix matching, and filtering by rules
- Game logic organized through functions (dictionary loading, scoring, display, etc.)

---
