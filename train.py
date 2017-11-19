from gensim.models import Word2Vec
import random

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
printBoard(board,longestWordLength)
