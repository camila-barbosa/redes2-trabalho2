# Trabalho 2 de Redes II.
# Participantes: Augusto Santos, Deivid Camargos, Marcus Miller, Camila Barbosa.

import socket

def iniciar_cliente():
    # Cria o socket TCP utilizando IPv4
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conecta ao servidor no endereço e porta especificados
        cliente.connect(('localhost', 5000))
        print("[SUCESSO] Conectado ao servidor TCP.")
        
        # Solicita a entrada do usuário no console
        mensagem = input("Digite a mensagem que deseja enviar: ")
        
        # Requisito 3a: Validação para impedir o envio de mensagens vazias
        if not mensagem.strip():
            print("[AVISO] Operação cancelada: Não é permitido enviar mensagens vazias.")
            return
            
        # Envia a mensagem codificada em bytes (UTF-8)
        cliente.send(mensagem.encode('utf-8'))
        
        # Aguarda e recebe a confirmação enviada pelo servidor
        resposta = cliente.recv(1024)
        print(f"[SERVIDOR]: {resposta.decode('utf-8')}")
        
    except ConnectionRefusedError:
        print("[ERRO] Não foi possível conectar ao servidor. Certifique-se de que ele está rodando.")
    except Exception as e:
        print(f"[ERRO] Ocorreu uma falha durante a execução: {e}")
    finally:
        # Requisito 3b: Garante o encerramento seguro da conexão após o término
        cliente.close()
        print("[STATUS] Conexão com o servidor finalizada com segurança.")

if __name__ == "__main__":
    iniciar_cliente()