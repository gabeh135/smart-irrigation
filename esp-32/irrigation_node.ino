#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "esp_sleep.h"

const int sensorPin = 17;
const int sensorPowerPin = 18;

const int samples = 20;

const float ADC_MAX = 4095.0;
const float ADC_VREF = 3.3;

const unsigned long CONNECT_TIMEOUT_MS = 15000;

const char* ssid = "WIFI_NAME";
const char* password = "WIFI_PASSWORD";

const char* mqtt_server = "MQTT_HOSTNAME";

WiFiClient espClient;
PubSubClient mqtt(espClient);

bool connectWiFi() {
  WiFi.begin(ssid, password);

  unsigned long start = millis();

  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - start > CONNECT_TIMEOUT_MS) {
      return false;
    }
    delay(500);
  }

  return true;
}

bool connectMQTT() {
  unsigned long start = millis();

  while (!mqtt.connected()) {
    mqtt.connect("soil_sensor");

    if (millis() - start > CONNECT_TIMEOUT_MS) {
      return false;
    }
    delay(500);
  }

  return true;
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
  float voltage = average * ADC_VREF / ADC_MAX;

  digitalWrite(sensorPowerPin, LOW);

  if (connectWiFi()) {
    mqtt.setServer(mqtt_server, 1883);

    if (connectMQTT()) {
      char payload[50];
      snprintf(payload, sizeof(payload), "{\"moisture\":%.3f}", voltage);

      mqtt.publish("yard/moisture", payload);
      mqtt.disconnect();
    }

    WiFi.disconnect(true);
  }

  esp_sleep_enable_timer_wakeup(60 * 1000000);
  esp_deep_sleep_start();
}

void loop() {
}