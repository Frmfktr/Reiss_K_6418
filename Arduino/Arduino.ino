#include <SoftwareSerial.h>

SoftwareSerial plotter(2, 3);

void setup() {
  Serial.begin(115200);
  plotter.begin(9600);
}

void loop() {
  if(Serial.available() > 0) {
    plotter.write(Serial.read());
  }
  if(plotter.available() > 0) {
    Serial.write(plotter.read());
  }
}
