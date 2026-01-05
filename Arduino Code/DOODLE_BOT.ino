#define ml1 9
#define ml2 6
#define mr1 10
#define mr2 11
char command;
char path[]={'S', 'R', 'L', 'L', 'R', 'R', 'L', 'L', 'F'};
int i=0;

void start(){
  digitalWrite(3,HIGH);
  digitalWrite(4,HIGH);
  delay(200);
  digitalWrite(4,LOW);
}

void goStraight(){
  analogWrite(ml1,55);
  analogWrite(ml2,0);
  analogWrite(mr1,47);
  analogWrite(mr2,0);
  delay(1500);
  
}
void hover(){
  analogWrite(ml1,0);
  analogWrite(ml2,125);
  analogWrite(mr1,125);
  analogWrite(mr2,0);
  delay(1000);
}
void turnRight(){
  analogWrite(ml1,70);
  analogWrite(ml2,0);
  analogWrite(mr1,0);
  analogWrite(mr2,62);
  digitalWrite(3,LOW);
  digitalWrite(7,HIGH);
  digitalWrite(4,HIGH);
  delay(570);
  digitalWrite(4,LOW);
  digitalWrite(3,HIGH);
  digitalWrite(7,LOW);
}
void turnLeft(){
  analogWrite(ml1,0);
  analogWrite(ml2,70);
  analogWrite(mr1,62);
  analogWrite(mr2,0);
  digitalWrite(3,LOW);
  digitalWrite(2,HIGH);
  digitalWrite(4,HIGH);
  delay(350 );
  digitalWrite(4,LOW);
  digitalWrite(3,HIGH);
  digitalWrite(2,LOW);
}
void brake(){
  analogWrite(ml1,0);
  analogWrite(ml2,0);
  analogWrite(mr1,0);
  analogWrite(mr2,0);
  digitalWrite(4,LOW);
  delay(50);
  digitalWrite(3,LOW);
  digitalWrite(2,HIGH);
  digitalWrite(4,HIGH);
  delay(50);
  digitalWrite(2,LOW);
  digitalWrite(7,HIGH);
  digitalWrite(4,LOW);
  delay(50);
  digitalWrite(7,LOW);
  digitalWrite(3,HIGH);
  digitalWrite(4,HIGH);
  delay(50);
}

void setup() {
  // put your setup code here, to run once:
  pinMode(ml1,OUTPUT);
  pinMode(ml2,OUTPUT);
  pinMode(mr1,OUTPUT);
  pinMode(mr2,OUTPUT);
  pinMode(2,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  /*action=path[i];
  if(action=='S'){
    goStraight();
    delay(2500);
    i=i+1;
  }
  else if(action=='R'){
    turnRight();
    delay(700);
    goStraight();
    delay(2000);
    i=i+1;
  }
  else if(action=='L'){
    turnLeft();
    delay(700);
    goStraight();
    delay(2000);
    i=i+1;
  }
  else if(action=='F'){
    brake();
    i=i;
  }
  goStraight();*/
  // put your main code here, to run repeatedly:
  if(command!='F'){
    for (i; i < strlen(path);) {
      char command = path[i];
      Serial.print("Executing: ");
      Serial.println(command);

      if (command == 'S') {
        // Start command - move forward
        start();
        goStraight();
        i++;
      }
      else if (command == 'L') {
        // Left turn, then continue moving forward
        turnLeft();
        goStraight();
        i++;
      }
      else if (command == 'R') {
        // Right turn, then continue moving forward
        turnRight();
        goStraight();
        i++;
      }
      else if (command == 'F') {
        // End command - stop the bot and exit loop
        //hover();
        brake();
        //break;
      }
    }
  }
  else{
    brake();
  }
  //brake();
}
