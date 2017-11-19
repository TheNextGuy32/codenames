from gensim.models import Word2Vec
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

def guessCoordinate(x,y,board,keyCard):
	z = (y*5)+x
	agentType = keyCard[z]
	if agentType == 0:
		#  Neutral
		print("%s was NEUTRAL! Too bad!" % board[z])
		board[z] = "NEU"
	elif agentType == 1:
		#  Blue
		print("%s was a BLU agent! Good job!" % board[z])
		board[z] = "BLU"
	elif agentType == 2:
		#  Red
		print("%s was a RED agent! Too bad!" % board[z])
		board[z] = "RED"
	else:
		#  Assassin
		print("%s was an assassin! You lose!" % board[z])
		board[z] = "DIE"
		return 1
		
	return isGameComplete(board)

def game(board,keyCard):
	#  Welcome Message
	print("Welcome to Codenames!\n")
	print("Use the computer generated hints to try to find your agents!")
	print("Input the coordinate of the codename you think the bot is referring to.")
	print("Input is X: 0-4 and Y: 0-4 inclusive.\n")
	print("For instance, %s is at 0,1" % board[5])

	#  Main game loop
	gameComplete = 0
	while not gameComplete:
		printBoard(board,longestWordLength)
		print("Hint: %s" % generateHint(board,keyCard))	
		
		#  Keep looping until they give good input
		x = -1
		y = -1
		while x == -1 or y == -1:
			response = input()
			
			#  Wrong input length
			if len(response) != 3:
				print("Response must be in 1,2 format.")
				pass
			
			coords = response.split(',')
			attX = int(coords[0])
			attY = int(coords[1])

			#  Wrong input range
			if attX > 4 or attX < 0 or attY > 4 or attX < 0:
				print("Response coords must be 0-4 inclusive.")
				pass
			x = attX
			y = attY
			
		#  Attempt game and see if we are done
		gameComplete = guessCoordinate(x,y,board,keyCard)

keyCard = {}
game(board,keyCard)
