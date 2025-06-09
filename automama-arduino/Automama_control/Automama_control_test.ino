#define lpwm 33
#define rpwm 32

#define brakeH 14
#define brakeL 27
#define pot 4
#define throttle 5
#define lresPin 15
#define centerPos 0 // Center position for steering
#define MAX_COMMAND_LENGTH 32 // Maximum command length

#define HEADER_BYTE 0xAA

char commandBuffer[MAX_COMMAND_LENGTH]; // Buffer for incoming command
int bufferIndex = 0; // Current position in buffer
bool steeringEnabled = true; // Steering control flag
bool isBrake = 0;
bool brakeDone = false;
byte targetThrottle = 0;
byte targetSteering = 6;
byte targetBrake    = 7;

void setup() {
  Serial.begin(115200);
  pinMode(pot, INPUT);
  pinMode(lpwm, OUTPUT);
  pinMode(rpwm, OUTPUT);
  pinMode(brakeH, OUTPUT);
  pinMode(brakeL, OUTPUT);
  pinMode(throttle, OUTPUT);
  pinMode(lresPin, INPUT);

   goToCenter();
   
   while(breakRead() != 7){
     brakeOp(7);
     // Serial.println(breakRead())
     delay(10);
   }
   brakeStop();
   stopThrottle();
   delay(2000);
//   stopThrottle();
//   delay(2000);
//  brakeRelease();
//  delay(100);
//  brakeStop();
  // while(breakRead() != 7){
  //   brakeOp(7);
  //   // Serial.println(breakRead())
  //   delay(10);
  // }
  // brakeStop();
  // delay(1000);
  // while(breakRead() != 9){
  //   brakeOp(9);
  //   delay(10);
  // }
  // brakeStop();
  // delay(1000);
  // while(breakRead() != 18){
  //   brakeOp(18);
  //   delay(10);
  // }
  // brakeStop();
  // delay(2000);
  // while(breakRead() != 7){
  //   brakeOp(7);
  //   delay(10);
  // }
  // brakeStop();
  // delay(1000);
//        analogWrite(lpwm, 0);
//      analogWrite(rpwm, 255);
//      delay(500);
//            analogWrite(lpwm, 0);
//      analogWrite(rpwm, 0);
}

void loop() {
//  read_sensor_data();/
  communication();
//read_received_data();
//  steeringControl(-3);
//  communication();
  steeringControl(targetSteering);
  throttleControl(targetThrottle);
  brakeOp(targetBrake);

  delay(20);
  // readUARTPacketBlocking();
  // Serial.print(targetThrottle);
  // Serial.print(" - ");
  // Serial.print(targetSteering);
  // Serial.print(" - ");
  // Serial.println(targetBrake);
  // // breakRead();
  // // brakeOp(7)
  // // delay(50);
  // // steeringControl(-4);
  // // Serial.println(steeringPosRead());
  // // delay(1000);
  // // steeringControl(4);
  // // delay(1000);
  // read_received_data();
}
