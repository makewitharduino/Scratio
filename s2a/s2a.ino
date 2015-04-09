#define AMAX 6   //A0-A5
#define DIN_MAX 6  //2,4,7,8,12,13
#define DOUT_MAX 6  //3,5,6,9,10,11
#define BASIC 0
#define CUSTOM 1

int dpin_in[DIN_MAX] = {2,4,7,8,12,13};
int dpin_out[DOUT_MAX] = {3,5,6,9,10,11};
int apin[AMAX] = {14,15,16,17,18,19}; //A0-A5
int nloop;
String D = "D"; //digital
String T = "T"; //tone
String P = "P"; //pwm
String A = "A"; //analog
String C = "C"; //custom
int mode = BASIC;

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
  if(nloop == 100){
    serialSend();
    nloop = 0;
  }else{
    nloop++;
  }
  delay(10);
}


void serialSend(){
  Serial.print(D);
  for(int i=0;i<DIN_MAX;i++){
    Serial.print(digitalRead(dpin_in[i]));
    delay(1);
  }
  Serial.print(A);
  for(int i=0;i<AMAX;i++){
    apin[i] = analogRead(i);
    Serial.print(apin[i]);
    if(i<AMAX-1)  Serial.print(",");
  }
  Serial.println();
}

void serialReceive(){
  String str;
  String valRaw;
  int slen;
  int pin;
  int val;

  if(Serial.available() > 0){
    str = Serial.readStringUntil('\n');
    slen = str.length();
    if(str.indexOf(D) > 0){
      pin = str.substring(0,str.indexOf(D)).toInt();
      valRaw = str.substring(str.indexOf(D)+1,slen);
      val = valRaw.toInt();
      if(val == 0)  digitalWrite(pin,false);
      else          digitalWrite(pin,true);
    }else if(str.indexOf(A) > 0){
      pin = str.substring(0,str.indexOf(A)).toInt();
      valRaw = str.substring(str.indexOf(A)+1,slen);
      val = valRaw.toInt();
      analogWrite(pin,val);
    }else if(str.indexOf(C) > 0){
      int val = str.substring(0,str.indexOf(C)).toInt();
      doMethod(val);
    }else{
      Serial.println(str);
    }
  }
};

void doMethod(int val){
  switch(val){
    case 1:
      Serial.println("domethod");
      break;
    default:
      break;
  }
}
