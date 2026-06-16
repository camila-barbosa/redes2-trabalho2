# Participantes:
# [Augusto Henrique]
# [Camila Barbosa]
# [Deivid Camargo]
# [Marcos Miller]

# 1. Certifique-se de que o 'servidor_hora.py' já esteja rodando em outro terminal.
# 2. Abra uma nova aba de terminal nesse msm repo.
# 3. Execute o comando: python3 cliente_hora.py
# 4. O cliente irá se conectar, exibir a hora recebida do servidor e encerrar automaticamente.

import socket

def solicitar_hora():
    HOST = input("Digite o IP do servidor: ")
    PORT = 7000

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conecta ao servidor [cite: 80]
        cliente.connect((HOST, PORT))
        
        # Envia uma solicitação ao servidor
        cliente.send("HORA_ATUAL".encode())
        
        # Recebe e exibe a hora [cite: 81]
        resposta = cliente.recv(1024).decode()
        print(f"Hora recebida do servidor: {resposta}")
        
    except Exception as erro:
        print(f"Erro ao conectar com o servidor: {erro}")
    finally:
        cliente.close()

if __name__ == "__main__":
    solicitar_hora()