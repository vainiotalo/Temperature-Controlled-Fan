#include <OneWire.h>
#include <DallasTemperature.h>

/*
Libraries available at
https://github.com/PaulStoffregen/OneWire
https://github.com/milesburton/Arduino-Temperature-Control-Library

Tempereture Controlled ON/OFF fan using a 2-wire 12V DC fan and DS18B20 temperature sensor
*/

#define ONE_WIRE_BUS 5 // Set up sensor data on pin 5

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

int Relay = 7; // Relay pin
float temp = 0;
float tempMax = 25.0; // Switch on the relay
boolean newValueChange = true;

void setup() {
  Serial.begin(9600);
  pinMode(Relay, OUTPUT); // Used relay is active-low
  digitalWrite(Relay, HIGH); // Relay switched off by default using input HIGH
  sensors.begin();
}

void loop() {
  temp = readTemp();
  delay(1000);
  receiveControllerCommand(); // Check if tempMax value has been changed
  replyToController();
  
  Serial.print("Temperature: `");
  Serial.print(temp);
  Serial.print("' C \n");
  
  if(temp > tempMax) { // If temp is higher than tempMax,
    digitalWrite(Relay, LOW); // switch on the relay
  } else {
    digitalWrite(Relay, HIGH);
  }
}

float readTemp(){
  sensors.requestTemperatures(); // Request temperature from sensor
  temp = sensors.getTempCByIndex(0); // Temperature in Celsius
  return temp;
}

void receiveControllerCommand(){
  char x = Serial.read();
  if(x == '+') {
    newValueChange = true;
    tempMax++;
  }
  if(x == '-'){
    newValueChange = true;
    tempMax--;
  }
}

void replyToController(){
  if(newValueChange){
    newValueChange = false;
    Serial.print("<");
    Serial.print(tempMax);
    Serial.print(">");
  }
}
