import os


line = '"let the demon take your soul"'
line2 = '"tonight, drinking Singha, malt liquor from, Thailand, and listening to, Wagner. I can’t believe that, he is not in, the other, room, or around the, corner, or alive, someplace, tonight. and he is, of course. as I am taken, by the sound of, him. and little goosebumps, run along, both of my, arms. then a, chill. he’s here, now."'

while True:
    print("1. eSpeak")
    print("2. Festival")
    print("3. FLite")
    choice = input("Select option:")

    if choice == "1":
        os.system('espeak -p 0 -a 120 -s 100 -v english-us -f monologi.txt')
    elif choice == "2":
        os.system('festival jam.txt --tts')
    elif choice == "3":
        os.system('flite --setf int_f0_target_mean=50 --setf duration_stretch=1.4 -voice kal16 -f jam.txt')
    elif choice == "4":
        os.system('spd-say -l en -p -100 -r -50 -i -40 {0}'.format(line2))
    elif choice == "5":
        os.system('pico2wave -w test.wav {0} && aplay test.wav'.format(line2))
