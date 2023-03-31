#!/usr/bin/env python

import PySimpleGUI as ui
#import configparser
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

# Read config file
#parser = configparser.ConfigParser()
#parser.read('/home/pi/robokerho/config')

# Build UI
layout = [#[ui.Text("Robohemian: Bukowski", font="DisposableDroidBB 16 bold", background_color="black")],
          #[ui.Button("CONFIG", button_color="orange"), ui.Button("RUN", button_color="green"), ui.Button("STOP", button_color="brown"), ui.Button("SHUTDOWN")],
          [ui.Button("RUN", button_color="green on black"), ui.Button("STOP", button_color="red on black"), ui.Button("SHUTDOWN", button_color="grey on black")],
          [ui.Multiline(reroute_stdout=True, reroute_stderr=True, auto_refresh=True, autoscroll=True, expand_x=True, expand_y=True, no_scrollbar=True, background_color="black", text_color="green")]]
window = ui.Window("Robohemian: Bukowski", layout, size=(1024, 600), font="DisposableDroidBB 36 bold", default_button_element_size=(16, 2), button_color="black", auto_size_buttons=False, resizable=True, background_color="black")

# Helpers
def start(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1, close_fds=ON_POSIX)
    t = Thread(target=enqueue_output, args=(process.stdout, q))
    t.daemon = True
    t.start()

# Main loop
while True:
    event, values = window.read(10)
    window.maximize()
    window.TKroot["cursor"] = "none"
    #print("Testing font...")

    if event == "CONFIG":
        start(['killall', 'python3'])
        if not process:
            start(['python3', '/home/pi/robokerho/python/config.py'])

    if event == "RUN":
        print("Starting...")
        start(['killall', 'python3'])
        if not process:
            start(['python3', '/home/pi/bukowski/python/buko.py'])

    if event == "STOP":        
        start(['killall', 'python3'])
        print("STOPPED")
        if process:
            process.stdout.close()
            process.send_signal(signal.SIGTERM)     

    if event == "SHUTDOWN":
        print("Suhtting down...")
        if process:
            process.stdout.close()
            process.send_signal(signal.SIGTERM)
        start(['sudo', 'shutdown', 'now'])

    if event == ui.WIN_CLOSED:
        start(['killall', 'python3'])
        if process:
            process.stdout.close()
            process.send_signal(signal.SIGTERM)
        break

    try: line = q.get_nowait()
    except Empty:
        continue
    else: print(line)

window.close()
