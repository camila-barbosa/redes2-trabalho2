# Exercício 6 - Captura de Tráfego TCP com Wireshark

**Participantes:** Augusto do Santos, Camila Santos, Deivid Camargos, Marcos Miller

---

## 1. Objetivo

Capturar e analisar o tráfego TCP gerado no estabelecimento e encerramento de conexão via telnet na porta 80, identificando o processo de three-way handshake e o encerramento da conexão.

---

## 2. Metodologia

1. O Wireshark foi iniciado com captura na interface **any**
2. O comando **`telnet google.com 80`** foi executado no terminal
3. A requisição **`GET / HTTP/1.0`** foi enviada manualmente
4. A captura foi filtrada com os filtros `tcp.flags.syn==1` e `tcp.flags.fin==1`
5. Os pacotes TCP foram analisados individualmente

---

## 3. Resultados

### 3.1 Informações Gerais da Captura

| Campo | Valor |
|-------|-------|
| Interface capturada | any |
| IP do cliente (origem) | 10.180.11.42 |
| IP do servidor Google (destino) | 172.217.162.14 |
| Porta de origem (cliente) | 43570 |
| Porta de destino (servidor) | 80 |
| Protocolo de transporte | TCP |

---

### 3.2 Processo de Estabelecimento de Conexão (Three-Way Handshake)

O processo de estabelecimento TCP observado seguiu o fluxo padrão:

1. **SYN (pacote 1):** O cliente (`10.180.11.42:43570`) enviou um segmento SYN ao servidor (`172.217.162.14:80`) para iniciar a conexão
2. **SYN-ACK (pacote 2):** O servidor respondeu com SYN-ACK, confirmando o recebimento e enviando seu próprio número de sequência
3. **ACK (pacote 3):** O cliente confirmou com ACK, completando o three-way handshake e estabelecendo a conexão

**Fluxo observado:**
- Pacote 1: `10.180.11.42 → 172.217.162.14` — `[SYN]`
- Pacote 2: `172.217.162.14 → 10.180.11.42` — `[SYN, ACK]`
- Pacote 3: `10.180.11.42 → 172.217.162.14` — `[ACK]`

---

### 3.3 Processo de Encerramento de Conexão

O encerramento da conexão TCP observado seguiu o fluxo com troca de segmentos FIN-ACK:

1. **FIN-ACK (pacote 77):** Um dos lados iniciou o encerramento enviando um segmento FIN-ACK
2. **FIN-ACK (pacote 78):** O outro lado confirmou e também encerrou sua direção da conexão com FIN-ACK

**Fluxo observado:**
- Pacote 77: `[FIN, ACK]`
- Pacote 78: `[FIN, ACK]`

---

### 3.4 Análise dos Cabeçalhos TCP

**Pacote SYN (estabelecimento):**
- Source: `10.180.11.42:43570` → Destination: `172.217.162.14:80`
- Flags: `SYN`
- Protocolo: TCP, Porta 80

**Pacote SYN-ACK (resposta do servidor):**
- Source: `172.217.162.14:80` → Destination: `10.180.11.42:43570`
- Flags: `SYN, ACK`
- Protocolo: TCP, Porta 80

**Pacotes FIN-ACK (encerramento):**
- Flags: `FIN, ACK`
- Protocolo: TCP, Porta 80

---

### 3.5 Capturas de Tela

| Print | Descrição |
|-------|-----------|
| `telnet_conexao.png` | Terminal com a conexão telnet sendo estabelecida |
| `telnet_resposta.png` | Terminal com a resposta HTTP do servidor |
| `wireshark_syn.png` | Wireshark com filtro `tcp.flags.syn==1` mostrando o handshake |
| `wireshark_fin.png` | Wireshark com filtro `tcp.flags.fin==1` mostrando o encerramento |

---

## 4. Conclusão

A captura demonstrou com sucesso o processo completo de estabelecimento e encerramento de uma conexão TCP. Ao conectar via telnet ao servidor do Google na porta 80, o three-way handshake (SYN → SYN-ACK → ACK) foi claramente observado nos pacotes 1, 2 e 3. Após o envio da requisição `GET / HTTP/1.0` e o recebimento da resposta, o encerramento da conexão ocorreu por meio da troca de segmentos FIN-ACK nos pacotes 77 e 78, confirmando o comportamento padrão do protocolo TCP.
