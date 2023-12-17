#include <AFMotor.h>

AF_DCMotor silmat(1); // Silmät
AF_DCMotor suu(2); // Suu

byte input = A0;
int alea; // Silmä arpa
byte dir; // Silmien suunta
int counter; // Universal counter


void setup() {
  Serial.begin(9600);

  counter = 0;
  alea = 0;
  dir = FORWARD;

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  
  // Suu Input signal
  pinMode(input, INPUT);

  silmat.setSpeed(255);
  suu.setSpeed(255);
  
  silmat.run(RELEASE);
  suu.run(RELEASE);
  delay(500);
}

void loop() {
  counter++;
  //Serial.println(counter);

  // Silmä arpa
  if(!alea) alea = random(2);
  //Serial.println(alea);
  if(counter > 75) {
    liikutaSilmia(alea);
    long stop = random(80, 200);
        if(counter > stop) {
      liikutaSilmia(0);
      counter = 0;
      alea = 0;
    }
  }

  // Suu input handling
  if(digitalRead(input)) {
    suu.run(FORWARD);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(10);
  } else {
    suu.run(RELEASE);
    digitalWrite(LED_BUILTIN, LOW);
    delay(10);
  }
  
  //silmat.run(FORWARD);
  //suu.run(FORWARD);
  delay(10);
}

void liikutaSilmia(long alea) {
  switch(alea) {
    case 1:
      silmat.run(dir);
      //else silmat.run(BACKWARD);
      digitalWrite(LED_BUILTIN, HIGH);
      break;
    default:
      silmat.run(RELEASE);
      if(random(2)) dir = FORWARD;
      else dir = BACKWARD;
      digitalWrite(LED_BUILTIN, LOW);
      break;
  }
}
