void read_sensor_data(){
  Serial.print("SteeringPos: ");
  Serial.print(String(steeringPosRead()));
  Serial.print(" ");
  Serial.print("BrakePos: ");
  Serial.print(String(breakRead()));
  Serial.println(" ");
}

void read_received_data(){
    Serial.print("Throttle: ");
  Serial.print(targetThrottle);
  Serial.print(" ");
  Serial.print("Steering: ");
  Serial.print(targetSteering);
  Serial.print(" ");
  Serial.print("Brake: ");
  Serial.print(targetBrake);
  Serial.println(" ");
}