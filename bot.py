
class Bot:
    def __init__(self, color, classifier):
        self.color = color
        self.classifier = classifier
        self.hints_given = []

    def generate_hint(self, blue, red, black, words):
        positive = blue
        negative = red

        if (self.color == 'red'):
            postive = red
            negative = blue 

        bad_words = words + self.hints_given
        out = self.classifier.gen_hint(positive, negative, black, bad_words)
        print(out)
        self.hints_given += out[0]
        return out


        
            
            
