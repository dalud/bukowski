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
wasStillSpeaking = 0
arduinoBusy = False
pose = 1
output = Output()
arduino = Arduino()
arduino.connect()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.IN) #Lasin uppokytkin
GPIO.setup(13, GPIO.IN) #Nielun uppokytkin
GPIO.setup(16, GPIO.OUT) #Suu
GPIO.setup(18, GPIO.IN) #Arduino busy signal

def exit():
    print("User exit")
    flush()
    GPIO.output(16, GPIO.LOW)
    arduino.write("z")
    sys.exit()

def signal_term_handler(signal, frame):
    print("SIGTERM")
    flush()
    exit()
signal.signal(signal.SIGTERM, signal_term_handler)

def drink():
    arduino.write("d")
    
def fillerUp():
    print('\n'*cls)
    print("Getting drink...")
    flush()
    arduino.write("h")
    GPIO.output(16, GPIO.HIGH)
    mouth.speakAsync(fillersUp[(int)(random()*len(fillersUp))])
    sleep(3)
    GPIO.output(16, GPIO.LOW)
    arduino.write("t")
    
def piss():
    print("Pissing...")
    flush()
    arduino.write('k')
    sleep(8)

def isArduinoBusy():
    return arduinoBusy

flush()
GPIO.output(16, GPIO.HIGH)
mouth.speak("Alright, I'm on.")
flush()
GPIO.output(16, GPIO.LOW)
arduino.write("1")
sleep(3)

while True:
    received = arduino.read()
    if received:
        #print(received)
        flush()
        if received == "busy":
            arduinoBusy = True
        if received == "free":
            arduinoBusy = False
    # print("arduino busy:", isArduinoBusy())
            
    try:
        if mouth.isSpeaking():
            s = subject = cue = None
            GPIO.output(16, GPIO.HIGH)
            wasStillSpeaking = time.time()
            # Only motion if Arduino is idle
            if not isArduinoBusy():
                # Tuoli
                if(random()*10 < 5):
                    arduino.write('c'+str(round(random())))
                # Käsi
                if(random()*10 < 7):
                    pose = round(random()*3)
                if not pose: pose = 1
                arduino.write(str(pose))
                
        if not mouth.isSpeaking():
            GPIO.output(16, GPIO.LOW)
            if(time.time() - wasStillSpeaking < 2) and not isArduinoBusy():
                arduino.write("d")
                    
            GPIO.output(16, GPIO.LOW)
            print('\n'*cls)
            flush()

            # Is tuoppi tyhjä?
            if GPIO.input(15) and not isArduinoBusy():
                piss()
                fillerUp()
            # Is nielu tyhjä?
            if GPIO.input(13) and not isArduinoBusy():
                print("Filling nielu...")
                flush()
                arduino.write("n")
            
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
                        GPIO.output(16, GPIO.HIGH)
                        mouth.speak(s+"?")
                        GPIO.output(16, GPIO.LOW)
                        sleep(.5)
                        s = subject = cue = None
                        GPIO.output(16, GPIO.HIGH)
                        mouth.speak(affirm[(int)(random()*len(affirm))])
                        GPIO.output(16, GPIO.LOW)
                        sleep(.5)
                        print('\n'*cls)
                        flush()
                        mouth.speakAsync(reply)
                        played.append(reply)
                        print(":msg:"+reply)
                        flush()
                        reply = None
                        if len(played) > 100: played.clear()
                        break
                    if subject.index(s) == len(subject)-1:
                        GPIO.output(16, GPIO.HIGH)
                        mouth.speak(s+"?")
                        GPIO.output(16, GPIO.LOW)
                        sleep(.5)
                        s = subject = cue = None
                        GPIO.output(16, GPIO.HIGH)
                        mouth.speak(decline[(int)(random()*len(decline))])
                        GPIO.output(16, GPIO.LOW)
                        sleep(.5)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        flush()
        exit()
