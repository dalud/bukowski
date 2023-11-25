#include <AccelStepper.h>
#include <SharpIR.h>


// Käden moottorit
AccelStepper shoulder(1, 10, 11);
int sh = -2600;
AccelStepper spreader(1, 8, 9);
int sp = 2700;
AccelStepper elbow(1, 12, 13);
int e = 5000;
AccelStepper wrist(1, 22, 23);
int w = 3000;
int speedo = 2000;
int accel = 1500;
int speedo_elbow = 20000;

// Pumput, venttiilit etc.
int sip = 2; // Galley pump (1.)
int tap = 3; // Pilge pump (2.)
int tukos = 4; // 24V valve
int nielu = 5; // 12V valve
int suu = 6; 
int kusi = 7; // Mahan kääntäjä
int silmat = 18;
int eks = 31; // Elbow kill switch (positive), alarm = 5500
int eks2 = 32; // Alarm = -400
int spks = 34; // Spreader kill switch (positive), alarm = 2700
int spks2 = 33; // Alarm = -200
int shks = 35; // Shoulder kill switch (negative), alarm = -2700
int shks2 = 36; // Alarm = 1000
int lasi = 45; // Veden taso lasissa -hälytys

SharpIR hanasilma( SharpIR::GP2Y0A41SK0F, A0 );

String command;

char poses[] = { '1', '2', '3', '4', '5', '6', '7' };

int counter; // Universal counter
int alea; // Silmä arpa


void setup() {
  Serial.begin(9600);

  counter = 0;
  alea = 0;

  // Outputs
  pinMode(sip, OUTPUT);
  digitalWrite(sip, HIGH);
  pinMode(tap, OUTPUT);
  digitalWrite(tap, HIGH);
  pinMode(tukos, OUTPUT);
  digitalWrite(tukos, HIGH);
  pinMode(nielu, OUTPUT);
  digitalWrite(nielu, HIGH);
  pinMode(kusi, OUTPUT);
  digitalWrite(kusi, HIGH);
  pinMode(suu, OUTPUT);
  digitalWrite(suu, HIGH);
  pinMode(silmat, OUTPUT);
  digitalWrite(silmat, HIGH);
  
  // Inputs
  pinMode(eks, INPUT);
  pinMode(eks2, INPUT);
  pinMode(spks, INPUT);
  pinMode(spks2, INPUT);
  pinMode(shks, INPUT);
  pinMode(shks2, INPUT);
  pinMode(lasi, INPUT);
  
  // Built in LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  
  //Stepper parameters
  shoulder.setMaxSpeed(5000); //SPEED = Steps / second  
  shoulder.setAcceleration(accel); //ACCELERATION = Steps /(second)^2    
  shoulder.setSpeed(speedo);
  
  spreader.setMaxSpeed(5000); //SPEED = Steps / second  
  spreader.setAcceleration(accel); //ACCELERATION = Steps /(second)^2    
  spreader.setSpeed(speedo);

  elbow.setMaxSpeed(speedo_elbow); //SPEED = Steps / second  
  elbow.setAcceleration(accel); //ACCELERATION = Steps /(second)^2    
  elbow.setSpeed(speedo_elbow);

  wrist.setMaxSpeed(5000); //SPEED = Steps / second  
  wrist.setAcceleration(accel); //ACCELERATION = Steps /(second)^2    
  wrist.setSpeed(speedo);
  
  delay(500);
}


