import os
from time import sleep
from random import random


# Get samples
dir = "/home/pi/bukowski/poems/"
samples = os.listdir(dir)
played = []
#print(samples)

def speak():
    # Pick random sample
    alea = (int)(random()*len(samples))

    # Don't repeat yourself
    while played.count(alea):
        alea = (int)(random()*len(samples))
        if len(played) == len(samples):
            played.clear()

    file = dir+samples[alea]

    #line = open(file, "r")
    #print(line.read())
    print(samples[alea].replace('.txt', ''))

    os.system('espeak -p 0 -a 100 -s 105 -v english-us -f {0}'.format(file))
    played.append(alea)

while True:
    speak()
    sleep(20)
