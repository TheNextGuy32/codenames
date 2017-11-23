"""
spacyPredictor.py

This file allows comparisons to the spaCy word vector models.
"""

import spacy
import numpy
vectorModel = spacy.load('en_vectors_web_lg')

def vectorize(words):
    # Generate vectors for each word based on spaCy's model
    vectors = [vectorModel.vocab[word].vector for word in words]
    return vectors

def overlap(hint, words):
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
    # Return the most similar word compared to the given vector
    similarWords = []
    for w in vectorModel.vocab:
        if (w.has_vector) and (w.orth_.islower()) and (w.lower_ not in words):
            similarWords.append(w)
    similarWords.sort(key=lambda w: similarity(w.vector, vector), reverse=True)
    return similarWords[:10]

def chooseHint(candidates):
    if len(candidates) > 0:
        clues = [c.orth_ for c in candidates]
        for clue in clues:
            if not overlap(clue, words):
                return clue

def filterBoard(board, keyCard):
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
    blues = [b for b in blues if b != 'BLU']
    reds = [r for r in reds if r != 'RED']
    return blues, reds, assassin

def generateHint(board, keyCard):
    blues, reds, assassin = filterBoard(board, keyCard)
    blueVectors = vectorize(blues)
    redVectors = vectorize(reds)
    assassin = vectorize([assassin])[0]

if __name__ == '__main__':
    words = ['clown', 'sphere', 'money', 'box']
    keyCard = [0, 1, 2, 3]
    hint = generateHint(words, keyCard)
    print(hint)
