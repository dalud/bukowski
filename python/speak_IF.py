import os
from subprocess import Popen

class Mouth:
    #def __init__(self):
    def speak(self, sentence):
        os.system('espeak -p 0 -a 100 -s 105 -v english-us "{0}"'.format(sentence))

    def speakAsync(self, sentence):
        #os.system('espeak -p 0 -a 100 -s 105 -v english-us "{0}"'.format(sentence))
        Popen('espeak -p 0 -a 100 -s 84 -v english-us "{0}"'.format(sentence), shell=True)    
