# Codenames Bot
An NLP Project by:
- James Reilly a.k.a. [James-Reilly](https://github.com/James-Reilly)
- Gregory Goh a.k.a. [ShinyTeeth](https://github.com/ShinyTeeth)
- Oliver Barnum a.k.a. [TheNextGuy32](https://github.com/TheNextGuy32)

## Prerequisites
- spaCy
- gensim
- WordNet
- Python 3

## Game Rules
https://czechgames.com/files/rules/codenames-rules-en.pdf

## Single Player Mode
`python train.py [-s]`

By default the single player mode uses the Twitter generator

To use the spacy generator pass the flag `-s`

This mode randomly generates a board and has you play as the bot's human teammate.
You get a +1 for every card you guess correctly and -1 for every one you guess incorrectly.
The bot will give you clues like 'sword 2', but in this mode you only guess one word per clue.

## Live Play Version
`python bot-play.py [-demo]`

To autofill the game use the flag `-demo`

This mode is used to play the physical copy of the game.
It allows the user to input the corresponding words into the program so the bot can generate clues.

## 

-----
Credits:
- Codenames Key Card Generator: https://goo.gl/E6Nvqc
