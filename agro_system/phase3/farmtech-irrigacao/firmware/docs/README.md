````markdown
# Sistema de Controle de Irrigação com ESP32

Projeto para automação de irrigação baseada em condições ambientais, com segurança por ativação manual dupla.

---

## 🔍 Lógica de Funcionamento da Bomba

**A bomba liga somente se TODAS estas condições forem atendidas simultaneamente:**

1. **Umidade abaixo de 30%**  
   _(Medida pelo sensor DHT22)_

2. **pH entre 5 e 7**  
   _(Simulado pela leitura do LDR)_

3. **Botões P (Fósforo) e K (Potássio) pressionados**  
   _(Ativação manual consciente)_

---

## ❓ Por Que Esses Parâmetros?

### 1. Umidade ≤ 30%

- **Motivo Técnico**: Valor seguro para evitar encharcamento em culturas semiáridas (ex: cactos, lavanda)
- **Base Científica**: Nível comum em sistemas de irrigação conservativa ([FAO, 2022](https://www.fao.org))
- **Flexibilidade**: Pode ser ajustado para:
  ```cpp
  // Modifique no código:
  if (umidade < 30) → if (umidade < SEU_VALOR)
  ```
````

### 2. pH 5-7

- **Importância Agronômica**: Faixa ideal para maioria das plantas:
  - **5-6.5**: Hortaliças (tomate, batata)
  - **6-7**: Grãos (feijão, trigo)
- **Segurança Química**: Evita danos por acidez/alcalinidade extrema
- **Observação**: O LDR simula um sensor de pH real - para uso prático:
  ```cpp
  // Calibre com valores reais:
  float pH = map(valorLDR, MIN_LDR, MAX_LDR, 0, 14);
  ```

---

## ⚙️ Calibração Recomendada

| Parâmetro | Valores Padrão | Ajuste Recomendado           |
| --------- | -------------- | ---------------------------- |
| Umidade   | 30%            | 20-40% conforme tipo de solo |
| pH        | 5-7            | 4.5-7.5 para plantas ácidas  |
| Pressão   | Botão físico   | Add delay(200) para debounce |

---

## ✅ Como Usar

1. Pressione **ambos botões** simultaneamente
2. Sistema verifica automaticamente:
   - Umidade do ar
   - Nível de pH simulado
3. Bomba mantém-se ligada **enquanto**:
   - Condições ambientais forem atendidas
   - Botões estiverem pressionados

---

## 🛠 Melhorias Futuras

- [ ] Adicionar display LCD para valores em tempo real
- [ ] Implementar ativação por temporizador
- [ ] Integrar com sensor de pH profissional
- [ ] Adicionar modo IoT (WiFi/Blynk)


