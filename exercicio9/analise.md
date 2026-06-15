# Exercício 9 - Captura de Tráfego DHCP com Wireshark

**Participantes:** Augusto do Santos, Camila Santos, Deivid Camargos, Marcos Miller

---

## 1. Objetivo

Capturar e analisar o tráfego DHCP gerado ao conectar e desconectar da rede, identificando o processo de concessão de endereço IP, os servidores DHCP utilizados e as mensagens trocadas.

---

## 2. Metodologia

1. O Wireshark foi iniciado com captura na interface **any**
2. O comando **`sudo dhclient -r`** foi executado para liberar o endereço IP atual
3. O comando **`sudo dhclient`** foi executado para solicitar um novo endereço IP
4. A captura foi filtrada com o filtro `dhcp`
5. Os pacotes DHCP foram analisados individualmente

---

## 3. Resultados

### 3.1 Informações Gerais da Captura

| Campo | Valor |
|-------|-------|
| Interface capturada | any |
| IP do cliente | 10.180.11.42 |
| IP do servidor DHCP | 10.180.8.1 |
| IP concedido ao cliente | 10.180.13.158 |
| Porta de origem (cliente) | 68 |
| Porta de destino (servidor) | 67 |
| Protocolo de transporte | UDP |

---

### 3.2 Processo de Concessão de Endereço IP (DORA)

O processo de concessão DHCP observado seguiu o fluxo completo:

1. **Release:** O cliente (`10.180.11.42`) enviou uma mensagem DHCP Release ao servidor (`10.180.8.1`) para liberar o endereço IP atual
2. **Discover:** O cliente enviou um broadcast DHCP Discover procurando servidores DHCP disponíveis na rede
3. **Offer:** O servidor DHCP (`10.180.8.1`) respondeu com um DHCP Offer oferecendo o endereço `10.180.13.158`
4. **Request:** O cliente enviou um DHCP Request aceitando a oferta do servidor
5. **ACK:** O servidor confirmou a concessão com um DHCP ACK, atribuindo oficialmente o endereço ao cliente
6. **Inform:** O cliente enviou um DHCP Inform para obter configurações adicionais de rede

**Fluxo observado:**
- `Release` → `Discover` → `Offer` → `Request` → `ACK` → `Inform`

---

### 3.3 Análise dos Cabeçalhos DHCP

**Mensagem Release:**
- Source: `10.180.11.42` → Destination: `10.180.8.1`
- Tipo: `DHCP Release`
- Protocolo: UDP, Porta 67/68

**Mensagem Discover:**
- Source: `0.0.0.0` → Destination: `255.255.255.255` (broadcast)
- Tipo: `DHCP Discover`
- Protocolo: UDP, Porta 67/68

**Mensagem Offer:**
- Source: `10.180.8.1` → Destination: `255.255.255.255`
- Tipo: `DHCP Offer`
- IP oferecido: `10.180.13.158`

**Mensagem ACK:**
- Source: `10.180.8.1` → Destination: `10.180.13.158`
- Tipo: `DHCP ACK`
- IP concedido: `10.180.13.158`

---

### 3.4 Capturas de Tela

| Print | Descrição |
|-------|-----------|
| `terminal_dhclient_novo.png` | Terminal com os comandos `dhclient -r` e `dhclient` executados |
| `terminal_tshark.png` | Terminal com a captura via tshark mostrando os pacotes DHCP |
| `wireshark_dhcp_novo.png` | Wireshark com filtro `dhcp` exibindo o fluxo completo de mensagens |

---

## 4. Conclusão

A captura demonstrou com sucesso o processo completo de liberação e concessão de endereço IP via DHCP. Ao executar `sudo dhclient -r`, o cliente enviou um Release liberando o endereço anterior ao servidor `10.180.8.1`. Em seguida, ao executar `sudo dhclient`, o fluxo DORA completo foi observado: Discover (broadcast), Offer (servidor propõe `10.180.13.158`), Request (cliente aceita) e ACK (servidor confirma a concessão). A mensagem Inform ao final indicou que o cliente solicitou configurações adicionais de rede. O protocolo UDP foi utilizado como transporte nas portas 67 (servidor) e 68 (cliente), conforme o padrão DHCP.
