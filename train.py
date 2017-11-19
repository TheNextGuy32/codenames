codenameFile = open("codenameList.txt",'r')
codenames = codenameFile.readlines()

for c in range(len(codenames)):
	codenames[c] = codenames[c].strip()

