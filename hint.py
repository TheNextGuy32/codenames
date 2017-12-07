from gensim.models import Word2Vec

ignored_words = ["BLU", "RED", "NEU", "DIE"]

def gen_hint(player, board, keyCard, model):
    zipped = list(zip(board, keyCard))
    positive = list(map(lambda y: y[0], filter(lambda x: x[0] not in ignored_words and x[1] == player, zipped)))
    negative = list(map(lambda y: y[0], filter(lambda x: x[0] not in ignored_words and x[1] != player, zipped)))
    neutral = list(map(lambda y: y[0], filter(lambda x: x[0] not in ignored_words and x[1] == 0, zipped)))
    die = list(map(lambda y: y[0], filter(lambda x: x[0] not in ignored_words and x[1] == 3, zipped)))[0]
    hint = model.gen_hint(positive, negative, die, neutral)
    print(hint)
    return hint
