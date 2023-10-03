import sys
from speechVosk_IF import Ear
from searchInFiles_IF import Searcher
from speak_IF import Mouth
from nltk_IF import SubjectParser
from random import random
import pyaudio
import audioop

flush = sys.stdout.flush

ear = Ear()
mouth = Mouth()
sb = SubjectParser()
dir_path = r'/home/pi/bukowski/works'
searcher = Searcher(dir_path)
played = []
affirm = ['yes', 'yeah', 'ah', 'sure', 'well', 'eh']
decline = ['no', "I don't think so", "sorry, no", 'negative']
apologize = ["sorry?", "excuse me?", "huh?", "what?", "what do you mean?", "I didn't get that"]
cls = 14
s = None
audio = pyaudio.PyAudio()
print(audio.get_default_output_device_info())
stream = audio.open(format=2, channels=2, rate=44100, input=True)

mouth.speak("Alright, I'm on.")

while True:
    if mouth.isSpeaking():
        s = subject = cue = None
        print("|"*audioop.rms(stream.read(1), 1))        
        
    if not mouth.isSpeaking():
        print('\n'*cls)
        flush()
        cue = ear.listen(True, s)
        #print(cue)
        if cue: subject = sb.parse(cue[0])
    else:
        subject = None
    flush()
    if subject:
        for s in subject:
            if not  s == "huh" and not mouth.isSpeaking():
                flush()
                reply = searcher.find(s, played)
                if reply and not reply in played and not mouth.isSpeaking():
                    mouth.speak(s+"?")
                    s = subject = cue = None
                    mouth.speak(affirm[(int)(random()*len(affirm))])
                    print('\n'*cls)
                    flush()
                    mouth.speakAsync(reply)
                    played.append(reply)
                    #print(len(played))
                    print(":msg:"+reply)
                    flush()
                    reply = None
                    if len(played) > 150: played.clear()
                    break
                if subject.index(s) == len(subject)-1:
                    mouth.speak(s+"?")
                    s = subject = cue = None
                    mouth.speak(decline[(int)(random()*len(decline))])
    #else: mouth.speak(apologize[(int)(random()*len(apologize))])
