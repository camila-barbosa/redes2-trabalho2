# Participantes:
# [Augusto Henrique]
# [Camila Barbosa]
# [Deivid Camargo]
# [Marcos Miller]

# COMO RODAR O SERVIDOR:
# 1. Abra um terminal Linux nesse repo.
# 2. Execute o comando: python3 servidor_ws.py
# 3. O servidor iniciará o broadcast de mensagens. Mantenha esta aba aberta.

import asyncio
import websockets

# Conjunto para armazenar todos os clientes conectados
clientes_conectados = set()

async def gerenciar_chat(websocket):
    # Adiciona o novo cliente ao set
    clientes_conectados.add(websocket)
    endereco = websocket.remote_address
    print(f"[LOG] Novo usuário conectado: {endereco}")
    
    try:
        # Fica ouvindo mensagens do cliente de forma assíncrona
        async for mensagem in websocket:
            print(f"[LOG] Mensagem recebida de {endereco}: {mensagem}")
            # Faz o broadcast (envia a mensagem) para todos os outros clientes
            for cliente in clientes_conectados:
                if cliente != websocket: # Não envia de volta para quem mandou
                    await cliente.send(f"Usuário {endereco[1]}: {mensagem}")
                    
    except websockets.exceptions.ConnectionClosed:
        # A exceção é capturada silenciosamente aqui para ir direto para o 'finally'
        pass
    finally:
        # Remove o cliente quando ele desconectar
        clientes_conectados.remove(websocket)
        print(f"[LOG] Usuário {endereco} desconectou-se.")
        
        # Avisa os clientes restantes que este usuário saiu
        for cliente in clientes_conectados:
            try:
                await cliente.send(f"--- [AVISO] Usuário {endereco[1]} saiu do chat. ---")
            except websockets.exceptions.ConnectionClosed:
                pass

async def main():
    # Inicia o servidor WebSocket na porta 8765
    async with websockets.serve(gerenciar_chat, "localhost", 8765):
        print("[LOG] Servidor de Chat WebSocket rodando em ws://localhost:8765")
        await asyncio.Future()  # Roda indefinidamente

if __name__ == "__main__":
    asyncio.run(main())