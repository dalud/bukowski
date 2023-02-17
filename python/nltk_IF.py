from rake_nltk import Rake

class SubjectParser:
    def __init__(self):
        self.rake = Rake()

    def parse(self, sentence):
        kw = self.rake.extract_keywords_from_text(sentence)
        return self.rake.get_ranked_phrases()
