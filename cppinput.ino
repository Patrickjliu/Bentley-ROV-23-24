const int joyXPin = A0;
const int joyYPin = A1;

void setup() {
  Serial.begin(9600);
  pinMode(joyXPin, INPUT);
  pinMode(joyYPin, INPUT);
}

void loop() {
  float xValue = analogRead(joyXPin);
  float yValue = analogRead(joyYPin);

  Serial.write(&xValue, sizeof(float));
  Serial.write(&yValue, sizeof(float));

  delay(100);
}