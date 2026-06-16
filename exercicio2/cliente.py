#Trabalho 2 - Redes de Computadores 2
#Exercício 2: Cliente Echo (UDP)
#Participantes: Augusto do Santos, Camila Santos, Deivid Camargos, Marcos Miller


import socket

# Configurações do servidor
HOST = input("Digite o IP do servidor: ")  # IP digitado na hora da execução
PORT = 6000         # Porta do servidor
BUFFER_SIZE = 65507 # Tamanho máximo seguro para UDP (64KB - headers)
TIMEOUT = 5         # Tempo limite de espera pela resposta (segundos)
LIMITE_MENSAGEM = 65507  # Limite de bytes por mensagem no UDP

def iniciar_cliente():
    #Inicializa e executa o cliente UDP Echo.

    # Cria o socket UDP (SOCK_DGRAM = UDP)
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Define timeout para evitar espera infinita por resposta
    cliente.settimeout(TIMEOUT)

    print("=== Cliente UDP Echo ===")
    print(f"Tentando conectar ao servidor {HOST}:{PORT}")
    print("Digite 'sair' para encerrar.\n")

    while True:
        try:
            # Lê a mensagem do usuário
            mensagem = input("Você: ").strip()

            # Comando de saída
            if mensagem.lower() == 'sair':
                print("[CLIENTE] Encerrando cliente...")
                break

            # Valida mensagem vazia
            if not mensagem:
                print("[CLIENTE] Mensagem vazia. Digite algo para enviar.")
                continue

            # Codifica a mensagem para bytes
            dados = mensagem.encode('utf-8')

            # Valida o tamanho máximo permitido pelo UDP
            if len(dados) > LIMITE_MENSAGEM:
                print(f"[CLIENTE] Mensagem muito longa! Máximo permitido: {LIMITE_MENSAGEM} bytes.")
                continue

            # Envia a mensagem ao servidor
            cliente.sendto(dados, (HOST, PORT))

            # Aguarda o eco do servidor
            resposta, _ = cliente.recvfrom(BUFFER_SIZE)
            print(f"[ECO] {resposta.decode('utf-8')}")

        except socket.timeout:
            # Servidor não respondeu dentro do tempo limite (simula perda de pacote)
            print("[CLIENTE] Tempo limite excedido. O servidor não respondeu.")

        except ConnectionResetError:
            # Servidor fechou a conexão inesperadamente
            print("[CLIENTE] Erro: conexão com o servidor foi resetada.")
            break

        except KeyboardInterrupt:
            # Encerra ao pressionar Ctrl+C
            print("\n[CLIENTE] Encerrando cliente...")
            break

    cliente.close()
    print("[CLIENTE] Cliente encerrado.")

if __name__ == "__main__":
    iniciar_cliente()
