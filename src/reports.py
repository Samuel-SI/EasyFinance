# src/reports.py

def gerar_diagnostico(historico_semanal, entradas, saidas, meses_reserva):
    if len(historico_semanal) < 2:
        return "Coletando dados para seu diagnóstico..."
    
    if entradas == 1 and saidas == 0:
        return "Dados insuficientes para diagnóstico seguro."

    semana_atual = historico_semanal[-1]
    semana_anterior = historico_semanal[-2]
    
    if semana_anterior == 0:
        return "Semana anterior sem registro para comparação."

    taxa = ((semana_atual - semana_anterior) / semana_anterior) * 100
    
    if taxa > 2:
        return f"Taxa de +{taxa:.1f}%. Caminho certo!"
    elif -2 <= taxa <= 2:
        return f"Taxa de {taxa:.1f}%. Operação estabilizada."
    elif semana_atual < 0:
        if meses_reserva >= 6:
            return "Caixa negativo, mas reservas garantem a operação."
        else:
            return f"CUIDADO: Taxa de {taxa:.1f}%. Risco de falência!"
    return f"Atenção: Lucro diminuiu ({taxa:.1f}%)."