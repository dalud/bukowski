import sys
from time import sleep

class DelayedPrint:
    #def __init__(self):

    def print(self, message):
        #TODO: match delay to fit message length
        delay = .25

        for i in range(len(message)):
            sys.stdout.write(message[i])
            sys.stdout.flush()
            sleep(delay)
