from speechVosk_IF import Ear
from searchInFiles_IF import Searcher
from speak_IF import Mouth
from nltk_IF import SubjectParser
from random import random

ear = Ear()
mouth = Mouth()
sb = SubjectParser()
dir_path = r'/home/pi/bukowski/works'
searcher = Searcher(dir_path)
played = []
affirm = ['yes', 'sure', 'ofcourse']
decline = ['no', "I don't think so", "sorry"]

while True:
    cue = ear.listen(True)
    subject = sb.parse(cue)
    print(subject)
    if subject:
        for s in subject:
            if not  s == "huh":
                print(s)
                mouth.speak(s+"?")
                reply = searcher.find(s, played)
                if reply and not reply in played:
                    mouth.speak(affirm[(int)(random()*len(affirm))])
                    print(reply)
                    mouth.speak(reply)
                    played.append(reply)
                    print("covered:" +str(len(played)))
                    if len(played) > 20: played.clear()
                    break
                else: mouth.speak(decline[(int)(random()*len(decline))])
    else: mouth.speak(decline[(int)(random()*len(decline))])
