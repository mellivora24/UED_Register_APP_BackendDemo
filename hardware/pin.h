#include <LiquidCrystal_I2C.h>
#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

#define TX 2
#define RX 3
#define relay 4
#define buzzer 5
#define btn_1 6
#define btn_2 7

LiquidCrystal_I2C screen(0x27, 16, 02);
SoftwareSerial finger_print(2, 3);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&finger_print);