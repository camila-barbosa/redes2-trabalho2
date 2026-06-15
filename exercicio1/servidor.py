# Trabalho 2 de Redes II.
# Participantes: Augusto Santos, Deivid Camargos, Marcus Miller, Camila Barbosa.

import socket
import threading

def gerenciar_cliente(conexao, endereco):
    print(f"[NOVA CONEXÃO] Cliente conectado do endereço: {endereco}")
    
    try:
        while True:
            # Recebe os dados enviados pelo cliente (limite de 1024 bytes)
            dados = conexao.recv(1024)
            
            # Se não houver dados, o cliente desconectou abruptamente
            if not dados:
                break
                
            # Decodifica os bytes recebidos para string
            mensagem = dados.decode('utf-8')
            
            # Validação adicional de segurança para mensagem vazia ou espaços
            if not mensagem.strip():
                print(f"[{endereco}] Tentativa de envio de mensagem vazia rejeitada.")
                conexao.send("Erro: A mensagem não pode ser vazia.".encode('utf-8'))
                continue
                
            print(f"[{endereco}] Mensagem recebida: {mensagem}")
            
            # Envia a confirmação de recebimento de volta para o cliente
            resposta = "Mensagem recebida com sucesso pelo servidor."
            conexao.send(resposta.encode('utf-8'))
            
    except Exception as e:
        print(f"[ERRO] Ocorreu uma falha na comunicação com {endereco}: {e}")
        
    finally:
        # Garante o encerramento seguro da conexão com este cliente específico
        conexao.close()
        print(f"[DESCONECTADO] Conexão encerrada com o endereço: {endereco}")

def iniciar_servidor():
    # AF_INET indica IPv4 e SOCK_STREAM indica o protocolo TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define o endereço IP (localhost) e a porta de escuta (5000)
    # O uso do try/except evita falhas se a porta já estiver em uso
    try:
        servidor.bind(('localhost', 5000))
    except Exception as e:
        print(f"[ERRO] Não foi possível iniciar o servidor na porta 5000: {e}")
        return

    # Coloca o servidor em modo de escuta para aguardar conexões
    servidor.listen()
    print("[STATUS] Servidor ativo e aguardando conexões na porta 5000...")
    
    try:
        while True:
            # Aceita uma nova conexão (bloqueia o código até um cliente conectar)
            conexao, endereco = servidor.accept()
            
            # Cria uma nova thread para gerenciar o cliente conectado
            thread = threading.Thread(target=gerenciar_cliente, args=(conexao, endereco))
            thread.daemon = True  # Permite que a thread feche se o servidor principal for encerrado
            thread.start()
            
    except KeyboardInterrupt:
        print("\n[STATUS] Desligando o servidor...")
    finally:
        # Garante o encerramento do socket principal do servidor
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()