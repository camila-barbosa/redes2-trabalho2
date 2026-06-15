# Trabalho 2 de Redes II.
# Participantes: Augusto Santos, Deivid Camargos, Marcus Miller, Camila Barbosa.

import socket
import threading
import sys

# Função executada em paralelo para escutar mensagens do servidor sem travar o teclado
def receber_mensagens(cliente, nome_usuario):
    try:
        while True:
            # Aguarda a chegada de pacotes da rede
            dados = cliente.recv(1024)
            if not dados:
                break
            
            # Decodifica a mensagem recebida do parceiro
            mensagem = dados.decode('utf-8')
            
            # Imprime a mensagem recebida e recria o prompt de digitação atual
            print(f"\n{mensagem}\n[{nome_usuario}]: ", end="")
    except Exception:
        print("\nConexão encerrada pelo servidor ou parceiro.")
    finally:
        # Encerra o socket local em caso de falha de recebimento
        cliente.close()

def iniciar_cliente():
    # Inicializa o socket TCP IPv4
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Coleta as configurações de conexão e o identificador visual do usuário
    ip_servidor = input("Digite o IP do servidor (pressione Enter para localhost): ") or 'localhost'
    porta = input("Digite a porta do servidor (pressione Enter para 5000): ")
    porta = int(porta) if porta else 5000
    nome_usuario = input("Digite o seu nome de usuário: ") or "Você"
    
    try:
        # Estabelece a conexão com o servidor ponte
        cliente.connect((ip_servidor, porta))
        print(f"Conectado ao chat em {ip_servidor}:{porta}. Digite 'sair' a qualquer momento para encerrar.")
        
        # Inicia a thread responsável por receber mensagens simultaneamente em segundo plano
        thread_recebimento = threading.Thread(target=receber_mensagens, args=(cliente, nome_usuario))
        thread_recebimento.daemon = True
        thread_recebimento.start()

        # Loop principal exclusivo para captura de digitação do usuário
        while True:
            texto = input(f"[{nome_usuario}]: ")
            
            # Verifica condição de parada antes de despachar a string
            if texto.strip().lower() == 'sair':
                cliente.send('sair'.encode('utf-8'))
                print("Encerrando o chat...")
                break
            
            # Formata a mensagem acoplando o nome do usuário e injeta na rede
            mensagem_formatada = f"[{nome_usuario}]: {texto}"
            cliente.send(mensagem_formatada.encode('utf-8'))

    except Exception as e:
        print(f"Erro de conexão: {e}")
    finally:
        # Garante o fechamento limpo e a devolução da porta de comunicação
        cliente.close()

if __name__ == "__main__":
    iniciar_cliente()