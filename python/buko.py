import sys
from speechVosk_IF import Ear
from searchInFiles_IF import Searcher
from speak_IF import Mouth
from nltk_IF import SubjectParser
from random import random

flush = sys.stdout.flush

ear = Ear()
mouth = Mouth()
sb = SubjectParser()
dir_path = r'/home/pi/bukowski/works'
searcher = Searcher(dir_path)
played = []
affirm = ['yes', 'yeah', 'sure', 'ofcourse!', 'definitely', 'well', 'okay baby']
decline = ['no', "I don't think so", "sorry, no", "probably not", 'negative']
apologize = ["sorry?", "excuse me?", "huh?", "what?", "what do you mean?", "I didn't get that"]
cls = 10

mouth.speak("Alright, I'm on.")

while True:
    print('\n'*cls)
    flush()
    cue = ear.listen(True)
    subject = sb.parse(cue)
    #print(subject)
    flush()
    if subject:
        for s in subject:
        #with subject[0] as s:
        #s = subject[0]
            if not  s == "huh":
                #print(s)
                flush()
                #mouth.speak(s+"?")
                reply = searcher.find(s, played)
                if reply and not reply in played:
                    mouth.speak(affirm[(int)(random()*len(affirm))])
                    print('\n'*cls)
                    flush()
                    print(reply)
                    flush()
                    mouth.speak(reply)
                    played.append(reply)
                    #print("covered:" +str(len(played)))
                    flush()
                    if len(played) > 50: played.clear()
                    break
                if subject.index(s) == len(subject)-1:
                    mouth.speak(decline[(int)(random()*len(decline))])
    else: mouth.speak(apologize[(int)(random()*len(apologize))])
