import sqlite3

def gerar_relatorio():
    # Conecta à base de dados existente
    conn = sqlite3.connect('fabrica.db')
    cursor = conn.cursor()

    print("==========================================")
    print("   RELATÓRIO CONSOLIDADO DE PRODUÇÃO     ")
    print("==========================================\n")

    # 1. Verificar total de leituras
    cursor.execute("SELECT COUNT(*) FROM leituras_maquina")
    total_leituras = cursor.fetchone()[0]

    if total_leituras == 0:
        print("Nenhum dado encontrado no banco de dados.")
        conn.close()
        return

    # 2. Média de temperatura e pressão
    cursor.execute("SELECT AVG(temperatura), AVG(pressao) FROM leituras_maquina")
    media_temp, media_pressao = cursor.fetchone()

    # 3. Total de peças produzidas (maior valor registrado no contador)
    cursor.execute("SELECT MAX(total_pecas) FROM leituras_maquina")
    total_pecas = cursor.fetchone()[0]

    # 4. Total de alertas de sobreaquecimento
    cursor.execute("SELECT COUNT(*) FROM leituras_maquina WHERE alerta_status LIKE '%ALERTA%'")
    total_alertas = cursor.fetchone()[0]

    # Exibição no terminal
    print(f"Total de Leituras Registradas: {total_leituras}")
    print(f"Temperatura Média da Prensa:  {media_temp:.1f} °C")
    print(f"Pressão Média Operacional:   {media_pressao:.2f} bar")
    print(f"Total de Peças Produzidas:    {total_pecas} unidades")
    print(f"Alertas de Sobreaquecimento:  {total_alertas} ocorrência(s)")
    print("\n==========================================")

    conn.close()

if __name__ == "__main__":
    gerar_relatorio()