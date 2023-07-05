# contrib-digi-lockers
For Vamanit Digital Locker Training

# **Vamanit Locker (Board: ESP32)**

### Application Required
[Arduino IDE](https://www.arduino.cc/en/software)

### Libraries Used: 
- Modbus TCP
    ```
    name=modbus-esp8266
    version=4.0.0-DEV
    author=Andre Sarmento Barbosa, Alexander Emelianov
    maintainer=Alexander Emelianov<a.m.emelianov@gmail.com>
    sentence=Modbus Library for Arduino. ModbusRTU, ModbusTCP and ModbusTCP Security
    category=Communication
    url=https://github.com/emelianov/modbus-esp8266
    ```

> Install using arduino library manager


In your Arduino IDE, go to **Sketch** > **Include Library** > **Manage Libraries**


### Steps to Upload the Code: 

> Add ESP32 board in arduino software 

In your Arduino IDE, go to **File** > **Preferences** 

Enter [https://dl.espressif.com/dl/package_esp32_index.json](https://dl.espressif.com/dl/package_esp32_index.json) into the **Additional Board Manager URLs**. Then, click the **OK** button 

Open the Boards Manager. Go to **Tools** > **Board** > **Boards Manager** 

Search for ESP32 and press install button for the **ESP32 by Espressif Systems** 

Install version 3.2.2


> Modify WiFI details in code

```cpp

//wifi settings 

const char* ssid = "WiFi ssid"; 

const char* password =  "password"; 



// it will set the static IP address 

IPAddress local_IP(192, 168, 100, 6); 

//it wil set the gateway static IP address 

IPAddress gateway(192, 168, 100, 100); 



// Following three settings are optional 

IPAddress subnet(255, 255, 255, 0); 

IPAddress primaryDNS(192, 168, 100, 42); 

IPAddress secondaryDNS(8, 8, 8, 8); 
```
 

> Uploading the code to ESP32 board 

Connect board to the system using USB  

Select your Board in **Tools** > **Board** menu 

Select the **Port**  

Press the Upload button in the Arduino IDE. Wait a few seconds while the code compiles and uploads to your board. 

---
### Features
```diff
+ Modbus TCP
- Wifi Setup at Boot
- Modbus TCP Security
- Weighting package
```