#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "esp_sleep.h"

const int sensorPin = 17;
const int sensorPowerPin = 18;

const int samples = 20;

const char* ssid = "WIFI_NAME";
const char* password = "WIFI_PASSWORD";

const char* mqtt_server = "MQTT_HOSTNAME";

WiFiClient espClient;
PubSubClient mqtt(espClient);

void connectWiFi() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void connectMQTT() {
  while (!mqtt.connected()) {
    mqtt.connect("soil_sensor");
    delay(500);
  }
}

void setup() {
  pinMode(sensorPowerPin, OUTPUT);
  digitalWrite(sensorPowerPin, HIGH);

  delay(1000);

  int total = 0;

  for (int i = 0; i < samples; i++) {
    total += analogRead(sensorPin);
    delay(50);
  }

  float average = total / (float)samples;

  digitalWrite(sensorPowerPin, LOW);

  connectWiFi();

  mqtt.setServer(mqtt_server, 1883);
  connectMQTT();

  char payload[50];
  snprintf(payload, sizeof(payload), "{\"moisture\":%.2f}", average);

  mqtt.publish("yard/moisture", payload);

  mqtt.disconnect();
  WiFi.disconnect(true);

  esp_sleep_enable_timer_wakeup(60 * 1000000);
  esp_deep_sleep_start();
}

void loop() {
}