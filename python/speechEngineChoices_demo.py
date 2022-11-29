import subprocess
import sys
import os
from threading import Thread
from queue import Queue, Empty
import signal


# Utils
process = None
ON_POSIX = 'posix' in sys.builtin_module_names
q = Queue()

def enqueue_output(out, queue):
    for line in iter(out.readline, ''):
        queue.put(line)
    out.close()

# Helpers
def start(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1, close_fds=ON_POSIX)
    t = Thread(target=enqueue_output, args=(process.stdout, q))
    t.daemon = True
    t.start()

#start(['espeak', '-p 0', '-a 100', '-s 130', '"let the demon take your soul"'])


while True:
    print("1. eSpeak")
    print("2. Festival")
    print("3. FLite")
    choice = input("Select option:")

    if choice == "1":
        os.system('espeak -p 0 -a 60 -s 130 "let the demon take your soul"')
    elif choice == "2":
        os.system('echo "let the demon take your soul" | festival --tts')
    elif choice == "3":
        os.system('flite --setf int_f0_target_mean=50 --setf duration_stretch=1.4 -voice kal16 -t "let the demon take your soul"')
    elif choice == "4":
        os.system('spd-say -l en -p -100 -r -50 -i -40 "let the demon take your soul"')
    elif choice == "5":
        os.system('pico2wave -w test.wav "let the demon take your soul" && aplay test.wav')

