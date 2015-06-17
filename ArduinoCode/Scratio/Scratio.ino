#include <Servo.h>

#define AMAX 7   //A0-A6
#define DIN_MAX 3  //2,3,4
#define DOUT_MAX 3  //10,11,13
#define AOUT_MAX 2  //5,6
#define SERVO0 7
#define SERVO1 8
#define SERVO2 12
#define WAIT_TIME  10  //10ms
#define NCOM  5  //D,T,A,SA,SD
#define COM_SA  0
#define COM_SD  1
#define COM_D  2
#define COM_T  3
#define COM_A  4

int din[DIN_MAX] = {2,3,4};
int dout[DOUT_MAX] = {10,11,13};
int aout[AOUT_MAX] = {5,6};
int ain[AMAX] = {A0,A1,A2,A3,A4,A5,A6}; //A0-A6
int nloop;
int pin;
int value;

Servo servo0;
Servo servo1;
Servo servo2;;

void setup() {
  //Do not change the serial connection bitrate.
  Serial.begin(115200);
  for(int i=0;i<DIN_MAX;i++){
    pinMode(din[i],INPUT_PULLUP);
  }
  for(int i=0;i<DOUT_MAX;i++){
    pinMode(dout[i],OUTPUT);
  }
  nloop = 0;
}

void loop() {
  //receive data from your app, do not remove this line.
  serialReceive();
  if(nloop == WAIT_TIME){
    serialSend();
    nloop = 0;
  }else{
    nloop++;
  }
  delay(1);
}

void serialSend(){
  Serial.print("D");
  for(int i=0;i<DIN_MAX;i++){
    Serial.print(digitalRead(din[i]));
  }
  Serial.print("A");
  for(int i=0;i<AMAX;i++){
    ain[i] = analogRead(i);
    Serial.print(ain[i]);
    if(i<AMAX-1)  Serial.print(",");
  }
  Serial.println();
}

void serialReceive(){
  if(Serial.available() > 0){
    String str = Serial.readStringUntil('\n');
    int index = checkCommand(str);

    switch(index){
      case COM_D:
        if(value == 0)  digitalWrite(pin,false);
        else            digitalWrite(pin,true);
        break;
      case COM_T:
        tone(pin,value,3000);
        break;
      case COM_A:
        analogWrite(pin,value);
        break;
      case COM_SA:
        setServoAngle(pin,value);
        break;
      case COM_SD:
        detachServo(pin);
        break;
      default:
        break;
    }
  }
};

void setServoAngle(int pin,int val){
  switch(pin){
    case SERVO0:
      servo0.attach(pin);
      servo0.write(val);
      break;
    case SERVO1:
      servo1.attach(pin);
      servo1.write(val);
      break;
    case SERVO2:
      servo2.attach(pin);
      servo2.write(val);
      break;
  }   
}

void detachServo(int pin){
  switch(pin){
    case SERVO0:
      servo0.detach();
      break;
    case SERVO1:
      servo1.detach();
      break;
    case SERVO2:
      servo2.detach();
      break;
  }   
}

int checkCommand(String str){
  String strc = "";
  for(int i=0;i<NCOM;i++){
    switch(i){
      case COM_D:
        strc = "D";
        break;
      case COM_T:
        strc = "T";
        break;
      case COM_A:
        strc = "A";
        break;
      case COM_SA:
        strc = "SA";
        break;
      case COM_SD:
        strc = "SD";
        break;
    }
    if(str.indexOf(strc) > 0){
      int slen = str.length();
      pin = str.substring(0,str.indexOf(strc)).toInt();
      value = str.substring((str.indexOf(strc)+strc.length()),slen).toInt();
      return i;
    }
  }
  return 0;
}
