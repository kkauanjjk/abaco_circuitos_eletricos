#include <LiquidCrystal.h>

// LiquidCrystal lcd(12, 11, 5, 4, 3, 2); // Configuração dos pinos do LCD

const int numPins = 3; // Número de pinos analógicos
int analogPins[numPins] = {A0, A1, A2}; // Define os pinos analógicos a serem lidos
char pinLabels[numPins][3] = {"C:", "D:", "U:"}; // Etiquetas para os pinos analógicos

int raw[numPins];
int Vin = 5;
float Vout[numPins];
float R1 = 220;
float R2[numPins];
float buffer[numPins];

int valorLido = 0; // Variável para armazenar o valor lido de C, D e U

const int botaoPlayPin = D2; // Pino do botão Play
int estadoBotaoPlayAnterior = HIGH; // Estado anterior do botão Play

void setup() {
  // lcd.begin(16, 2); // Inicializa o display LCD com 16 colunas e 2 linhas
  Serial.begin(9600);
  pinMode(botaoPlayPin, INPUT); 

  delay(1000);
}

void loop() {
  estadoBotaoPlayAnterior = digitalRead(botaoPlayPin);
  delay(100);
  
int lerValor() {
  int valor = 0;
  for (int i = 0; i < numPins; i++){
    raw[i] = analogRead(analogPins[i]);

    if (raw[i]) {
      buffer[i] = raw[i] * Vin;
      Vout[i] = (buffer[i]) / 1024.0;
      buffer[i] = (Vin / Vout[i]) - 1;
      R2[i] = R1 * buffer[i];
      valor = valor * 10 + (int)(round(R2[i] / 220));
      Serial.println("       "); // Limpa o espaço anterior      
      Serial.println((int)(round(R2[i] / 1000)));
    }
  }
  return valor;
}
