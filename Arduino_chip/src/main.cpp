/*  Vamanit Locker Code
    Board ESP8266 12E
    Communication using Modbus TCP
    Controls 3 Relays - Lockers

    Inbuilt LED works on Inverted Logic, same as Relay Control Board
*/

#include <Arduino.h>

//esp8266 modbus tcp
#ifdef ESP8266
  #include <ESP8266WiFi.h>
#else //ESP32
  #include <WiFi.h>
#endif
#include <ModbusIP_ESP8266.h>

// #include "Arduino.h"

//-----------------------------------wifi configuration -----------------------------------------------

//wifi settings
const char* ssid = "Workbench Router";
const char* password =  "Teamw0rk@123";

// it wil set the static IP address
IPAddress local_IP(192, 168, 100, 6);
//it wil set the gateway static IP address
IPAddress gateway(192, 168, 100, 100);

// Following three settings are optional
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(192, 168, 100, 42);
IPAddress secondaryDNS(8, 8, 8, 8);

//Modbus Registers Offsets
const int L1_COIL = 100;
const int L2_COIL = 101;
const int L3_COIL = 102;

//input register
const int Weight_Irg = 200;

//Locker Pins
const int LOCKER1 = 15;
const int LOCKER2 = 16;
const int LOCKER3 = 17;

//Switch Pins
const int L1SWITCH = 18;
const int L2SWITCH = 19;
const int L3SWITCH = 21;

//ModbusIP object
ModbusIP mb;
int  L1State;
int  L2State;
int  L3State;

//-------------------------------------------void setup------------------------------------------------------------

void setup() {
  Serial.begin(9600);

  //-------------------------------------WiFi Configuration With Static IP-------------------------------------------

  // This part of code will try create static IP address
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("STA Failed to configure");
  }
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  //  Modbus Server
  mb.server();
  //--------------------------------------------IN/OUT-----------------------------------------------------------------

  //Locker PinMode
  pinMode(LOCKER1 , OUTPUT);
  pinMode(LOCKER2 , OUTPUT);
  pinMode(LOCKER3 , OUTPUT);

  digitalWrite(LOCKER1,HIGH);
  digitalWrite(LOCKER2,HIGH);
  digitalWrite(LOCKER3,HIGH);

  //Switch PinMode
  pinMode(L1SWITCH , INPUT);
  pinMode(L2SWITCH , INPUT);
  pinMode(L3SWITCH , INPUT);

  //Reading Coil
  mb.addCoil(L1_COIL);
  mb.addCoil(L2_COIL);
  mb.addCoil(L3_COIL);

}


bool FLAG = true;
unsigned long previousMillis;

void loop() {

  // --------------------------------Locker and switch logic--------------------------------------------------------

  //Call once inside loop()
  mb.task();

  //Getting State of Coils
  L1State = mb.Coil(L1_COIL);
  L2State = mb.Coil(L2_COIL);
  L3State = mb.Coil(L3_COIL);
  // --------------------------------------------Locker1--------------------------------------------------------

  if (L1State == 1) {
    // open lock
    digitalWrite(LOCKER1, LOW);
    //check for switch state to close door after 10 seconds
    unsigned long currentMillis = millis();
    if (FLAG) {
      previousMillis = currentMillis;
      FLAG = false;
    }
    if (currentMillis - previousMillis >= 10000) {
        // close the lock
        digitalWrite(LOCKER1, HIGH);
      // check for switch state to close the lock
      if (digitalRead(L1SWITCH) == 0) {
        // close the lock
        // digitalWrite(LOCKER1, HIGH);
        // change the flag state to true
        FLAG = true;
        //change the coil state
        mb.Coil(L1_COIL, false);
      }
    }
  }

  // --------------------------------------------Locker2-------------------------------------------------------

  else if (L2State == 1) {
    digitalWrite(LOCKER2, LOW);
    //check for switch state to close door after 10 seconds
    unsigned long currentMillis = millis();
    if (FLAG) {
      previousMillis = currentMillis;
      FLAG = false;
    }
    if (currentMillis - previousMillis >= 10000) {
        // close the lock
        digitalWrite(LOCKER2, HIGH);
      // check for switch state to close the lock
      if (digitalRead(L2SWITCH) == 0) {
        // close the lock
        // digitalWrite(LOCKER2, HIGH);
        // change the flag state to true
        FLAG = true;
        //change the coil state
        mb.Coil(L2_COIL, false);
      }
    }

  }
  // ----------------------------------------------Locker3-----------------------------------------------------

  else if (L3State == 1) {
    digitalWrite(LOCKER3, LOW);
    //check for switch state to close door after 10 seconds
    unsigned long currentMillis = millis();
    if (FLAG) {
      previousMillis = currentMillis;
      FLAG = false;
    }
    if (currentMillis - previousMillis >= 10000) {
        // close the lock
        digitalWrite(LOCKER3, HIGH);
      // check for switch state to close the lock
      if (digitalRead(L3SWITCH) == 0) {
        // close the lock
        // digitalWrite(LOCKER3, HIGH);
        // change the flag state to true
        FLAG = true;
        //change the coil state
        mb.Coil(L3_COIL, false);
      }
    }

  }

  // Print Status of Lockers
  Serial.println("Coil States:");
  Serial.println(L1State);
  Serial.println(L2State);
  Serial.println(L3State);
  delay(100);
}