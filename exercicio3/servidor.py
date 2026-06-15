# Trabalho 2 de Redes II.
# Participantes: Augusto Santos, Deivid Camargos, Marcus Miller, Camila Barbosa.

import socket
import threading

def retransmitir(origem, destino):
    # Tenta manter a comunicação ativa continuamente em segundo plano
    try:
        while True:
            # Recebe até 1024 bytes do cliente de origem
            dados = origem.recv(1024)
            
            # Se os dados forem nulos, a conexão foi perdida ou encerrada
            if not dados:
                break
                
            # Decodifica os bytes em texto para validar o conteúdo
            mensagem = dados.decode('utf-8')
            
            # Interrompe o laço se o comando de encerramento for detectado
            if mensagem.strip().lower() == 'sair':
                break
                
            # Repassa a mensagem original em bytes para o cliente de destino
            destino.send(dados)
    except Exception:
        # Evita que erros de rede quebrem a execução da thread abruptamente
        pass
    finally:
        # Garante o fechamento seguro de ambas as pontas ao finalizar
        origem.close()
        destino.close()

def iniciar_servidor():
    # Cria o socket do servidor definindo o protocolo IPv4 e o padrão TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Coleta as configurações de escuta da rede ou aplica os valores padrão
    ip_host = input("Digite o IP de escuta (pressione Enter para 0.0.0.0): ") or '0.0.0.0'
    porta = input("Digite a porta de escuta (pressione Enter para 5000): ")
    porta = int(porta) if porta else 5000
    
    try:
        # Associa o servidor ao IP e porta definidos
        servidor.bind((ip_host, porta))
    except Exception as e:
        print(f"[ERRO] Falha ao vincular o servidor na porta {porta}: {e}")
        return
    
    # Configura o servidor para aceitar até 2 conexões na fila
    servidor.listen(2)

    print(f"Servidor de chat iniciado em {ip_host}:{porta}. Aguardando o primeiro cliente...")
    # Pausa a execução principal até o primeiro cliente realizar a conexão
    cliente1, endereco1 = servidor.accept()
    print(f"Cliente 1 conectado: {endereco1}. Aguardando parceiro...")

    # Pausa novamente até o segundo cliente ingressar no servidor
    cliente2, endereco2 = servidor.accept()
    print(f"Cliente 2 conectado: {endereco2}. Chat iniciado.")

    # Instancia duas threads para rotear as mensagens em ambas as direções simultaneamente
    thread1 = threading.Thread(target=retransmitir, args=(cliente1, cliente2))
    thread2 = threading.Thread(target=retransmitir, args=(cliente2, cliente1))

    # Inicia a execução das tarefas em paralelo
    thread1.start()
    thread2.start()

if __name__ == "__main__":
    # Garante que o servidor só inicie se o arquivo for executado diretamente
    iniciar_servidor()