# Exercício 7 - Captura de Tráfego DNS com Wireshark

**Participantes:** Augusto do Santos, Camila Santos, Deivid Camargos, Marcos Miller

---

## 1. Objetivo

Capturar e analisar o tráfego DNS gerado pelo navegador ao acessar um site, identificando o processo de resolução de nomes, os servidores DNS utilizados e os registros DNS obtidos.

---

## 2. Metodologia

1. O Wireshark foi iniciado com captura na interface **wlp1s0** (Wi-Fi)
2. O site **www.google.com** foi acessado no navegador
3. A captura foi interrompida e filtrada com o filtro `dns`
4. Os pacotes DNS foram analisados individualmente

---

## 3. Resultados

### 3.1 Informações Gerais da Captura

| Campo | Valor |
|-------|-------|
| Interface capturada | wlp1s0 (Wi-Fi) |
| IP do computador (origem) | 192.168.3.248 |
| IP do servidor DNS (roteador) | 192.168.3.1 |
| Porta de origem (cliente) | Aleatória (ex: 38688, 36959) |
| Porta de destino (DNS) | 53 |
| Protocolo de transporte | UDP |

---

### 3.2 Processo de Resolução de Nomes

O processo de resolução DNS observado seguiu o fluxo padrão:

1. **Query (Consulta):** O computador (`192.168.3.248`) enviou uma consulta DNS ao servidor (`192.168.3.1`) perguntando pelo endereço IP de `google.com`
2. **Response (Resposta):** O servidor DNS respondeu com o endereço IP resolvido

**Exemplo observado (pacotes 7526 e 7527):**
- Query: `Standard query 0x97c A google.com` — consultando o registro tipo A (IPv4) de google.com
- Response: `Standard query response 0xe97c AAAA google.com AAAA 2800:3f0:4001:839::200e` — resposta com endereço IPv6 (AAAA)

---

### 3.3 Tipos de Registros DNS Observados

| Tipo | Significado | Exemplo observado |
|------|-------------|-------------------|
| A | Endereço IPv4 | `google.com A 172.217.30.74` |
| AAAA | Endereço IPv6 | `google.com AAAA 2800:3f0:4001:839::200e` |
| CNAME | Nome canônico (alias) | `clients6.google.com CNAME clients.l.google.com` |
| SOA | Start of Authority | `ns1.google.com` |
| HTTPS | Registro de serviço HTTPS | Observado em múltiplas consultas |

---

### 3.4 Servidores DNS Utilizados

O servidor DNS utilizado foi o **roteador local** (`192.168.3.1`), que atua como DNS recursivo repassando as consultas para servidores DNS externos (como os do Google: `8.8.8.8`).

---

### 3.5 Análise dos Cabeçalhos DNS

**Pacote de Query (consulta):**
- Source: `192.168.3.248` → Destination: `192.168.3.1`
- Protocolo: UDP, Porta 53
- Tipo: `Standard query`
- Nome consultado: `google.com`

**Pacote de Response (resposta):**
- Source: `192.168.3.1` → Destination: `192.168.3.248`
- Protocolo: UDP, Porta 53
- Tipo: `Standard query response`
- Registros retornados: endereços IPv4 e IPv6 de google.com

---

## 4. Conclusão

A captura demonstrou com sucesso o processo completo de resolução DNS. Ao acessar `www.google.com`, o sistema operacional enviou consultas DNS ao servidor local (roteador), que retornou múltiplos registros incluindo endereços IPv4 (tipo A), IPv6 (tipo AAAA) e aliases (tipo CNAME). O protocolo UDP foi utilizado como transporte na porta 53, conforme o padrão DNS.
