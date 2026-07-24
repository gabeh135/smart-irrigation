#include <Arduino.h>
#include "esp_sleep.h"

const int sensorPin = 17;
const int sensorPowerPin = 18;

const int samples = 20;

void setup() {
  Serial.begin(115200);

  pinMode(sensorPowerPin, OUTPUT);
  digitalWrite(sensorPowerPin, HIGH);

  delay(1000);

  int total = 0;

  for (int i = 0; i < samples; i++) {
    total += analogRead(sensorPin);
    delay(50);
  }

  float average = total / (float)samples;

  Serial.print("Average moisture reading: ");
  Serial.println(average);

  digitalWrite(sensorPowerPin, LOW);

  Serial.println("Sleeping...");

  delay(100);

  esp_sleep_enable_timer_wakeup(60 * 1000000);
  esp_deep_sleep_start();
}

void loop() {
}