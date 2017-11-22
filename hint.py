from gensim.models import Word2Vec

ignored_words = ["BLU", "RED", "NEU", "DIE"]

def generateHint(player, board, keyCard, model):
    zipped = zip(board, keyCard)
    positive = list(map(lambda y: y[0], filter(lambda x: x[0] not in ignored_words and x[1] == player, zipped)))
    negative = list(map(lambda y: y[0], filter(lambda x: x[0] not in ignored_words and x[1] != player, zipped)))
    
    return model.generateHint(positive, negative)