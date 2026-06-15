# Trabalho 2 de Redes II.
# Participantes: Augusto Santos, Deivid Camargos, Marcus Miller, Camila Barbosa.

import socket
import threading

def gerenciar_cliente(conexao, endereco):
    # Informa no console que um novo cliente ingressou na rede
    print(f"[NOVA CONEXÃO] Cliente conectado do endereço: {endereco}")
    
    try:
        # Mantém a comunicação ativa enquanto o cliente estiver conectado
        while True:
            # Recebe os pacotes de rede com limite de 1024 bytes
            dados = conexao.recv(1024)
            
            # Encerra o processamento se o pacote recebido estiver vazio (desconexão)
            if not dados:
                break
                
            # Transforma os bytes brutos da rede em texto legível
            mensagem = dados.decode('utf-8')
            
            # Rejeita a mensagem e avisa o cliente caso ela contenha apenas espaços vazios
            if not mensagem.strip():
                print(f"[{endereco}] Tentativa de envio de mensagem vazia rejeitada.")
                conexao.send("Erro: A mensagem não pode ser vazia.".encode('utf-8'))
                continue
                
            # Exibe a informação recebida com sucesso
            print(f"[{endereco}] Mensagem recebida: {mensagem}")
            
            # Codifica e despacha a confirmação oficial de volta para o emissor
            resposta = "Mensagem recebida com sucesso pelo servidor."
            conexao.send(resposta.encode('utf-8'))
            
    except Exception as e:
        # Registra falhas inesperadas de rede durante a transmissão
        print(f"[ERRO] Ocorreu uma falha na comunicação com {endereco}: {e}")
        
    finally:
        # Garante a devolução dos recursos e o fechamento do canal ao sistema operacional
        conexao.close()
        print(f"[DESCONECTADO] Conexão encerrada com o endereço: {endereco}")

def iniciar_servidor():
    # Instancia o socket principal configurado para tráfego TCP em redes IPv4
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Coleta as configurações manuais ou aplica os padrões caso o usuário pressione Enter
    ip_host = input("Digite o IP de escuta (pressione Enter para 0.0.0.0/todas as redes): ") or '0.0.0.0'
    porta = input("Digite a porta de escuta (pressione Enter para 5000): ")
    porta = int(porta) if porta else 5000
    
    try:
        # Tenta acoplar o servidor ao endereço fornecido e à porta especificada
        servidor.bind((ip_host, porta))
    except Exception as e:
        # Aborta a execução se o sistema operacional recusar a alocação da porta
        print(f"[ERRO] Não foi possível iniciar o servidor na porta {porta}: {e}")
        return

    # Inicia a fila de espera para aceitar pedidos de comunicação entrantes
    servidor.listen()
    print(f"[STATUS] Servidor ativo e aguardando conexões em {ip_host}:{porta}...")
    
    try:
        # Executa o loop infinito para absorver múltiplos clientes simultaneamente
        while True:
            # Trava o servidor momentaneamente até que um aperto de mãos (handshake) ocorra
            conexao, endereco = servidor.accept()
            
            # Direciona o cliente aceito para uma linha de execução paralela independente
            thread = threading.Thread(target=gerenciar_cliente, args=(conexao, endereco))
            thread.daemon = True 
            thread.start()
            
    except KeyboardInterrupt:
        # Permite o desligamento seguro do script ao interceptar o comando Ctrl+C
        print("\n[STATUS] Desligando o servidor...")
    finally:
        # Derruba o soquete de escuta matriz, finalizando a aplicação
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()