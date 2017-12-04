from gensim.models import KeyedVectors
from functools import reduce
from itertools import product
from nltk.corpus import wordnet
import pickle
import itertools

class TwitterPredictor():
    def __init__(self):
        self.model = pickle.load(open("twitter-model.p", "rb"))
        #self.model = KeyedVectors.load_word2vec_format('crawl-vectors.txt', binary=False)
        #pickle.dump(self.model, open("crawl-model.p", "wb"));

    def get_max(self, a, b):
        a_mod = 0
        b_mod = 0
        if len(a[0]) == 1:
            a_mod = -0.5
        if len(b[0]) == 1:
            b_mod = -0.5
        if a[1][1] + a_mod >= b[1][1] + b_mod:
            return a
        return b
    
    def notOnBoard(self, clue, all_words):
        for word in all_words:
            if clue in word or word in clue:
                return False
        return True
    
    def avg_distance(self, clue, target_words, negative):
        max_len = 4
        dist = 0
        clue_sys = wordnet.synsets(clue)
        if len(clue_sys) > max_len:
            clue_sys = clue_sys[:max_len]
        clue_sys = set(clue_sys)
        
        for word in target_words:
            target_sys = wordnet.synsets(word)
            if len(target_sys) > max_len:
                target_sys = target_sys[:max_len]
            target_sys = set(target_sys)
            try:
                best = max((wordnet.wup_similarity(s1, s2) or 0) for s1, s2 in product(clue_sys, target_sys))
            except:
                best = 0
            dist += best
        
        similarity = self.model.n_similarity([clue], negative)
        return (dist / len(target_words)) - similarity
    
    def dump_guesses(self, guesses):
        for guess in guesses:
            print(guess[0])
            for prob in guess[1]:
                print(prob)
            print('')
        print('\n\n')
    
    def gen_hint(self, posWords, negWords, black, words):
        all_words = posWords + negWords + words + [black]
        #all_words = []
        out = []
        for i in range(0, min(4, len(posWords) + 1)):
            temp = [list(x) for x in itertools.combinations(posWords, i)]
            out.extend(temp)
        
        filtered_out = list(filter(lambda x: len(x) > 0, out))

        guesses = list(map(lambda x: (x, self.model.most_similar_cosmul(positive=x)), filtered_out))
        filtered_guesses = list(map(lambda x: (x[0], list(filter(lambda y: self.notOnBoard(y[0], all_words), x[1]))), guesses))
        #self.dump_guesses(filtered_guesses)
        filtered_guesses = list(filter(lambda y: len(y[1]) > 0, map(lambda x: (x[0], sorted(map(lambda y: (y[0], y[1] + self.avg_distance(y[0], x[0], negWords)), x[1]), key=lambda z: z[1], reverse=True)), filtered_guesses)))
        #self.dump_guesses(filtered_guesses)

        if len(filtered_guesses) == 1:
            guess = (filtered_guesses[0][0], filtered_guesses[0][1][0])
        else:
            guess = reduce(self.get_max, map(lambda x: (x[0], x[1][0]), filtered_guesses), ('', ('', 0)))
        
        return (guess[1][0], len(guess[0])), guess[0]

def main():
    pred = TwitterPredictor()
    print('cream' in 'ice')
    hint = pred.gen_hint(['spy', 'carrot', 'sink', 'mole', 'school', 'tag', 'casino', 'scorpion'], ['princess', 'state', 'water', 'himalayas', 'dress', 'pie', 'spring', 'air', 'paper'], 'bed', [])
    print(hint)
    # print(not any(word in ''))

if __name__ == "__main__":
    main()
