#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define LCD_ADDRESS 0x27 
#define LCD_COLUMNS 20
#define LCD_ROWS 4

LiquidCrystal_I2C lcd(LCD_ADDRESS, LCD_COLUMNS, LCD_ROWS);

String trim(String str) {
  while (str.length() > 0 && isWhitespace(str.charAt(0))) {
    str.remove(0, 1);
  }
  while (str.length() > 0 && isWhitespace(str.charAt(str.length() - 1))) {
    str.remove(str.length() - 1, 1);
  }
  return str;
}

void setup() {
  Serial.begin(9600);
  Wire.begin();

  lcd.init();
  lcd.backlight();
  lcd.clear();
  Serial.println("LCD Initialized");
}

void loop() {
  String incoming_data; 

  if (Serial.available() > 0) {
    incoming_data = trim(Serial.readString()); 
    Serial.print("Received from Serial: ");
    Serial.println(incoming_data);

    if (incoming_data.startsWith("t")) {
      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.print(incoming_data.substring(1, 21));

      lcd.setCursor(0, 1);
      lcd.print(incoming_data.substring(21, 41));

      lcd.setCursor(0, 2);
      lcd.print(incoming_data.substring(41, 61));

      lcd.setCursor(0, 3);
      lcd.print(incoming_data.substring(61, 81));

      Serial.println("ok");
    } else if (incoming_data.startsWith("r")) {
      lcd.clear();
      Serial.println("ok");
    } else {
      Serial.println("error"); 
    }
  }
}
