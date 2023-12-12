#include <M5StickC.h>
#include <Arduino.h>
#include <WiFi.h>
#include <NTPClient.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

#define SSID "Your WIFI SSID"
#define PASSWORD "Your WIFI Password"
#define UUID "Set IoT Sensor UUID as you want"
#define DOMAIN_URL "Connection of Server URL"
#define MESSAGE_ROW 30

#define SET_MESSAGE(format, ...) \
    M5.Lcd.fillScreen(BLACK); \
    M5.Lcd.setCursor(0, 0); \
    M5.Lcd.setTextColor(BLUE); \
    M5.Lcd.printf("UUID: %s\n", UUID); \
    M5.Lcd.setCursor(0, MESSAGE_ROW); \
    M5.Lcd.setTextColor(WHITE); \
    M5.Lcd.printf(format, ##__VA_ARGS__)
void home_message();
void check_internet();
void record_IMU_data();
void send_IMU_data(const String msg);

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

String IMU_payload = "";
bool record_IMU_flag = false;

void setup()
{
  M5.begin();
  M5.Lcd.setRotation(3);
}

void loop()
{
  check_internet();
  M5.update();

  if (M5.BtnA.wasReleased())
  {
    M5.IMU.Init();
    record_IMU_flag = !record_IMU_flag;
    if (record_IMU_flag)
    {
      SET_MESSAGE("Recording IMU data......\n\nPress M5 button to stop recording");
      IMU_payload = "";
    }
    else
    {
      SET_MESSAGE("Saving record data......\n\nReturn after 3 seconds");
      delay(3000);
      home_message();
    }
  }

  if (record_IMU_flag)
  {
    record_IMU_data();
  }

  if (M5.BtnB.wasReleased() && !record_IMU_flag)
  {
    if (IMU_payload != "")
    {
      send_IMU_data();
      home_message();
    }
    else
    {
      SET_MESSAGE("There's no recorded data\n\nReturn after 3 seconds");
      delay(3000);
      home_message();
    }
  }
}

void home_message()
{
  if (IMU_payload == "")
  {
    SET_MESSAGE("1. Press M5 button to record IMU data\n\n2. Press bottom button to send data");
  }
  else
  {
    SET_MESSAGE("1. (Restart) Press M5 button to record IMU data\n\n2. (You have IMU data now!!) Press bottom button to send data");
  }   
}

void check_internet()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    WiFi.begin(SSID, PASSWORD);
    SET_MESSAGE("No Internet.\n\nConnecting to %s......", SSID);
    
    while (WiFi.status() != WL_CONNECTED) 
    {
      delay(1000);
    }

    SET_MESSAGE("Success connecting to %s\n\nStarting after 3 seconds", SSID);
    timeClient.begin();
    delay(3000);
    home_message();
  }
}

void record_IMU_data()
{
  float gyroX = 0, gyroY = 0, gyroZ = 0;
  float accelX = 0, accelY = 0, accelZ = 0;
  float pitch = 0, roll = 0, yaw = 0;
  uint32_t timestamp = 0;

  M5.IMU.getGyroData(&gyroX, &gyroY, &gyroZ);
  M5.IMU.getAccelData(&accelX, &accelY, &accelZ);
  M5.IMU.getAhrsData(&pitch, &roll, &yaw);    
  timestamp = timeClient.getEpochTime();
  IMU_payload += String(gyroX) + "," + String(gyroY) + "," + String(gyroZ) + ","
                + String(accelX) + "," + String(accelY) + "," + String(accelZ) + ","
                + String(pitch) + "," + String(roll) + "," + String(yaw) + ","
                + String(timestamp) + "|";
  timeClient.update();
  
  delay(100);
}

void send_IMU_data()
{
  SET_MESSAGE("Sending IMU data to server......");

  HTTPClient http;
  http.begin(String(DOMAIN_URL) + String(UUID));
  http.addHeader("Content-Type", "text/plain");
  uint16_t httpResponseCode = http.POST(IMU_payload);

  if (httpResponseCode == 200)
  {
    SET_MESSAGE("Success send IMU data to server\n\n Return after 3 seconds");
    delay(3000);
    IMU_payload = "";
  }
  else
  {
    SET_MESSAGE("There is an unknown error issue occur, please try again\n\n Return after 3 seconds");
    delay(3000);
  }

  http.end();
}