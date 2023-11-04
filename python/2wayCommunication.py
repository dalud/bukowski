from arduinoIF import Arduino

arduino = Arduino()
arduino.connect()

while True:
    received = arduino.read()

    if received:
        print("Nyt tuli hommia:", received)
        if received == "t":
            print("Täyttö!")
    else:
        print("omiani tässä kattelen vaan...")
