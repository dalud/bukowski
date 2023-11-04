#include <AccelStepper.h>

const int buttonPin = 2;  // the number of the pushbutton pin
const int buttonPin2 = 3;
const int ledPin = 13;    // the number of the LED pin

int buttonState = 0;  // variable for reading the pushbutton status
int buttonState2 = 0;


void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT);
  pinMode(buttonPin2, INPUT);
}

void loop() {
  buttonState = digitalRead(buttonPin);
  buttonState2 = digitalRead(buttonPin2);
  Serial.print("switch1: ");
  Serial.println(buttonState);
  Serial.print("switch2: ");
  Serial.println(buttonState2);

  if ((buttonState == HIGH) ||(buttonState2 == HIGH)) {
    digitalWrite(ledPin, HIGH);
    //Serial.println("t");
  } else {
    digitalWrite(ledPin, LOW);
  }
}
