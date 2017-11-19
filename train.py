from gensim.models import Word2Vec
import os
import re
import random
import keyCardReader


codenameFile = open("codenameList.txt",'r')
codenames = codenameFile.readlines()
codenameFile.close()

codenameSentences = []
for c in range(len(codenames)):
	codename = codenames[c] = codenames[c].strip()

	codenameSentences.append([codename])
	codenames[c] = codename

keyCards = keyCardReader.readFromFile()
keyCard = keyCards[int(random.random()*(len(keyCards)))]	

# trainedModelFile = "MODEL_FILE.txt"
# model = Word2Vec.load(trainedModelFile)
# print(c.most_similar('money', topn=5))




def createBoard():
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

board, longestWordLength = createBoard()

def generateHint(board, keyCard):
	return "Ballroom 1"

def isGameComplete(board):
	return 0

def guessCoordinate(z,board,keyCard):
	if board[z] == "NEU" or board[z] == "RED" or board[z]=="BLU" or board[z] =="DIE":
		print("You've already guessed %i,%i." % (x,y))
		return 0

	agentType = keyCard[z]
	if agentType == 0:
		#  Neutral
		print("%s was NEUTRAL! Too bad!\n" % board[z])
		board[z] = "NEU"
	elif agentType == 1:
		#  Blue
		print("%s was a BLU agent! Good job!\n" % board[z])
		board[z] = "BLU"
	elif agentType == 2:
		#  Red
		print("%s was a RED agent! Too bad!\n" % board[z])
		board[z] = "RED"
	else:
		#  Assassin
		print("%s was an ASSASSIN! You lose!\n" % board[z])
		board[z] = "DIE"
		return 1
		
	return isGameComplete(board)

def findCodenameCoord(response):
	for c in range(len(board)):
		if response == board[c]:
			return c
	return -1

def game(board,keyCard):
	#  Welcome Message
	print("Welcome to Codenames!\n")
	print("Use the computer generated hints to try to find your agents!")
	print("Input the codename you think the bot is referring to.\n")

	#  Main game loop
	gameComplete = 0
	while not gameComplete:
		printBoard(board,longestWordLength)
		print("\nHint: %s" % generateHint(board,keyCard))	
		
		#  Keep looping until they give good input
		response = ""
		coord = -1
		while response == "" and coord == -1:
			attemptedResponse = input().lower()
			if re.match("^[a-z]", attemptedResponse):
				coord = findCodenameCoord(attemptedResponse)
				if coord != -1:
					response = attemptedResponse
				else:
					print("%s not found on board."%attemptedResponse)
			else:
				print("Incorrect input format.")

		#  Attempt game and see if we are done
		os.system('cls' if os.name == 'nt' else 'clear')
		gameComplete = guessCoordinate(coord,board,keyCard)
	print("Game Over! Thanks for playing!")
game(board,keyCard)
