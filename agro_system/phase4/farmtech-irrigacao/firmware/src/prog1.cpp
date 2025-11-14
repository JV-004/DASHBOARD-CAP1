#include <DHT.h>

// Definições do DHT22
#define DHTPIN 16     // DHT22 no GPIO16
#define DHTTYPE DHT22 // Tipo do sensor
DHT dht(DHTPIN, DHTTYPE);

// Definição dos pinos
const int botaoP = 4;  // Botão Fósforo
const int botaoK = 5;  // Botão Potássio
const int ldrPin = 34; // LDR (pH) no GPIO34
const int rele = 17;   // Relé no GPIO17

// Variáveis para detecção de estado dos botões
bool lastEstadoP = HIGH;
bool lastEstadoK = HIGH;

// Protótipo da função
void testarBotoes();

void setup() {
    Serial.begin(115200);
    
    // Configuração dos pinos
    pinMode(botaoP, INPUT);
    pinMode(botaoK, INPUT);
    pinMode(rele, OUTPUT);
    
    // Inicializa o DHT22
    dht.begin();
    delay(2000); // Tempo para estabilização do sensor

    Serial.println("\nSistema Iniciado!");
    Serial.println("Testando componentes...");
    testarBotoes();
}

void loop() {
    // Leitura da umidade com tratamento de erro
    float umidade = dht.readHumidity();
    if (isnan(umidade)) {
        Serial.println("Erro na leitura do DHT22!");
        delay(2000);
        return;
    }

    // Leitura e mapeamento do LDR para pH
    int valorLDR = analogRead(ldrPin);
    float pH = map(valorLDR, 0, 4095, 0, 14);

    // Leitura dos estados dos botões
    bool estadoAtualP = digitalRead(botaoP);
    bool estadoAtualK = digitalRead(botaoK);

    // Detecção de mudança no botão P
    if (estadoAtualP != lastEstadoP) {
        Serial.print("Botão P: ");
        Serial.println(estadoAtualP ? "PRESSIONADO" : "SOLTO");
        lastEstadoP = estadoAtualP;
    }

    // Detecção de mudança no botão K
    if (estadoAtualK != lastEstadoK) {
        Serial.print("Botão K: ");
        Serial.println(estadoAtualK ? "PRESSIONADO" : "SOLTO");
        lastEstadoK = estadoAtualK;
    }

    // Lógica de acionamento da bomba
    if (umidade < 30 && pH >= 5 && pH <= 7 && estadoAtualP && estadoAtualK) {
        digitalWrite(rele, HIGH);
    } else {
        digitalWrite(rele, LOW);
    }

    // Exibição dos dados no monitor serial
    Serial.print("Umidade: ");
    Serial.print(umidade);
    Serial.print("% | pH: ");
    Serial.print(pH);
    Serial.print(" (LDR: ");
    Serial.print(valorLDR);
    Serial.print(") | Fósforo: ");
    Serial.print(estadoAtualP ? "Sim" : "Não");
    Serial.print(" | Potássio: ");
    Serial.print(estadoAtualK ? "Sim" : "Não");
    Serial.print(" | Bomba: ");
    Serial.println(digitalRead(rele) ? "LIGADA" : "DESLIGADA");

    delay(4000); // Intervalo entre ciclos
}

// Implementação da função de teste dos botões
void testarBotoes() {
    Serial.println("Teste Inicial dos Botões:");
    Serial.print("Botão P: ");
    Serial.println(digitalRead(botaoP) ? "Ativo" : "Inativo");
    Serial.print("Botão K: ");
    Serial.println(digitalRead(botaoK) ? "Ativo" : "Inativo");

    if (digitalRead(botaoP) == digitalRead(botaoK)) {
        Serial.println("AVISO: Verifique as conexões dos botões!");
    }
}