void loop() {
  counter++;
  //Serial.write(counter);

  // Kill switch checks
  if(digitalRead(eks)) fixElbow(1);
  if(digitalRead(eks2)) fixElbow(0);
  if(digitalRead(spks)) fixSpreader(1);
  if(digitalRead(spks2)) fixSpreader(0);
  if(digitalRead(shks)) fixShoulder(0);
  if(digitalRead(shks2)) fixShoulder(1);

  // Lasin tilanne
  // Serial.println(digitalRead(lasi));
  if(digitalRead(lasi)) fillerUp();
  
  // Silmä arpa
  if(!alea) alea = random(3);
  
  if(counter > 7500) {
    liikutaSilmia(alea);
    
    if(counter > 10000) {
      liikutaSilmia(0);
      counter = 0;
      alea = 0;
    }
  }

  // Read command from Serial Bus
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
  }
  
  // Reset
  if(command == "z" || command == "0") {
    zeroMotors();
  }
  
  // Manual arm positioning 
  if(command.startsWith("sh")) { // Hail
    // Shoulder dir is negative
    // Custom position
    if(command.length() > 2) shoulder.moveTo(command.substring(2).toInt());
    // Default max
    else shoulder.moveTo(sh);
    shoulder.run();
  }
  if(command.startsWith("sp")) { // Spreader
    if(command.length() > 2) spreader.moveTo(command.substring(2).toInt());
    else spreader.moveTo(sp);
    spreader.run();    
  }
  if(command.startsWith("e")) { // Elbow
    if(command.length() > 1) elbow.moveTo(command.substring(1).toInt());
    else elbow.moveTo(e);
    elbow.run();
  }
  if(command.startsWith("w")) { // Wrist
    if(command.length() > 1) wrist.moveTo(command.substring(1).toInt());
    else wrist.moveTo(w);
    wrist.run();
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
  if(command == "h") { // Heiluttelu
    heiluttelu();
  }

  if(command == "k") { // Kuse
    kuse();
  }

  if(command.startsWith("p")) { // Puhu/suu
    if(command.length() > 1) liikutaSuuta(command.substring(1).toInt());
  }

  if(command == "s") {
    digitalWrite(silmat, LOW);
  }

  // Set arm poses
  if(command == "1") { // Perus tuoppi lepo
    pose(1);
  }
  if(command == "2") { // Juoma asento
    pose(2);
  }
  if(command == "3") { // Juoma 2
    pose(3);
  } 
  if(command == "4") { // Skol!
    pose(4);
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
  if(command == "8") { // Fill
    pose(8);
  }
  // TODO: default to 1 (in Rasp?)
}

void zeroMotors() {
  shoulder.moveTo(0);
  shoulder.run();
  spreader.moveTo(0);
  spreader.run();
  elbow.moveTo(0);
  elbow.run();
  wrist.moveTo(0);
  wrist.run();
  digitalWrite(suu, HIGH);
  digitalWrite(silmat, HIGH);
  // TODO: add all others
}

void pose(int pose) {
  switch(pose) {
    // Rewrite poses 1-7 as appropriate 
    case 1: // Tuoppi lepo
      shoulder.moveTo(0);
      shoulder.run();
      spreader.moveTo(0);
      spreader.run();
      elbow.moveTo(3500);
      elbow.run();
      wrist.moveTo(0);
      wrist.run();
      break;
    case 2: // Sip
      shoulder.moveTo(0);
      shoulder.run();
      spreader.moveTo(1000);
      spreader.run();
      elbow.moveTo(5000);
      elbow.run();
      wrist.moveTo(-500);
      wrist.run();
      break;
    case 3: // Sip 2
      shoulder.moveTo(1000);
      shoulder.run();
      spreader.moveTo(500);
      spreader.run();
      elbow.moveTo(5000);
      elbow.run();
      wrist.moveTo(0);
      wrist.run();
      break;
    case 4: // Skol!
      shoulder.moveTo(-2500);
      shoulder.run();
      spreader.moveTo(500);
      spreader.run();
      elbow.moveTo(3000);
      elbow.run();
      wrist.moveTo(-400);
      wrist.run();
      break;
    case 5:
      shoulder.moveTo(0);
      shoulder.run();
      spreader.moveTo(0);
      spreader.run();
      elbow.moveTo(0);
      elbow.run();
      wrist.moveTo(0);
      wrist.run();
      break;
    case 6:
      shoulder.moveTo(0);
      shoulder.run();
      spreader.moveTo(0);
      spreader.run();
      elbow.moveTo(0);
      elbow.run();
      wrist.moveTo(0);
      wrist.run();
      break;
    case 7:
      shoulder.moveTo(0);
      shoulder.run();
      spreader.moveTo(0);
      spreader.run();
      elbow.moveTo(0);
      elbow.run();
      wrist.moveTo(0);
      wrist.run();
      break;
    case 8: // Fill 'er up
      shoulder.moveTo(-2500);
      shoulder.run();
      spreader.moveTo(500);
      spreader.run();
      elbow.moveTo(1000);
      elbow.run();
      wrist.moveTo(-250);
      wrist.run();
      break;
  }
}

void drink() {
    digitalWrite(sip, LOW);
    digitalWrite(suu, LOW);
    delay(5000);
    digitalWrite(sip, HIGH);
    digitalWrite(suu, HIGH);
    command = "";
}

void fill() {
    digitalWrite(tap, LOW);
    delay(6000);
    digitalWrite(tap, HIGH);
    command = "";
}

void fillNielu() {
  digitalWrite(tukos, LOW);
  digitalWrite(nielu, LOW);
  digitalWrite(tap, LOW);
  delay(5000);
  digitalWrite(tukos, HIGH);
  digitalWrite(nielu, HIGH);
  digitalWrite(tap, HIGH);
  command = "";
}

void kuse() {
  digitalWrite(kusi, LOW);
  delay(6000);
  digitalWrite(kusi, HIGH);
  delay(100);
  command = "";
}

void liikutaSuuta(int amp) {
  if(amp) {
    digitalWrite(suu, LOW);
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(suu, HIGH);
    digitalWrite(LED_BUILTIN, LOW);
  }
}

// Ongoing "h" from command center for x seconds
int heiluKiekka=0;
int heiluMax=5000;
void heiluttelu() {
  heiluKiekka++;
  if(heiluKiekka<heiluMax) wrist.moveTo(500);
  if(heiluKiekka>heiluMax) wrist.moveTo(-500);
  if(heiluKiekka>heiluMax*2) heiluKiekka=0;
  wrist.run();
}

void liikutaSilmia(long alea) {
  switch(alea) {
    case 1:
      digitalWrite(silmat, LOW);
      break;
    default:
      digitalWrite(silmat, HIGH);
      break;
  }
}

void fixShoulder(int direction) {
  if(direction) {
    command = "";
    shoulder.stop();
    shoulder.setCurrentPosition(1000);
    shoulder.moveTo(0);
    while(digitalRead(shks2)) shoulder.run();
  } else {
    command = "";
    shoulder.stop();
    shoulder.setCurrentPosition(-2600);
    shoulder.moveTo(0);
    while(digitalRead(shks)) shoulder.run();
  }
}

void fixSpreader(int direction) {
  if(direction) {
    command = "";
    spreader.stop();
    spreader.setCurrentPosition(2700);
    spreader.moveTo(0);

    while(digitalRead(spks)) spreader.run();
  } else {
    command = "";
    spreader.stop();
    spreader.setCurrentPosition(-200);
    spreader.moveTo(0);

    while(digitalRead(spks2)) spreader.run();
  }
}

void fixElbow(int direction) {
  if(direction) { // Positive
    command = "";
    elbow.stop();
    elbow.setCurrentPosition(5000);
    elbow.moveTo(0);

    while(digitalRead(eks)) elbow.run();
  } else { // Negative
    command = "";
    elbow.stop();
    elbow.setCurrentPosition(-400);
    elbow.moveTo(0);

    while(digitalRead(eks2)) elbow.run();
  }
}

void fillerUp() {
  Serial.println("Nytkö?");
  delay(500);
  if(digitalRead(lasi)) {
    Serial.println("Nyt!");
    Serial.println("t");
    while(hanasilma.getDistance() > 3) pose(8);
    Serial.println("Nyt ois lasi paikoillaan...");
  }
}
