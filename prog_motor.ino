// --- Mapeamento de Hardware ---
 #define directionPin 2 //pino que define o sentido de rotação
 #define stepPin 3 //pino que manda os passos para o driver
 #define enable 4 //pino ENA+ que habilita o driver
 
int incomingByte = 0; // variável para o dado recebido
int receivedByte = 0; // variável para o dado recebido
unsigned int velocidade = 1000;//variável para armazenar a velocidade
 
// --- Configurações Iniciais ---
void setup()
{

 pinMode(11,INPUT_PULLUP);//sinal do sensor de fim de curso - limite inferior
 pinMode(12,INPUT_PULLUP);//sinal do sensor de fim de curso - limite superior
 pinMode(directionPin, OUTPUT);//pino que define o sentido de rotação
 pinMode(stepPin, OUTPUT);//pino que manda os passos para o driver
 
 Serial.begin(9600);
 
 
} //end setup
 
 
// --- Loop Infinito ---
void loop()
{
 if (Serial.available() > 0) {
 // lê do buffer o dado recebido:
 receivedByte = Serial.read();
 if (receivedByte != 10 && receivedByte != 13) {
  incomingByte = receivedByte;
 }
 }
 switch(incomingByte){
 case 'd'://desce a maquina
 if(digitalRead(11)==HIGH){
   digitalWrite(directionPin, LOW);//sentido anti-horário
   digitalWrite(stepPin, HIGH);
   delayMicroseconds(velocidade);
   digitalWrite(stepPin, LOW);
   delayMicroseconds(velocidade);
   Serial.println('b');//Código enviado para decrementar 1 passo
 }
 break;

 case 's'://sobe a maquina
 if(digitalRead(12)==HIGH){
   digitalWrite(directionPin, HIGH);//sentido horário
   digitalWrite(stepPin, HIGH);
   delayMicroseconds(velocidade);
   digitalWrite(stepPin, LOW);
   delayMicroseconds(velocidade);
   Serial.println('a');//Código enviado para incrementar 1 passo
 }
 break;

 case 'p'://parada
 digitalWrite(directionPin, LOW);
 digitalWrite(stepPin, LOW);
 
 break;
 default:
 digitalWrite(directionPin, LOW);
 digitalWrite(stepPin, LOW);
 break;
 }
 
 
 
} //end loop
 
