# Participantes:
# [Augusto Henrique]
# [Camila Barbosa]
# [Deivid Camargo]
# [Marcos Miller]

# COMO RODAR O SERVIDOR:
# 1. abrir um terminal nesse repo
# 2. executar o comando: python3 servidor_hora.py
# 3. o servidor ficará ativo aguardando conexões. Mantenha esta aba aberta.

import socket
import threading
from datetime import datetime

# Função que cada thread vai executar para atender um cliente
def atender_cliente(conexao, endereco):
    print(f"[LOG] Nova conexão estabelecida com {endereco}")
    try:
        # Aguarda o cliente solicitar a hora
        mensagem = conexao.recv(1024).decode()
        if mensagem:
            # Obtém a hora atual no formato HH:MM:SS [cite: 78]
            hora_atual = datetime.now().strftime("%H:%M:%S")
            conexao.send(hora_atual.encode())
            print(f"[LOG] Solicitação atendida para {endereco}. Hora enviada: {hora_atual}")
    except Exception as erro:
        # Garante que falhas em um cliente não quebrem o servidor [cite: 84]
        print(f"[ERRO] Falha na comunicação com {endereco}: {erro}")
    finally:
        # Encerramento seguro da conexão
        conexao.close()
        print(f"[LOG] Conexão com {endereco} encerrada.")

def iniciar_servidor():
    HOST = '0.0.0.0'
    PORT = 7000 # Porta especificada [cite: 76]

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[LOG] Servidor de Hora rodando em {HOST}:{PORT}")

    try:
        while True:
            conexao, endereco = servidor.accept()
            # Cria e inicia uma nova thread para o cliente conectado [cite: 77]
            thread = threading.Thread(target=atender_cliente, args=(conexao, endereco))
            thread.start()
    except KeyboardInterrupt:
        print("\n[LOG] Servidor encerrado manualmente.")
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()