void setup() {
  Serial.begin(9600);
  pinMode(A1, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // Serial.println("t");
  digitalWrite(A1, HIGH);
  digitalWrite(LED_BUILTIN, HIGH);
}
