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
	board = [""] * 25 
	freeCodename = [1]  * len(codenames)
	for i in range(25):
		while 1:
			codenameIndex = int(random.random()*(len(codenames)+1))	
			if freeCodename[codenameIndex]:
				board[i] = codenames[codenameIndex]
				freeCodename[codenameIndex] = 0
				break
	return board

board = createBoard()

