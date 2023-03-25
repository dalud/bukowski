import os

class Mouth:
    #def __init__(self):
    def speak(self, sentence):
        os.system('espeak -p 0 -a 100 -s 105 -v english-us "{0}"'.format(sentence))
