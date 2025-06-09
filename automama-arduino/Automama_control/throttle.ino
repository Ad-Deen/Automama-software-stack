void throttleControl(byte speed) {
  // speed = map(speed, 0, 10, 0, 255);
  // if (speed < 0) speed = 0;
  // if (speed > 255) speed = 255;
//  isBrake = 0;
//  breakRead() < 9? isBrake = 0: isBrake = 1;
//  if (!isBrake) {
    analogWrite(throttle, speed);
//  }
}

void stopThrottle() {
  analogWrite(throttle, 0);
}
