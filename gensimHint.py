import gensim, logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
     
    # train word2vec on the two sentences
    model = gensim.models.Word2Vec(sentences, min_count=1)

    def generateHint(board, keyCard):
        hint = "ballroom"
        numberReferences = 1
        return (hint, numberReferences)