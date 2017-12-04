import sys
import random
import os
from spacyHint import SpacyClassifier
from twitterPredictor import TwitterPredictor
from bot import Bot 
import keyCardReader


def pick_bot(bot_type):
    if (bot_type == 'spacy'):
        return SpacyClassifier()
    elif (bot_type == 'twitter'):
        return TwitterPredictor()
        

def start(blu, red, black, neu, bot_type, color):
    bot_turn = False
    if (len(blu) > len(red)):
        if color == 'blue':
            bot_turn = True
    if (len(red) > len(blu)):
        if color == 'red':
            bot_turn = True
    bot = Bot(color, pick_bot(bot_type) )
    game_over = False 
    while not game_over:
        print('Current Board')
        print('Blue: ' + str(blu))
        print('Red: ' + str(red))
        print('Black: ' + black + '\n');
        if bot_turn:
            print('Bots turn!')
            print("Bot is generating hint...")
            print(bot.generate_hint(blu, red, black, neu))
            # Get hint
        else:
            print("Human player's turn!")
        guess = input('\nSpace separated words guessed (Space separated): ').split(' ')
        dumb = False
        for g in guess:
            try:
                blu.remove(g)
            except ValueError:
                dumb = False
            try:
                red.remove(g)
            except ValueError:
                dumb = False
            if g == black:
                bot_turn = not bot_turn
                game_over = True
                break;
        if len(red) == 0 or len(blu) == 0 or game_over:
            break;
        bot_turn = not bot_turn
        os.system('cls' if os.name == 'nt' else 'clear')

    if bot_turn:
        print('BOT WINS')
    else:
        print('HUMAN WINS')

def createBoard(codenames):
    longestWordLength = 1
    board = [""] * 25 
    freeCodename = [1]  * len(codenames)
    for i in range(25):
        while 1:
            codenameIndex = int(random.random()*(len(codenames)))   
            if freeCodename[codenameIndex]:
                board[i] = codenames[codenameIndex]
                longestWordLength = max(longestWordLength,len(board[i]))
                freeCodename[codenameIndex] = 0
                break
    return (board,longestWordLength)

def get_card_input():
    if (len(sys.argv) == 2 and sys.argv[1] == "-demo"):
        #  Read in the codenames
        codenameFile = open("codenameList.txt",'r')
        codenames = codenameFile.readlines()
        codenameFile.close()

        #  Parse the codenames
        codenameSentences = []
        for c in range(len(codenames)):
            codename = codenames[c] = codenames[c].strip()

            codenameSentences.append([codename])
            codenames[c] = codename

        #  Read in the keycards
        keyCards = keyCardReader.readFromFile()
        board, longestWordLength = createBoard(codenames)
        keyCard = keyCards[int(random.random()*(len(keyCards)))]
        blu = []
        red = []
        black = ''
        neu = []
        for i in range(len(keyCard)):
            if keyCard[i] == 3:
                black = board[i]
            elif keyCard[i] == 2:
                red.append(board[i])
            elif keyCard[i] == 1:
                blu.append(board[i])
            else:
                neu.append(board[i])

    else:
        blu = input('Please input BLUE words (Space Separated): ').split(' ')
        red = input('Please input RED words (Space Separated): ').split(' ')
        black = input('Please input BLACK card: ')
        neu = input('Please input NEUTRAL words (Space Separated): ').split(' ')

    return blu, red, black, neu

def main():
    print('Welcome to Codenames')
    bot_type = input ('Select predictor type (spacy, twitter, wiki): ')
    blu, red, black, neu = get_card_input()
    while True:
        color = input('Which team is the bot playing for? (blue/red): ')
        if color == 'red' or color == 'blue':
            break;
        else:
            print('Invalid Input')
    start(blu, red, black, neu, bot_type, color)


if __name__ == "__main__":
    main()
