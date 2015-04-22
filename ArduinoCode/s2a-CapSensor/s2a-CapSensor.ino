#include <Wire.h>
#include "Adafruit_MPR121.h"

// You can have up to 4 on one i2c bus but one is enough for testing!
Adafruit_MPR121 cap = Adafruit_MPR121();

// Keeps track of the last pins touched
// so we know when buttons are 'released'
uint16_t lasttouched = 0;
uint16_t currtouched = 0;

#define NCAP  12

int state[NCAP];

void setup() {
  while (!Serial);        // needed to keep leonardo/micro from starting too fast!
  //Do not change the serial connection bitrate.
  Serial.begin(115200);
  
  for(int i=0;i<NCAP;i++){
    state[i] = 0;
  }

  if (!cap.begin(0x5A)) {
    Serial.println("MPR121 not found, check wiring?");
    while (1);
  }
}

void loop() {
  // Get the currently touched pads
  currtouched = cap.touched();

  //receive data from your app, do not remove this line.
  serialSend();
  
  // reset our state
  lasttouched = currtouched;
  delay(10);
}

void serialSend(){
  Serial.print("C");
  for (uint8_t i=0; i<NCAP; i++) {
    // it if *is* touched and *wasnt* touched before, alert!
    if ((currtouched & _BV(i)) && !(lasttouched & _BV(i)) ) {
      state[i] = 1;
//      Serial.print(1);
    }
    // if it *was* touched and now *isnt*, alert!
    if (!(currtouched & _BV(i)) && (lasttouched & _BV(i)) ) {
      state[i] = 0;
//      Serial.print(2);
    }
    Serial.print(state[i]);
  }
  Serial.println();
}
