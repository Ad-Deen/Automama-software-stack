byte breakRead() {
  byte linearResistance = analogRead(lresPin)/100;
  // Serial.print("Linear Resistance: ");
  // Serial.println(linearResistance);
  // return linearResistance > 100;
  // Serial.println(applied ? "Brakes Applied" : "Brakes Not Applied");
  return linearResistance;
}

void brakeOp(byte targetBrake) {
    if (abs(breakRead()- targetBrake) > 1){
      brakeDone = false;
      }
  
    if (breakRead() > 9){
      stopThrottle();
      }
    if(breakRead() < targetBrake){
      if(!brakeDone){
        stopThrottle();
        brakeApply();
      }
    }
    else if(breakRead() > targetBrake){
      if(!brakeDone){
        stopThrottle();
        brakeRelease();
      }
    }
    else{
      analogWrite(brakeH, 0);
      analogWrite(brakeL, 0);
      brakeDone = true;
    }
  // }
  // else{
  //   analogWrite(brakeH, 0);
  //   analogWrite(brakeL, 0);
  // }
}


void brakeApply(){
  analogWrite(brakeH, 125);
  analogWrite(brakeL, 0);
}

void brakeRelease(){
   analogWrite(brakeH, 0);
  analogWrite(brakeL, 125);
}
void brakeStop(){
   analogWrite(brakeH, 0);
  analogWrite(brakeL, 0);
}
