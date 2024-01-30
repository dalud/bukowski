#include <AFMotor.h>

AF_DCMotor silmat(1);
AF_DCMotor suu(2);
AF_DCMotor luomet(3);

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

  silmat.setSpeed(30);
  suu.setSpeed(30);
  luomet.setSpeed(70);
  
  silmat.run(RELEASE);
  suu.run(RELEASE);
  luomet.run(RELEASE);

  delay(500);
}

void loop() {
  counter++;
  //Serial.println(counter);

  // Silmä arpa
  if(!alea) alea = random(2);
  if(counter > 100) {
    liikutaSilmia(alea);
    long stop = random(105, 200);
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

  // Luomet arvonta
  if(random(300) < 1) liikutaLuomia();
  
  delay(10);
}

void liikutaSilmia(long alea) {
  switch(alea) {
    case 1:
      silmat.run(dir);
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

void liikutaLuomia() {
  luomet.run(FORWARD);
  delay(700);
  luomet.run(RELEASE);
  delay(10);
}
