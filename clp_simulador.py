import socket
import json
import time
import random

# Configurações de rede locais (simulando a rede industrial)
HOST = '127.0.0.1'
PORTA = 5000

def iniciar_clp():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORTA))
    server.listen(1)
    
    print("=== SIMULADOR DE CLP INDUSTRIAL INICIADO ===")
    print(f"Aguardando conexão do sistema de coleta na porta {PORTA}...\n")
    
    conn, addr = server.accept()
    print(f"[CONECTADO] Sistema de Coleta conectado via IP: {addr[0]}\n")

    contador_pecas = 0

    try:
        while True:
            contador_pecas += random.randint(1, 3)
            
            # Dados simulados dos sensores da máquina
            dados_maquina = {
                "maquina_id": "PRENSA_01",
                "temperatura_c": round(random.uniform(65.0, 95.0), 1),
                "pressao_bar": round(random.uniform(4.5, 6.0), 2),
                "total_pecas": contador_pecas
            }
            
            # Envia os dados convertidos para JSON
            mensagem = json.dumps(dados_maquina) + "\n"
            conn.sendall(mensagem.encode('utf-8'))
            
            print(f"[CLP ENVIANDO]: Temp: {dados_maquina['temperatura_c']}°C | "
                  f"Pressão: {dados_maquina['pressao_bar']} bar | "
                  f"Peças: {dados_maquina['total_pecas']}")
            
            time.sleep(2) # Envia dados a cada 2 segundos

    except (KeyboardInterrupt, BrokenPipeError):
        print("\n[DESCONECTADO] Simulador encerrado.")
        conn.close()
        server.close()

if __name__ == "__main__":
    iniciar_clp()