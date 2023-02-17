from rake_nltk import Rake
from nltk_IF import SubjectParser
rake = Rake()

kw = rake.extract_keywords_from_text("")

ranked_phrases = rake.get_ranked_phrases()

print(ranked_phrases)

sb = SubjectParser()
print(sb.parse(""))
