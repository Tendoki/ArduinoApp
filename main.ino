#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <GSON.h>

#define ACC_LOGIN "greenhouse"
#define ACC_PASS "217643"
const int analogInPin = A0;
const int dsPin = D4;
const int relayPin = D3;
const char* ssid = "RT-WiFi-165";     
const char* password = "593872460"; 
const char* serverUrl = "http://yaroslav.homs.win/add";


WiFiClient wifiClient;

#include <Adafruit_AHTX0.h>
Adafruit_AHTX0 aht;

#include <BH1750.h>
BH1750 lightMeter;

#include <GyverDS18.h>
GyverDS18Single ds(dsPin,false);
uint16_t lux_target=65535;

void setup() {
  Serial.begin(115200);
  EEPROM.begin(512);

  if (EEPROM.read(0)!=64) {
    EEPROM.write(0, 64); 
    EEPROM.write(1, lux_target); 
    EEPROM.commit();
  }
  lux_target=EEPROM.read(1);
  
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);

  if (!aht.begin())                                 
  {                                    
    Serial.println("AHT Problem");   
    while (1) delay(10);                                       
  }

  lightMeter.begin();

  ds.requestTemp();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
}

sensors_event_t air_humidity, air_temp;
float lux;
float soil_temp=0;
int soil_humidity = 0;

uint32_t timer_send=0;

void loop() {
  lux = lightMeter.readLightLevel();
  if (lux<lux_target) {
    digitalWrite(relayPin, LOW);
  }else{
    digitalWrite(relayPin, HIGH);
  }

  if (WiFi.status() == WL_CONNECTED && millis()-timer_send>5000) {

    
    HTTPClient http;

    aht.getEvent(&air_humidity, &air_temp);
    soil_humidity = analogRead(analogInPin);
    soil_humidity=100.0-soil_humidity/10.24;
    
    if (ds.ready()) {         
        if (ds.readTemp()) { 
            soil_temp=ds.getTemp();
        } else {
            Serial.println("DS Problem");
        }
        ds.requestTemp();  
    }

    gson::string gs; 
    gs.beginObj();
    gs.addString("login", ACC_LOGIN);
    gs.addString("password", ACC_PASS);
    gs.addFloat(F("soil_temperature"), soil_temp);
    gs.addFloat(F("soil_humidity"), soil_humidity);
    gs.addFloat(F("air_temperature"), air_temp.temperature);
    gs.addFloat(F("air_humidity"), air_humidity.relative_humidity);
    gs.addFloat(F("light_intensity"), lux);
    gs.endObj();  
    gs.end();

    Serial.println(gs);

    http.begin(wifiClient,serverUrl);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(gs);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
      if (httpResponseCode==200 && response.toInt()!=lux_target) {
        lux_target=response.toInt();
        EEPROM.write(1, lux_target); 
        EEPROM.commit();
        Serial.println("Change lux to " +String(lux_target));
      }
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
    timer_send=millis();
  }
  

}
