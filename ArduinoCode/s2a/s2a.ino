#define AMAX 6   //A0-A5
#define DIN_MAX 6  //2,4,7,8,12,13
#define DOUT_MAX 6  //3,5,6,9,10,11

int dpin_in[DIN_MAX] = {2,4,7,8,12,13};
int dpin_out[DOUT_MAX] = {3,5,6,9,10,11};
int apin[AMAX] = {14,15,16,17,18,19}; //A0-A5
char command[5] = {'D','T','P','A','C'};
int nloop;

void setup() {
  //Do not change the serial connection bitrate.
  Serial.begin(115200);
  for(int i=0;i<DIN_MAX;i++){
    pinMode(dpin_in[i],INPUT_PULLUP);
  }
  for(int i=0;i<DOUT_MAX;i++){
    pinMode(dpin_out[i],OUTPUT);
  }
  nloop = 0;
}

void loop() {
  //receive data from your app, do not remove this line.
  serialReceive();
  if(nloop == 100){ //1s
    serialSend();
    nloop = 0;
  }else{
    nloop++;
  }
  delay(10);
}

void serialSend(){
  Serial.print("D");
  for(int i=0;i<DIN_MAX;i++){
    Serial.print(digitalRead(dpin_in[i]));
    delay(1);
  }
  Serial.print("A");
  for(int i=0;i<AMAX;i++){
    apin[i] = analogRead(i);
    Serial.print(apin[i]);
    if(i<AMAX-1)  Serial.print(",");
  }
  Serial.println();
}

void serialReceive(){
  if(Serial.available() > 0){
    String str = Serial.readStringUntil('\n');
    int slen = str.length();
    int index = checkCommand(str);

    int pin = str.substring(0,str.indexOf(String(command[index]))).toInt();
    int val = str.substring(str.indexOf(String(command[index]))+1,slen).toInt();

    switch(index){
      case 0: //D
        if(val == 0)  digitalWrite(pin,false);
        else          digitalWrite(pin,true);
        break;
      case 1: //T
        tone(pin,val,3000);
        break;
      case 3: //A
        analogWrite(pin,val);
        break;
      case 4: //C
      //doMethod(pin);
        break;
      default:
        break;
    }
  }
};

int checkCommand(String str){
  String strc = "";
  for(int i=0;i<5;i++){
    strc = String(command[i]);
    if(str.indexOf(strc) > 0) return i;
  }
}

void doMethod(int val){
  switch(val){
    case 1:
      Serial.println("domethod");
      break;
    default:
      break;
  }
}
