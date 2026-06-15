#Trabalho 2 - Redes de Computadores 2
#Exercício 2: Servidor Echo (UDP)
#Participantes: Augusto do Santos, Camila Santos, Deivid Camargos, Marcos Miller

import socket

# Configurações do servidor
HOST = '0.0.0.0'  # Aceita conexões de qualquer interface
PORT = 6000       # Porta definida no enunciado
BUFFER_SIZE = 65507  # Tamanho máximo seguro para UDP (64KB - headers)

def iniciar_servidor():
    """Inicializa e executa o servidor UDP Echo."""

    # Cria o socket UDP (SOCK_DGRAM = UDP)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Vincula o socket ao endereço e porta
    servidor.bind((HOST, PORT))
    print(f"[SERVIDOR] Aguardando mensagens na porta {PORT}...")

    while True:
        try:
            # Recebe a mensagem e o endereço do cliente
            dados, endereco_cliente = servidor.recvfrom(BUFFER_SIZE)
            mensagem = dados.decode('utf-8')

            print(f"[SERVIDOR] Mensagem recebida de {endereco_cliente}: {mensagem}")

            # Envia a mensagem de volta (eco)
            servidor.sendto(dados, endereco_cliente)
            print(f"[SERVIDOR] Eco enviado para {endereco_cliente}")

        except UnicodeDecodeError:
            # Erro ao decodificar a mensagem recebida
            print(f"[SERVIDOR] Erro: mensagem inválida recebida de {endereco_cliente}")

        except KeyboardInterrupt:
            # Encerra o servidor ao pressionar Ctrl+C
            print("\n[SERVIDOR] Encerrando servidor...")
            break

    servidor.close()
    print("[SERVIDOR] Servidor encerrado.")

if __name__ == "__main__":
    iniciar_servidor()
