# Exercício 8 - Captura de Tráfego ICMP com Wireshark

**Participantes:** Augusto do Santos, Camila Santos, Deivid Camargos, Marcos Miller 

---

## 1. Objetivo

Capturar e analisar o tráfego ICMP gerado pelo comando `ping`, identificando os pacotes de requisição (Echo request) e resposta (Echo reply).

---

## 2. Metodologia

1. O Wireshark foi iniciado com captura na interface **wlp1s0** (Wi-Fi)
2. O comando `ping www.google.com` foi executado no terminal
3. A captura foi interrompida e filtrada com o filtro `icmp`
4. Os pacotes ICMPv6 foram analisados individualmente

---

## 3. Resultados

### 3.1 Informações Gerais da Captura

| Campo | Valor |
|-------|-------|
| Interface capturada | wlp1s0 (Wi-Fi) |
| IP de origem (request) | 2804:10dc:d170:500::caa4:3a4a:f2d0:caa1 |
| IP de destino (request) | 2001:4860:4826:7700:: |
| Protocolo | ICMPv6 |
| Tamanho dos pacotes | 118 bytes |

---

### 3.2 Processo do Ping

O comando `ping` utiliza o protocolo ICMP para verificar a conectividade entre dois hosts. O fluxo observado foi:

1. **Echo Request:** O computador enviou um pacote ICMP do tipo *request* para o servidor do Google
2. **Echo Reply:** O servidor respondeu com um pacote ICMP do tipo *reply*, confirmando a conectividade

---

### 3.3 Análise dos Pacotes

**Pacote 123 — Echo Request:**

| Campo | Valor |
|-------|-------|
| Tipo | Echo (ping) request |
| ID | 0x359c |
| Sequência | seq=8 |
| Hop limit | 64 |
| Protocolo | ICMPv6 |
| Tamanho | 118 bytes (944 bits) |

**Pacote 124 — Echo Reply:**

| Campo | Valor |
|-------|-------|
| Tipo | Echo (ping) reply |
| ID | 0x359c |
| Sequência | seq=8 |
| Hop limit | 116 |
| Protocolo | ICMPv6 |
| Tamanho | 118 bytes (944 bits) |

---

### 3.4 Observações

- O mesmo **ID (0x359c)** e **número de sequência (seq=8)** aparecem no request e no reply, confirmando que são um par correspondente.
- O **hop limit** do request é **64** (padrão de saída) e do reply é **116**, indicando quantos saltos (roteadores) o pacote percorreu até chegar ao destino e voltar.
- A captura utilizou **ICMPv6** pois o Google respondeu via **IPv6**, protocolo mais moderno que o IPv4.
- Além dos pings, foram observados pacotes **Neighbor Solicitation** e **Neighbor Advertisement**, que fazem parte do funcionamento normal do ICMPv6 para descoberta de vizinhos na rede.

---

## 4. Conclusão

A captura demonstrou com sucesso o funcionamento do protocolo ICMP através do comando `ping`. Os pacotes de Echo request e Echo reply foram identificados corretamente, com IDs e sequências correspondentes, confirmando a conectividade entre o computador local e os servidores do Google via ICMPv6.
