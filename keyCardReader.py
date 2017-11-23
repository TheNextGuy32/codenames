"""
mapper.py

This file handles the reading of key card files.
0 represents Neutral
1 represents Blue
2 represents Red
3 represents Assassin
"""

from collections import Counter

def verify(keyCard):
    counts = Counter(keyCard)
    return counts[0] == 7 and counts[1] == 9 and counts[2] == 8 and counts[3] == 1

def readFromFile():
    keyCards = []
    with open('codenameKeyCard20.txt', 'r') as keyCardFile:
        # First line contains number of key cards in the file
        count = int(keyCardFile.readline())
        while count > 0:
            line = keyCardFile.readline().rstrip('\n')
            # Every key card is separated by ===
            if line == '===':
                keyCard = []
                for i in range(5):
                    rowStr = keyCardFile.readline().rstrip('\n').split()
                    rowInt = [int(rowStr[j]) for j in range(len(rowStr))]
                    keyCard = keyCard + rowInt
                if verify(keyCard):
                    keyCards.append(keyCard)
                count -= 1
    return keyCards

if __name__ == '__main__':
    keyCards = readFromFile()
    print(len(keyCards))
    for kc in keyCards:
        print(kc)
