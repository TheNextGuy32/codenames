"""
spacyPredictor.py

This file allows generating hints by measuring
the words using spaCy word vector models.
"""

import spacy
import numpy
vectorModel = spacy.load('en_vectors_web_lg')

def overlap(hint, words):
    """ Check if the hint has overlaps or is overlapped
    by any word in words. (e.g. 'clown' in 'clowns')

    :param hint:    The proposed hint string
    :param words:   List of word strings
    """
    overlap = False
    for codename in words:
        overlap = overlap or (hint in codename or codename in hint)
    return overlap

def similarity(wv1, wv2):
    # compare similarity between two numpy vectors
    if (numpy.linalg.norm(wv1) == 0) or (numpy.linalg.norm(wv2) == 0):
        return 0.0
    return numpy.dot(wv1, wv2) / numpy.linalg.norm(wv1) * numpy.linalg.norm(wv2)

def tenMostSimilar(vector):
    # Return the 10 most similar word compared to the given vector
    similarWords = []
    for w in vectorModel.vocab:
        if (w.has_vector) and (w.orth_.islower()) and (w.lower_ not in words):
            similarWords.append(w)
    similarWords.sort(key=lambda w: similarity(w.vector, vector), reverse=True)
    return similarWords[:10]

def chooseHint(candidates, words):
    if len(candidates) > 0:
        for clue in candidates:
            if not overlap(clue.orth_, words):
                return clue

def filterBoard(board, keyCard):
    """ Organize the given codenames on the board,
    categorizing each word according to role,
    then generating a spaCy representation of each word.
    """
    blues = []
    reds = []
    assassin = ''
    for i in range(len(keyCard)):
        if keyCard[i] == 3:
            assassin = board[i]
        elif keyCard[i] == 2:
            reds.append(board[i])
        elif keyCard[i] == 1:
            blues.append(board[i])
    blues = [vectorModel.vocab[b] for b in blues if b != 'BLU']
    reds = [vectorModel.vocab[r] for r in reds if r != 'RED']
    return blues, reds, vectorModel.vocab[assassin]

def generateHint(board, keyCard):
    blues, reds, assassin = filterBoard(board, keyCard)
    for b in blues:
        bv = b.vector
        bw = b.orth_
        similar = tenMostSimilar(bv)
        hint = chooseHint(similar, board)
        print(hint.orth_ + '\t' + str(hint.similarity(b)))
        print(similarity(bv, hint.vector))
        print(b.similarity(b))

if __name__ == '__main__':
    words = ['clown', 'sphere', 'money', 'box']
    keyCard = [1, 1, 1, 1]
    hint = generateHint(words, keyCard)
    print(hint)
