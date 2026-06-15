# Trabalho 2 de Redes II.
# Participantes: Augusto Santos, Deivid Camargos, Marcus Miller, Camila Barbosa.

import socket

def iniciar_cliente():
    # Prepara o socket cliente local utilizando o protocolo TCP tradicional
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Solicita o destino e a porta, assumindo localhost se não houver preenchimento
    ip_servidor = input("Digite o IP do servidor (pressione Enter para localhost): ") or 'localhost'
    porta = input("Digite a porta do servidor (pressione Enter para 5000): ")
    porta = int(porta) if porta else 5000
    
    try:
        # Envia a requisição formal de conexão para o IP e porta estipulados
        cliente.connect((ip_servidor, porta))
        print(f"[SUCESSO] Conectado ao servidor TCP em {ip_servidor}:{porta}.")
        
        # Pausa o programa e aguarda a digitação textual do operador da máquina
        mensagem = input("Digite a mensagem que deseja enviar: ")
        
        # Bloqueia o tráfego de rede desnecessário caso a entrada de texto seja inválida
        if not mensagem.strip():
            print("[AVISO] Operação cancelada: Não é permitido enviar mensagens vazias.")
            return
            
        # Converte a mensagem em um formato binário trafegável e a injeta na rede
        cliente.send(mensagem.encode('utf-8'))
        
        # Aguarda ativamente até que a resposta em texto retorne do servidor de destino
        resposta = cliente.recv(1024)
        print(f"[SERVIDOR]: {resposta.decode('utf-8')}")
        
    except ConnectionRefusedError:
        # Intercepta casos onde o servidor de destino está offline ou protegidos por firewalls
        print("[ERRO] Não foi possível conectar ao servidor. Certifique-se de que ele está rodando.")
    except Exception as e:
        # Trata erros sintáticos residuais ou falhas de disco do próprio sistema
        print(f"[ERRO] Ocorreu uma falha durante a execução: {e}")
    finally:
        # Desconecta ativamente e finaliza o programa local
        cliente.close()
        print("[STATUS] Conexão com o servidor finalizada com segurança.")

if __name__ == "__main__":
    iniciar_cliente()