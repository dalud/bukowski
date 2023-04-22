#include <AccelStepper.h>

AccelStepper shoulder(1, 10, 11);
int sh = -3000;
AccelStepper spreader(1, 8, 9);
int sp = 2000;
AccelStepper elbow(1, 12, 13);
int e = 3000;
int speedo = 2000;
int accel = 1500;
int speedo_elbow = 20000;

int sip = 2;
int tap = 3;
int tukos = 4;
int nielu = 6;

String command;

bool logita;
bool debug;
char poses[] = { '1', '2', '3', '4', '5', '6', '7' };
int kiekka = 0;
int maxi;


void setup() {
  Serial.begin(9600);

  // Drink
  pinMode(sip, OUTPUT);
  digitalWrite(sip, HIGH);
  pinMode(tap, OUTPUT);
  digitalWrite(tap, HIGH);
  pinMode(tukos, OUTPUT);
  digitalWrite(tukos, HIGH);
  pinMode(nielu, OUTPUT);
  digitalWrite(nielu, HIGH);

  // Built in LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  
  // activate debug logging
  logita = false;
  // kiekka < maxi = loop speed
  // with log, set kiekka lower
  if(logita) {
    maxi = 1000;
  } else maxi = 10000;

  // Run in debug mode
  debug = true;
  //debug = false;

  //Stepper parameters
  //setting up some default values for maximum speed and maximum acceleration
  shoulder.setMaxSpeed(5000); //SPEED = Steps / second  
  shoulder.setAcceleration(accel); //ACCELERATION = Steps /(second)^2    
  shoulder.setSpeed(speedo);
  
  spreader.setMaxSpeed(5000); //SPEED = Steps / second  
  spreader.setAcceleration(accel); //ACCELERATION = Steps /(second)^2    
  spreader.setSpeed(speedo);

  elbow.setMaxSpeed(speedo_elbow); //SPEED = Steps / second  
  elbow.setAcceleration(accel); //ACCELERATION = Steps /(second)^2    
  elbow.setSpeed(speedo_elbow);
  
  delay(500);
  //---------------------------------------------------------------------------
}

void loop() {
  kiekka++;  
  // Debug mode using serial commands
  if(debug) {
    if (Serial.available()) {
      command = Serial.readStringUntil('\n');
    }
  }
  
  // Auto mode
  if(!debug) {
    if(digitalRead(2)) {
      digitalWrite(LED_BUILTIN, HIGH);
  
      if(kiekka>maxi) {    
        command = poses[random(sizeof(poses))];
        kiekka = 0;
      }
    } else {
      digitalWrite(LED_BUILTIN, LOW);
      command = "z";
    }
  }


  if(logita) {
    //Serial.print(digitalRead(2));
    //Serial.println(": " +command);
  }

  // Reset
  if(command == "z" || command == "0") {
    zeroMotors();
  }
  
  // Manual arm positioning 
  if(command.startsWith("sh")) { // Hail
    if(logita) Serial.println(shoulder.currentPosition());
    // Custom position
    if(command.length() > 2) shoulder.moveTo(command.substring(2).toInt());
    // Default max
    else shoulder.moveTo(sh);
    shoulder.run();
  }
  if(command.startsWith("sp")) { // Spreader
    if(logita) Serial.println(spreader.currentPosition());
    if(command.length() > 2) spreader.moveTo(command.substring(2).toInt());
    else spreader.moveTo(sp);
    spreader.run();    
  }
  if(command.startsWith("e")) { // Elbow
    if(logita) Serial.println(elbow.currentPosition());
    if(command.length() > 1) elbow.moveTo(command.substring(1).toInt());
    else elbow.moveTo(e);
    elbow.run();
  }

  // Others, letkusto
  if(command == "d") { // Drink
    drink();
  }
  if(command == "f") { // Fill tuoppi
    fill();
  }
  if(command == "n") { // Nielu
    fillNielu();
  }

  // Set arm poses
  if(command == "1") { // Poses
    pose(1);
  }
  if(command == "2") {
    // pose(2); // Älä riko lasia
  }
  if(command == "3") {
    pose(3);
  } 
  if(command == "4") {
    // pose(4);
  }
  if(command == "5") {
    pose(5);
  }
  if(command == "6") {
    pose(6);
  }
  if(command == "7") {
    pose(7);
  }
  if(command == "8") {
    pose(8);
  }
}

void zeroMotors() {
  shoulder.moveTo(0);
  shoulder.run();
  spreader.moveTo(0);
  spreader.run();
  elbow.moveTo(0);
  elbow.run();
}

void pose(int pose) {
  switch(pose) {
    // Rewrite poses 1-7 as appropriate
    case 1:
      shoulder.moveTo(sh);
      shoulder.run();
      spreader.moveTo(0);
      spreader.run();
      elbow.moveTo(0);
      elbow.run();
      break;
    case 2:
      shoulder.moveTo(0);
      shoulder.run();
      spreader.moveTo(sp);
      spreader.run();
      elbow.moveTo(0);
      elbow.run();
      break;
    case 3:
      shoulder.moveTo(0);
      shoulder.run();
      spreader.moveTo(0);
      spreader.run();
      elbow.moveTo(e);
      elbow.run();
      break;
    case 4:
      shoulder.moveTo(sh);
      shoulder.run();
      spreader.moveTo(sp);
      spreader.run();
      elbow.moveTo(0);
      elbow.run();
      break;
    case 5:
      shoulder.moveTo(sh);
      shoulder.run();
      spreader.moveTo(0);
      spreader.run();
      elbow.moveTo(e);
      elbow.run();
      break;
    case 6:
      shoulder.moveTo(0);
      shoulder.run();
      spreader.moveTo(sp);
      spreader.run();
      elbow.moveTo(e);
      elbow.run();
      break;
    case 7:
      shoulder.moveTo(sh);
      shoulder.run();
      spreader.moveTo(sp);
      spreader.run();
      elbow.moveTo(e);
      elbow.run();
      break;
    case 8: // Fill 'er up
      shoulder.moveTo(-2000); // -3000 current max
      shoulder.run();
      spreader.moveTo(0);
      spreader.run();
      elbow.moveTo(2000); // 3000
      elbow.run();
      break;
  }
}

void drink() {
    digitalWrite(sip, LOW);
    delay(5000);
    digitalWrite(sip, HIGH);
    command = "";
}

void fill() {
    digitalWrite(tap, LOW);
    delay(3000);
    digitalWrite(tap, HIGH);
    command = "";
}

void block() {
    digitalWrite(tukos, LOW);
    digitalWrite(nielu, LOW);
    delay(1000);
    digitalWrite(tukos, HIGH);
    digitalWrite(nielu, HIGH);
    command = "";
}

void fillNielu() {
  digitalWrite(tukos, LOW);
  digitalWrite(nielu, LOW);
  digitalWrite(tap, LOW);
  delay(4000);
  digitalWrite(tukos, HIGH);
  digitalWrite(nielu, HIGH);
  digitalWrite(tap, HIGH);
  command = "";
}
