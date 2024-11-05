#include <AFMotor.h>

AF_DCMotor silmat(1);
AF_DCMotor suu(2);
AF_DCMotor luomet(3);

byte input = A0;
int alea; // Silmä arpa
byte dir; // Silmien suunta
int counter; // Universal counter
int suun_suunta = 1;
int luomien_suunta = 1;


void setup() {
  Serial.begin(9600);

  counter = 0;
  alea = 0;

  dir = FORWARD;

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  
  // Suu Input signal0
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
  if(counter > 150) {
    liikutaSilmia(alea);
    long stop = random(155, 250);
        if(counter > stop) {
      liikutaSilmia(0);
      counter = 0;
      alea = 0;
      suun_suunta = random(1,3);
    }
  }

  // Suu input handling
  if(digitalRead(input)) {
    suu.setSpeed(random(10,70));
    suu.run(suun_suunta);
    digitalWrite(LED_BUILTIN, HIGH);
    // Luomet arvonta
    if(random(200) < 1) liikutaLuomia();

    delay(10);
  } else {
    suu.run(RELEASE);
    digitalWrite(LED_BUILTIN, LOW);
    delay(10);
  }
  
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
  if (luomien_suunta == 1) luomien_suunta = 2;
  else luomien_suunta = 1;
  luomet.run(luomien_suunta);
  delay(random(500, 800));
  luomet.run(RELEASE);
  delay(10);
}
