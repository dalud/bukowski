import sys
from speechVosk_IF import Ear
from searchInFiles_IF import Searcher
from speak_IF import Mouth
from nltk_IF import SubjectParser
from random import random
from amplitude_IF import Output
from arduinoIF import Arduino
from time import sleep
import signal

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
s = subject = cue = None
otetutHuikat = 0
output = Output()
arduino = Arduino()
arduino.connect()


def exit():
    print("User exit")
    flush()
    arduino.write("z")
    sys.exit()

def signal_term_handler(signal, frame):
    print("SIGTERM")
    flush()
    exit()
signal.signal(signal.SIGTERM, signal_term_handler)

#def drink():
    
def fillerUp():
    arduino.write("t")
    sleep(30)
    arduino.write("1")
    sleep(2)
    arduino.write("4")
    sleep(3)
    arduino.write("1")

flush()
mouth.speak("Alright, I'm on.")
arduino.write("1")
sleep(2)

while True:
    received = arduino.read()
    if received:
        continue
        #print("Nyt tuli hommia:", received)
        #flush()
        #if received == "t":
                #print("täyttää vissiin pitäis...")
                #flush()
    else:
        try:
            if mouth.isSpeaking():
                s = subject = cue = None
                #arduino.write('p'+str(output.read()))
                arduino.write("p1")
                received = arduino.read()
                
            if not mouth.isSpeaking():
                arduino.write("p0")
                print('\n'*cls)
                flush()
                if otetutHuikat > 5:
                    fillerUp()
                    otetutHuikat = 0
                    
                cue = ear.listen(True, s)
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
                            arduino.write("p1")
                            mouth.speak(s+"?")
                            arduino.write("p0")
                            sleep(.5)
                            s = subject = cue = None
                            arduino.write("p1")
                            mouth.speak(affirm[(int)(random()*len(affirm))])
                            arduino.write("p0")
                            sleep(.5)
                            print('\n'*cls)
                            flush()
                            mouth.speakAsync(reply)
                            played.append(reply)
                            print(":msg:"+reply)
                            flush()
                            reply = None
                            if len(played) > 200: played.clear()
                            break
                        if subject.index(s) == len(subject)-1:
                            arduino.write("p1")
                            mouth.speak(s+"?")
                            arduino.write("p0")
                            sleep(.5)
                            s = subject = cue = None
                            arduino.write("p1")
                            mouth.speak(decline[(int)(random()*len(decline))])
                            arduino.write("p0")
                            arduino.write("d")
                            otetutHuikat += 1
                            sleep(5)
                            sleep(.5)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            flush()
            exit()
