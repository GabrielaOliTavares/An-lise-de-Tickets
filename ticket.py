import pandas as pd

# 1. Carregando os dados (Simulando a exportação do Zendesk)

data = {
    'id': [101, 102, 103, 104],
    'mensagem': [
        "Meu produto veio quebrado, quero estorno!",
        "Como mudo meu endereço?",
        "O sistema está fora do ar, não consigo pagar.",
        "Gostei muito do atendimento, nota 10."
    ]
}
df = pd.DataFrame(data)

# 2. Lógica de Automação (Diferencial para a vaga)
def classificar_prioridade(texto):
    urgentes = ["quebrado", "estorno", "fora do ar", "erro", "pagamento"]
    if any(palavra in texto.lower() for palavra in urgentes):
        return "ALTA - Encaminhar p/ Humano"
    return "BAIXA - Bot pode resolver"

# 3. Aplicando a lógica em massa
df['prioridade'] = df['mensagem'].apply(classificar_prioridade)

# 4. Exibindo o resultado
print("--- RELATÓRIO DE TRIAGEM AUTOMATIZADA ---")
print(df)
