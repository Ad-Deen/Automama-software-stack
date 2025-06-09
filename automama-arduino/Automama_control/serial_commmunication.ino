void communication(){
  if (Serial.available() >= 3) {
    targetThrottle = Serial.read();
    targetSteering = Serial.read();
    targetBrake = Serial.read();
    // Echo the 3 values back
    byte stpos =steeringPosRead()+6;
    
    Serial.write(targetThrottle);
    Serial.write(stpos);
    Serial.write(breakRead());
  }
}

// void processCommand(const char* command) {
//   communication();
//   if (strncmp(command, "t ", 2) == 0) {
//     const char* valueStr = command + 2; // Skip "t "
//     if (isValidNumber(valueStr)) {
//       int speed = atoi(valueStr);
//         throttleControl(speed);
//         Serial.print("Throttle Speed Set: ");
//         Serial.println(speed);
//     } else {
//       Serial.println("Error: Invalid throttle value");
//     }
//   } else if (strncmp(command, "s ", 2) == 0) {
//     const char* valueStr = command + 2; // Skip "s "
//     if (isValidNumber(valueStr)) {
//       int position = atoi(valueStr);
//         steeringPosition = position;
//         steeringEnabled = true;
//         Serial.print("Steering Position Set: ");
//         Serial.println(position);

//     } else {
//       Serial.println("Error: Invalid steering value");
//     }
//   } else if (strcmp(command, "c") == 0) {
//     goToCenter();
//   } else if (strcmp(command, "p") == 0) { // Changed to "p" for stop
//     stopThrottle();
//   } else if (strcmp(command, "b") == 0) {
//     brakeNow = true;
//   } else if (strcmp(command, "r") == 0) {
//     brakeNow = false;
//   } else {
//     Serial.println("Unknown Command");
//     stopThrottle();
//   }
// }
