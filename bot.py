
class Bot:
    def __init__(self, color, classifier):
        self.color = color
        self.classifier = classifier
        self.hints_given = []

    def generate_hint(self, blue, red, black, words):
        positive = blue
        negative = red + black

        if (self.color == 'red'):
            postive = red
            negative = blue + black

        bad_words = words + self.hints_given
        self.classifier.generate_hint(positive, negative, bad_words)
        
            
            
