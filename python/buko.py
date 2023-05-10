import sys
from speechVosk_IF import Ear
from searchInFiles_IF import Searcher
from speak_IF import Mouth
from nltk_IF import SubjectParser
from random import random
import asyncio
from delayedPrint_IF import DelayedPrint

flush = sys.stdout.flush

ear = Ear()
mouth = Mouth()
sb = SubjectParser()
dir_path = r'/home/pi/bukowski/works'
searcher = Searcher(dir_path)
printer = DelayedPrint(.05)
played = []
affirm = ['yes', 'yeah', 'ah', 'sure', 'well', 'eh']
decline = ['no', "I don't think so", "sorry, no", 'negative']
apologize = ["sorry?", "excuse me?", "huh?", "what?", "what do you mean?", "I didn't get that"]
cls = 10

mouth.speak("Alright, I'm on.")

while True:
    print('\n'*cls)
    flush()
    #TODO: if subprocess speaking DO Not get new subject
    cue = ear.listen(True)
    subject = sb.parse(cue)
    #print(subject)
    flush()
    if subject:
        for s in subject:
            if not  s == "huh":
                #print(s)
                flush()
                #mouth.speak(s+"?")
                reply = searcher.find(s, played)
                if reply and not reply in played:
                    mouth.speak(s+"?")
                    mouth.speak(affirm[(int)(random()*len(affirm))])
                    print('\n'*cls)
                    flush()
                    mouth.speakAsync(reply)
                    played.append(reply)
                    printer.print(reply)
                    flush()
                    #print("covered:" +str(len(played)))
                    flush()
                    if len(played) > 50: played.clear()
                    break
                if subject.index(s) == len(subject)-1:
                    mouth.speak(s+"?")
                    mouth.speak(decline[(int)(random()*len(decline))])
    else: mouth.speak(apologize[(int)(random()*len(apologize))])
