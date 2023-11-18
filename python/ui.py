#!/usr/bin/env python

import PySimpleGUI as ui
import subprocess
import sys
import os
from threading import Thread
from queue import Queue, Empty
import signal
from delayedPrint_IF import DelayedPrint

# Utils
process = None
ON_POSIX = 'posix' in sys.builtin_module_names
q = Queue()
printer = DelayedPrint()

def enqueue_output(out, queue):
    for line in iter(out.readline, ''):
        queue.put(line)
    out.close()

# Build UI
layout = [ui.Button("RUN", button_color="green on black"), ui.Button("STOP", button_color="red on black"), ui.Button("EXIT", button_color="grey on black")], [ui.Multiline(reroute_stdout=True, reroute_stderr=True, auto_refresh=True, autoscroll=True, expand_x=True, expand_y=True, no_scrollbar=True, background_color="black", text_color="green")]
window = ui.Window("Robohemian: Bukowski", layout, size=(1024, 600), font="BohemianTypewriter 40", default_button_element_size=(5, 2), button_color="black", auto_size_buttons=False, resizable=True, background_color="black")
#font="DisposableDroidBB 48 bold"

# Helpers
def start(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1, close_fds=ON_POSIX) #stderr=subprocess.STDOUT, 
    t = Thread(target=enqueue_output, args=(process.stdout, q))
    t.daemon = True
    t.start()

# Main loop
while True:
    event, values = window.read(10)
    window.maximize()
    window.TKroot["cursor"] = "none"
    
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

    if event == "EXIT":
        print("Shutting down...")
        if process:
            process.stdout.close()
            process.send_signal(signal.SIGTERM)
        #start(['sudo', 'shutdown', 'now'])
        window.close()

    if event == ui.WIN_CLOSED:
        start(['killall', 'python3'])
        if process:
            process.stdout.close()
            process.send_signal(signal.SIGTERM)
        break

    try: line = q.get_nowait()
    except Empty:
        if not printer.isPrinting():
            continue
    if ":msg:" in line and not printer.isPrinting():
        printer.print(line.split(":msg:")[1])
    else: print(line)

window.close()
