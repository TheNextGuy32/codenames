"""
mapper.py

This file handles the reading of map files.
"""

from collections import Counter

def verify(boardMap):
    counts = Counter(boardMap)
    return counts[0] == 7 and counts[1] == 9 and counts[2] == 8 and counts[3] == 1

def main():
    maps = []
    with open('codenameMap20.txt', 'r') as mapFile:
        # First line contains number of maps in the file
        count = int(mapFile.readline())
        while count > 0:
            line = mapFile.readline().rstrip('\n')
            # Every map is separated by ===
            if line == '===':
                boardMap = []
                for i in range(5):
                    rowStr = mapFile.readline().rstrip('\n').split()
                    rowInt = [int(rowStr[j]) for j in range(len(rowStr))]
                    boardMap = boardMap + rowInt
                if verify(boardMap):
                    maps.append(boardMap)
                count -= 1

    print(len(maps))
    for m in maps:
        print(m)

if __name__ == '__main__':
    main()
