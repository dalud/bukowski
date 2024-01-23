import sys
from speechVosk_IF import Ear
from searchInFiles_IF import Searcher
from speak_IF import Mouth
from nltk_IF import SubjectParser
from random import random
from amplitude_IF import Output
from arduinoIF import Arduino
from time import sleep
import time
import signal
import RPi.GPIO as GPIO

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
fillersUp = ["Looks like I need another drink", "I need to fill'er up!", "Running dry again It seems...", "Maybe one more, eh?"]
cls = 14
s = subject = cue = None
otetutHuikat = 0
wasStillSpeaking = 0
pose = 1
output = Output()
arduino = Arduino()
arduino.connect()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

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

def drink():
    arduino.write("d")
    #otetutHuikat += 1
    
def fillerUp():
    print('\n'*cls)
    print("Getting drink...")
    flush()
    #sleep(11) #Is this really necessary
    arduino.write("h")
    sleep(1)
    mouth.speakAsync(fillersUp[(int)(random()*len(fillersUp))])
    sleep(5)
    arduino.write("z")
    sleep(3)
    print('\n'*cls)
    print("Filling glass...")
    flush()
    arduino.write("t")
    sleep(20)
    arduino.write("1")
    sleep(6)
    print('\n'*cls)
    print("Filling nielu...")
    flush()
    arduino.write("n")
    sleep(10)
    print('\n'*cls)

def piss():
    print("Pissing...")
    flush()
    arduino.write('k')
    sleep(8)

flush()
mouth.speak("Alright, I'm on.")
flush()
arduino.write("1")
sleep(3)

while True:
    received = arduino.read()
    #if received:
        # Mahdollisesti joskus
        #print(received)
        #flush()
        #continue
    try:
        if mouth.isSpeaking():
            s = subject = cue = None
            arduino.write("p1")
            wasStillSpeaking = time.time()
            # Tuoli
            if(random()*10 < 5):
                arduino.write('c'+str(round(random())))
            # Käsi
            if(random()*10 < 7):
                pose = round(random()*3)
            if not pose: pose = 1
            arduino.write(str(pose))
                
        if not mouth.isSpeaking():
            if(time.time() - wasStillSpeaking < 2):
                arduino.write("d")
                #otetutHuikat += 1
                    
            arduino.write("p0")
            print('\n'*cls)
            flush()
            #if otetutHuikat > 3:
            if GPIO.input(11):
                piss()
                fillerUp()
                #otetutHuikat = 0
                    
            cue = ear.listen(True, s)
            if cue: subject = sb.parse(cue[0])
            else: subject = None
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
                        sleep(.5)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        flush()
        exit()
