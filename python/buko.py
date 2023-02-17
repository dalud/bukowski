from speechVosk_IF import Ear
from searchInFiles_IF import Searcher
from speak_IF import Mouth

ear = Ear()
mouth = Mouth()

dir_path = r'/home/pi/bukowski/poems'
searcher = Searcher(dir_path)

while True:
    cue = ear.listen(True)
    #word = " car "
    #reply = searcher.search(word)
    #print(reply)
    mouth.speak(cue)
