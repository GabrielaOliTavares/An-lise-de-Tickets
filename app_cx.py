import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="CX Automation Bot", page_icon="🤖")

st.title("🤖 Assistente de Triagem Inteligente")
st.markdown("---")

# Simulação da Lógica de Automação (Backend)
def processar_mensagem(texto):
    texto = texto.lower()
    if any(p in texto for p in ["quebrado", "estorno", "atraso", "erro"]):
        return "🔴 **Prioridade Alta**: Seu caso foi encaminhado para um especialista humano agora mesmo.", "Alta"
    else:
        return "🟢 **Prioridade Normal**: Entendi sua dúvida! Um de nossos assistentes virtuais responderá em breve.", "Baixa"

# Interface de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do usuário
if prompt := st.chat_input("Como posso ajudar hoje?"):
    # Mostra a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta do "Bot" com base na sua lógica de Python
    resposta_texto, prioridade = processar_mensagem(prompt)
    
    # Mostra a resposta do Bot
    with st.chat_message("assistant"):
        st.markdown(resposta_texto)
    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})

    # Barra lateral com metadados técnicos (Diferencial analítico)
    with st.sidebar:
        st.subheader("Painel do Controller (CX)")
        st.write(f"**Última Mensagem:** {prompt}")
        st.write(f"**Prioridade Identificada:** {prioridade}")
        st.progress(100 if prioridade == "Alta" else 30)