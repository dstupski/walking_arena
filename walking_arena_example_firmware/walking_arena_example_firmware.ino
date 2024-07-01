char command;
int state_1=0;
int state_2 =0;
unsigned long milli=millis();
unsigned long duration_ =10000;
int led_pin1  =3;
int led_pin2 =5;

void flicker(unsigned long on_time, unsigned long off_time, unsigned long duration){
  unsigned long startTime = millis();
  unsigned long currentTime = startTime;
  unsigned long previousTime=startTime;
  bool ledState = HIGH;
  analogWrite(led_pin1, 255);
  analogWrite(led_pin2, 255);
  

  while ((currentTime - startTime) < duration){
    currentTime = millis();
    
    if (ledState == HIGH && (currentTime-previousTime) >= on_time) {
      ledState= LOW;
      analogWrite(led_pin1, 0);
      analogWrite(led_pin2, 0);
      previousTime = millis();
    } 
    else if (ledState == LOW && (millis() - previousTime) >= off_time){
      ledState = HIGH;
      analogWrite(led_pin1, 255);
      analogWrite(led_pin2, 255);
      previousTime = millis();
    }
  }
analogWrite(led_pin1, 0);
analogWrite(led_pin2, 0);
}



void setup() {
  Serial.begin(9600);
  pinMode(led_pin1, OUTPUT);
  pinMode(led_pin2, OUTPUT);
}


void loop() {
    if (Serial.available()){
    command = Serial.read();
  }
 if(command =='a'){
    analogWrite(led_pin1, 0);
    analogWrite(led_pin2, 0);
    state_1=1;
    duration_ = 10000;
    milli =millis();
    command=' ';
  }
  if(command =='b'){
    analogWrite(led_pin1, 255);
    analogWrite(led_pin2, 255);
    state_1=1;
    duration_ = 10000;
    milli =millis();
    command=' ';
  }
   if(command =='c'){ 
    flicker(200, 400., 10000);
    command=' ';
  
  }
    if(command =='d'){ 
    flicker(200, 200., 10000);
    command=' ';
  
  }
      if(command =='e'){ 
    flicker(200, 100., 10000);
    command=' ';
  
  }
 if (state_1==1 and millis()-milli>duration_){
  analogWrite(led_pin1, 0);
  analogWrite(led_pin2, 0);
  state_1=0;
 }
  // put your main code here, to run repeatedly:

}
