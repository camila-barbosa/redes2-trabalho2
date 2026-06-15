# Participantes:
# [Augusto Henrique]
# [Camila Barbosa]
# [Deivid Camargo]
# [Marcos Miller]

# 1. Certifique-se de que o 'servidor_ws.py' já esteja rodando em outro terminal.
# 2. Abra uma nova aba de terminal na pasta deste arquivo.
# 3. Execute o comando: python3 cliente_ws.py
# 4. Para testar o chat, abra uma terceira aba de terminal e rode o mesmo comando para simular um segundo usuário.
# 5. Digite suas mensagens e pressione Enter. Para encerrar, digite 'sair'.

import asyncio
import websockets
import sys

async def receber_mensagens(websocket):
    # Tarefa que roda em segundo plano para receber mensagens dos outros
    try:
        async for mensagem in websocket:
            print(f"\n{mensagem}\n> ", end="")
    except websockets.exceptions.ConnectionClosed:
        print("\nConexão encerrada pelo servidor.")

async def cliente_chat():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Conectado ao chat! Digite suas mensagens (ou 'sair' para fechar):")
        
        # Inicia a tarefa de escuta em paralelo
        tarefa_receber = asyncio.create_task(receber_mensagens(websocket))
        
        loop = asyncio.get_running_loop()
        while True:
            # Aguarda a digitação do usuário sem bloquear a thread principal
            mensagem = await loop.run_in_executor(None, sys.stdin.readline)
            mensagem = mensagem.strip()
            
            if mensagem.lower() == 'sair':
                break
            if mensagem:
                await websocket.send(mensagem)
                
        tarefa_receber.cancel()

if __name__ == "__main__":
    asyncio.run(cliente_chat())