import sys
import os

def main():
    print('Welcome to Codenames')
    blu = input('Please input BLUE words (Space Separated): ').split(' ')
    red = input('Please input RED words (Space Separated): ').split(' ')
    black = input('Please input BLACK card: ')
    neu = input('Please input NEUTRAL words (Space Separated): ')
    while True:
        color = input('Which team is the bot playing for? (blue/red): ')
        if color == 'red' or color == 'blue':
            break;
        else:
            print('Invalid Input')

    bot_turn = False
    if (len(blu) > len(red)):
        if color == 'blue':
            bot_turn = True
    if (len(red) > len(blu)):
        if color == 'red':
            bot_turn = True
    game_over = False 
    while not game_over:
        print('Current Board')
        print('Blue: ' + str(blu))
        print('Red: ' + str(red))
        print('Black: ' + black + '\n');
        if bot_turn:
            print('Bots turn!')
            print("Bot is generating hint...")
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
                    
main()
