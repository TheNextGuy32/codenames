import os
import sys
import random
import datetime
import hint
import keyCardReader
from twitterPredictor import TwitterPredictor
from spacyHint import SpacyClassifier

model_type = "t"
if len(sys.argv) > 1:
    if sys.argv[1] == "-s":
        model_type = "s"

#  Read in the codenames
codenameFile = open("codenameList.txt",'r')
codenames = codenameFile.readlines()
codenameFile.close()

random.seed()

#  Parse the codenames
codenameSentences = []
for c in range(len(codenames)):
    codename = codenames[c] = codenames[c].strip()

    codenameSentences.append([codename])
    codenames[c] = codename

#  Read in the keycards
keyCards = keyCardReader.readFromFile()

#  Update this to keep our output straight
versionNumber = "0.1"
guesses = []
    
# trainedModelFile = "MODEL_FILE.txt"
# model = Word2Vec.load(trainedModelFile)
# print(c.most_similar('money', topn=5))

def createBoard():
    longestWordLength = 1
    board = [""] * 25 
    freeCodename = [1]  * len(codenames)
    for i in range(25):
        while 1:
            codenameIndex = random.randrange(len(codenames))
            if freeCodename[codenameIndex]:
                board[i] = codenames[codenameIndex]
                longestWordLength = max(longestWordLength,len(board[i]))
                freeCodename[codenameIndex] = 0
                break
    return (board,longestWordLength)

def printBoard(board, longestWordLength):
    #  Title spacing
    spacing = 3
    boardLength = (longestWordLength * 5) + (spacing*3)
    boardTitle = "====  Codenames  ====="
    titleSpaces = int((boardLength/2) - (len(boardTitle)/2))
    print("%s%s"%(titleSpaces*' ',boardTitle))

    #  Print codenames
    for c in range(len(board)):
        if int(c % 5) == 0 and c != 0:
            print("")
        numberSpaces = longestWordLength - len(board[c])
        spaces = (numberSpaces+spacing) * ' '
        print("%s%s" % (board[c],spaces), end='')
    
    print("")

def isGameComplete(board):
    blueFound = 0 
    redFound = 0
    for codename in board:
        blueFound += codename == "BLU"
        redFound += codename == "RED"
    print("You've found %i BLUE agents." % blueFound)
    return blueFound == 9 or redFound == 8

def guessCoordinate(z,board,keyCard, results):
    if board[z] == "NEU" or board[z] == "RED" or board[z]=="BLU" or board[z] =="DIE":
        print("You've already guessed %i,%i." % (x,y))
        return 0

    agentType = keyCard[z]
    if agentType == 0:
        #  Neutral
        print("%s is NEUTRAL! What a waste of turn." % board[z])
        board[z] = "NEU"
    elif agentType == 1:
        #  Blue
        print("%s is a BLUE agent! Good job!" % board[z])
        board[z] = "BLU"
    elif agentType == 2:
        #  Red
        print("%s is a RED agent! Too bad!" % board[z])
        board[z] = "RED"
    else:
        #  Assassin
        print("%s is an ASSASSIN!" % board[z])
        board[z] = "DIE"

    #  We found something, increment results
    results[agentType] = results[agentType]+1

def findCodenameCoord(response):
    for c in range(len(board)):
        if response == board[c]:
            return c
    return -1

def isGameOver(results):
    if results[1] == 9:
        print("You found all the BLUE agents! You win!")
        return 1
    elif results[2] == 8:
        print("All the RED agents were revealed! You lose!")
        return 1
    elif results[3] == 1:
        print("You found the assassin. You lose.")
        return 1
    else:
        return 0

def writeResults(results):
    date = datetime.datetime.now().strftime("%m_%d_%Y-%H_%M_%S")
    resultFileName = "output/%s-%s.txt" % (versionNumber,date)
    
    resultsFile = open(resultFileName,'w')

    resultsFile.write("%i %i %i %i" % (results[0],results[1],results[2],results[3]))
    for guess in guesses:
        resultsFile.write("\n%s"%guess)

    resultsFile.close()

def game(board, keyCard, longestWordLength):
    #  Welcome Message
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to Codenames!\n")
    print("Use the computer generated hints to try to find your BLUE agents!")
    print("Input a codename you think the bot is referring to.\n")
    if model_type == "t":
        model = TwitterPredictor()
    else:
        model = SpacyClassifier()

    #  Keeping track of score, neutral, blue, red, assassin
    results = [0,0,0,0]
    gameOver = 0
    player = 1
    #  Main game loop
    while not gameOver:
        printBoard(board,longestWordLength)
        hintRef, bot_clues = hint.gen_hint(player,board,keyCard,model)
        print("\nThe hint is \'%s\'. It refers to %i active codename(s)." % hintRef)   
        
        #  Keep looping until they give good input
        response = ""
        coord = -1
        while response == "" and coord == -1:
            attemptedResponse = input().lower()
            coord = findCodenameCoord(attemptedResponse)
            if coord != -1:
                response = attemptedResponse
            else:
                print("%s not found on board." % attemptedResponse)

        guesses.append("%s %s" % (hintRef[0], response))

        os.system('cls' if os.name == 'nt' else 'clear')
        print("The bot was thinking of {} with the clue {}".format(bot_clues, hintRef[0]))
        guessCoordinate(coord, board, keyCard, results)
        gameOver = isGameOver(results)

    print("You found %i BLUE agents, %i RED agents, %i NEUTRALS, and %i ASSASSIN(s)" % (results[1],results[2],results[0],results[3]))
    writeResults(results)

board, longestWordLength = createBoard()
keyCard = random.choice(keyCards)
game(board,keyCard,longestWordLength)
