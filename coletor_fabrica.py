import socket
import json
import sqlite3
from datetime import datetime

HOST = '127.0.0.1'
PORTA = 5000

def criar_banco_dados():
    """Cria o banco de dados SQLite e a tabela se não existirem."""
    conn = sqlite3.connect('fabrica.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras_maquina (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            maquina_id TEXT NOT NULL,
            temperatura REAL NOT NULL,
            pressao REAL NOT NULL,
            total_pecas INTEGER NOT NULL,
            alerta_status TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def iniciar_coletor():
    criar_banco_dados()
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORTA))
    print("=== COLETOR DE DADOS CONECTADO AO CLP ===\n")

    conn_db = sqlite3.connect('fabrica.db')
    cursor = conn_db.cursor()

    buffer = ""
    try:
        while True:
            data = client.recv(1024).decode('utf-8')
            if not data:
                break
                
            buffer += data
            while "\n" in buffer:
                linha, buffer = buffer.split("\n", 1)
                if linha.strip():
                    leitura = json.loads(linha)
                    
                    # Regra de negócio simples (Alarme de Alta Temperatura)
                    status = "OK"
                    if leitura["temperatura_c"] > 88.0:
                        status = "ALERTA: SOBREAQUECIMENTO"
                    
                    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Inserção no banco de dados
                    cursor.execute('''
                        INSERT INTO leituras_maquina 
                        (data_hora, maquina_id, temperatura, pressao, total_pecas, alerta_status)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        agora,
                        leitura["maquina_id"],
                        leitura["temperatura_c"],
                        leitura["pressao_bar"],
                        leitura["total_pecas"],
                        status
                    ))
                    conn_db.commit()

                    print(f"[{agora}] Registrado -> Temp: {leitura['temperatura_c']}°C | Status: {status}")

    except KeyboardInterrupt:
        print("\n[ENCERRADO] Coletor finalizado pelo usuário.")
    finally:
        conn_db.close()
        client.close()

if __name__ == "__main__":
    iniciar_coletor()