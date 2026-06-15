# Trabalho 2 de Redes II.
# Participantes: Augusto Santos, Deivid Camargos, Marcus Miller, Camila Barbosa.

import socket
import threading
import sys

def receber_mensagens(cliente):
    try:
        while True:
            dados = cliente.recv(1024)
            if not dados:
                break
            
            mensagem = dados.decode('utf-8')
            # Imprime a mensagem recebida e recria o prompt de digitação
            print(f"\n[Parceiro]: {mensagem}\n[Você]: ", end="")
    except Exception:
        print("\nConexão encerrada pelo servidor ou parceiro.")
    finally:
        cliente.close()

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        cliente.connect(('localhost', 5000))
        print("Conectado ao chat. Digite 'sair' a qualquer momento para encerrar.")
        
        thread_recebimento = threading.Thread(target=receber_mensagens, args=(cliente,))
        thread_recebimento.daemon = True
        thread_recebimento.start()

        while True:
            mensagem = input("[Você]: ")
            cliente.send(mensagem.encode('utf-8'))
            
            if mensagem.strip().lower() == 'sair':
                print("Encerrando o chat...")
                break

    except Exception as e:
        print(f"Erro de conexão: {e}")
    finally:
        cliente.close()

if __name__ == "__main__":
    iniciar_cliente()