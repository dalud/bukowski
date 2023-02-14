#from speechVosk_IF import Ear
from searchInFiles_IF import Searcher

#ear = Ear()
dir_path = r'C:\Users\jaakk\OneDrive\Documents\poems'
searcher = Searcher(dir_path)

#ear.listen(True)
word = "silence"
print(searcher.search(word))
