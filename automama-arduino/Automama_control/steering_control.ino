int steeringPosRead() {
  int direction = analogRead(pot);
//  direction = direction / 100;/
  direction = getMovingAverage(direction/100);
  
  direction = map(direction, 4, 16, 6, -6); // right is +ive left is -ve)
//  Serial.println(direction);/
  return direction; // Fixed to return actual direction
}

void steeringControl(byte target) {
  // if (direction < -7) direction = -7;
  // if (direction > 7) direction = 7;
  int direction = target -6 ;
  int currentPos = steeringPosRead();
  // if (steeringEnabled) {
    if (currentPos > direction) {
//      stopThrottle();
      // Serial.println("Turning Left");
      analogWrite(lpwm, 255);
      analogWrite(rpwm, 0);
    } else if (currentPos < direction) {
//      stopThrottle();
      // Serial.println("Turning Right");
      analogWrite(lpwm, 0);
      analogWrite(rpwm, 255);
    } else {
      analogWrite(lpwm, 0);
      analogWrite(rpwm, 0);
      // Serial.println("On Position");
      // steeringEnabled = false;
    }
  // } else {
  //   analogWrite(lpwm, 0);
  //   analogWrite(rpwm, 0);
  // }
}

void goToCenter() {
  while(steeringPosRead() != 0){
    // Serial.print("Pot: ");
    // Serial.print(steeringPosRead());
    // Serial.println("   ");
    // steeringControl(steeringPosition); //
    if (steeringPosRead() < centerPos) {
      analogWrite(lpwm, 0);
      analogWrite(rpwm, 255);
      Serial.println("Turning Right to Center");
    } else if (steeringPosRead() > centerPos) {
      analogWrite(lpwm, 255);
      analogWrite(rpwm, 0);
      Serial.println("Turning Left to Center");
    } else {
      analogWrite(lpwm, 0);
      analogWrite(rpwm, 0);
      Serial.println("Already at Center Position");
    }
    delay(10);
  }
  analogWrite(lpwm, 0);
  analogWrite(rpwm, 0);
  Serial.println("Already at Center Position");
}
