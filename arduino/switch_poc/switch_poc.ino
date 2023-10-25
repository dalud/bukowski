#include <AccelStepper.h>

// constants won't change. They're used here to set pin numbers:
const int buttonPin = 12;  // the number of the pushbutton pin
const int ledPin = 13;    // the number of the LED pin

// variables will change:
int buttonState = 0;  // variable for reading the pushbutton status

AccelStepper elbow(AccelStepper::FULL4WIRE, 2, 3, 4, 5, true); 

void setup() {
  Serial.begin(9600);
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
}

void loop() {
  elbow.moveTo(1000);
  
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);
  //Serial.println(buttonState);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
    elbow.run();
  } else {
    // turn LED off:
    digitalWrite(ledPin, LOW);
    elbow.stop();
  }
}
