#define AMAX 6   //A0-A5
#define DMAX 12  //2-13

int dpin[DMAX] = {};
int apin[AMAX] = {};
int spin[DMAX] = {};
int nloop;
String D = "D";
String A = "A";
String M = "M";
String S = "S";

void setup() {
  //Do not change the serial connection bitrate.
  Serial.begin(115200);
  for(int i=0;i<DMAX;i++){
    pinMode(i+2,INPUT_PULLUP);
    spin[i] = 0;
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
  for(int i=0;i<DMAX;i++){
    if(spin[i] == 0)    dpin[i] = digitalRead(i+2);
    else dpin[i] = 2;
    delay(1);
    Serial.print(dpin[i]);
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
      pinMode(pin,OUTPUT);
      spin[pin-2] = 1;
      if(val == 0)  digitalWrite(pin,false);
      else          digitalWrite(pin,true);
    }else if(str.indexOf(A) > 0){
      pin = str.substring(0,str.indexOf(A)).toInt();
      valRaw = str.substring(str.indexOf(A)+1,slen);
      val = valRaw.toInt();
      analogWrite(pin,val);
    }else if(str.indexOf(S) > 0){
      pin = str.substring(0,str.indexOf(S)).toInt();
      valRaw = str.substring(str.indexOf(S)+1,slen);
      val = valRaw.toInt();
      spin[pin-2] = val;
      if(val == 0)  pinMode(pin,INPUT_PULLUP);
      else          pinMode(pin,OUTPUT);
    }else if(str.indexOf(M) > 0){
      int val = str.substring(0,str.indexOf(M)).toInt();
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
