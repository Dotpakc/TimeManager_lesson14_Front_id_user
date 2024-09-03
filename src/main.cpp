#include <Arduino.h>
#include <NanitLib.h>
#include <keypad.h>

const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns

char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
}; // це матриця клавіш або карта клавіш

byte rowPins[ROWS] = {P7_4, P7_3, P7_2, P7_1}; // піни рядків
byte colPins[COLS] = {P6_4, P6_3, P6_2, P6_1}; // піни стовпців

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );



// display.setTextSize(2);
// display.setTextWrap(false);
// display.setCursor(41, 5);
// display.print("Time");
// display.setTextSize(1);
// display.setCursor(25, 22);
// display.print("Manager System");
// display.fillRoundRect(28, 48, 74, 25, 4, 0x52AA);
// display.setTextSize(2);
// display.setCursor(36, 53);
// display.print("12345");
// display.setTextColor(0x540);
// display.setTextSize(1);
// display.setCursor(11, 142);
// display.print("Accept #");
// display.drawRect(3, 134, 122, 23, 0x52AA);
// display.setTextColor(0xFFFF);
// display.setCursor(76, 142);
// display.print("Reset *");





void setup() {
  Serial.begin(9600);
  Nanit_Base_Start();

  tft.setRotation(0);
  tft.fillScreen(ST7735_BLACK);
  tft.setTextColor(ST7735_WHITE, ST7735_BLACK);

  tft.setTextSize(2);
  tft.setCursor(41, 5);
  tft.print("Time");
  tft.setTextSize(1);
  tft.setCursor(25, 22);
  tft.print("Manager System");
  tft.fillRoundRect(28, 48, 74, 25, 4, 0x52AA);
  tft.setTextColor(0x540);
  tft.setTextSize(1);
  tft.setCursor(11, 142);
  tft.print("Accept *");
  tft.drawRect(3, 134, 122, 23, 0x52AA);
  tft.setTextColor(0xFFFF);
  tft.setCursor(76, 142);
  tft.print("Reset #");


  // tft.setTextSize(2);
  // tft.setCursor(36, 53);
  // tft.print("12345");

  tft.setTextColor(ST7735_WHITE,  0x52AA);
}

String input = "";


void clearInput() {
  input = "";
  tft.setCursor(36, 53);
  tft.print("     ");
}

void loop() {
  char key = keypad.getKey();
  if (key) {
    if (key == '#') {
      clearInput();
    } else if (key == '*') {
      if (input.length() > 0) Serial.println(input);
      clearInput(); 
    } else {
      input += key;
      if (input.length() > 5) clearInput(); 
    }

    tft.setTextSize(2);
    tft.setCursor(36, 53);
    tft.print(input);

  }
}