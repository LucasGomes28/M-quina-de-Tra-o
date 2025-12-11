#include <AltSoftSerial.h>
// Define os pinos RX e TX para a comunicação serial via software
// O pino 8 do Arduino será o RX e o pino 9 será o TX
AltSoftSerial meuSerial;


// --- Mapeamento de Hardware ---
#define ADDO 7 //Data Out
#define ADSK 6 //SCK
 
float forca = 0;
long tara = 0;
long qnt_passos = 0;
int incomingByte = 0; // variável para o dado recebido
int receivedByte = 0; // variável para o dado recebido
 
// --- Protótipo das Funções Auxiliares ---
unsigned long ReadCount(); //conversão AD do HX711
 
 
// --- Variáveis Globais ---
long convert;
 
 
// --- Configurações Iniciais ---
void setup()
{
 pinMode(ADDO, INPUT_PULLUP); //entrada para receber os dados
 pinMode(ADSK, OUTPUT); //saída para SCK
 
 Serial.begin(115200);
 meuSerial.begin(9600);
 
 for(int x=0; x<10; x++){
 tara = ReadCount();
 delay(10);
 }
 
} //end setup
 
 
// --- Loop Infinito ---
void loop()
{

 if (digitalRead(ADDO) == LOW) {
    convert = ReadCount();
    // (x - in_min) * (out_max-out_min) / (in_max - in_min) + out_min;
    forca = ((convert - tara) * 10.792) / 51746.0;
    //forca = ((convert - tara) * 10.792) / (51746.0 - tara);
 }
static unsigned long last = 0;
if (millis() - last >= 100) {
   last = millis();
   Serial.print(forca,2);
   Serial.print(';');
   Serial.println(qnt_passos);

}

 //Leitura de dados do código em Python
 if (Serial.available() > 0) {
   // lê do buffer o dado recebido:
   receivedByte = Serial.read();
   if (receivedByte != 10 && receivedByte != 13) {
     incomingByte = receivedByte;

     switch(incomingByte){
       case 'd'://desce a maquina
          meuSerial.println('d');
       break;
      
       case 's'://sobe a maquina
          meuSerial.println('s');
       break;
      
       case 'p'://parada
          meuSerial.println('p');
          qnt_passos = 0;
       break;
       default:
          qnt_passos = incomingByte;
       break;
       }
   }
 }

 //Leitura de dados do arduino UNO
 if (meuSerial.available() > 0) {

   // lê do buffer o dado recebido:
   receivedByte = meuSerial.read();
   if (receivedByte != 10 && receivedByte != 13) {
     incomingByte = receivedByte;

     switch(incomingByte){
       case 'a'://incrementa 1 passo
          qnt_passos = qnt_passos + 1;
       break;
      
       case 'b'://decrementa 1 passo
          qnt_passos = qnt_passos - 1;
       break;

       default:
       break;
       }
     }
   }
} //end loop
 

// --- Funções ---
unsigned long ReadCount()
{
 unsigned long Count = 0;
 unsigned char i;
 
 digitalWrite(ADSK, LOW);
 
 while(digitalRead(ADDO));
 
 for(i=0;i<24;i++)
 {
 digitalWrite(ADSK, HIGH);
 Count = Count << 1;
 digitalWrite(ADSK, LOW);
 if(digitalRead(ADDO)) Count++;
 
 } //end for
 
 digitalWrite(ADSK, HIGH);
 Count = Count^0x800000;
 digitalWrite(ADSK, LOW);
 
 return(Count);
 
 
} //end ReadCount
 
