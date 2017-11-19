"""
spacyPredictor.py

This file allows comparisons to the spaCy word vector models.
"""

import spacy
import numpy
vectorModel = spacy.load('en_vectors_web_lg')

def similarity(wv1, wv2):
    # compare similarity between two numpy vectors
    if (numpy.linalg.norm(wv1) == 0) or (numpy.linalg.norm(wv2) == 0):
        return 0.0
    return numpy.dot(wv1, wv2) / numpy.linalg.norm(wv1) * numpy.linalg.norm(wv2)

def mostSimilar(vector, words):
    # Return the most similar word compared to the given vector
    similarWords = []
    for w in vectorModel.vocab:
        if (w.has_vector) and (w.orth_.islower()) and (w.lower_ not in words):
            similarWords.append(w)
    similarWords.sort(key=lambda w: similarity(w.vector, vector), reverse=True)
    return similarWords[0].orth_

def vectorize(words):
    # Generate vectors for each word based on spaCy's model
    vectors = [vectorModel.vocab[word].vector for word in words]
    return vectors

if __name__ == '__main__':
    vectors = vectorize(['clown', 'sphere', 'money'])
    print(mostSimilar(vectors[2], ['clown', 'sphere', 'money']))
