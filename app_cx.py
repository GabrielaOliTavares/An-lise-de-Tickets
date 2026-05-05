import streamlit as st
 
st.set_page_config(page_title="CX Automation Bot", page_icon="🤖", layout="wide")
 
# ─── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
  .option-btn { margin: 4px 0; }
  div[data-testid="stHorizontalBlock"] { gap: 8px; }
  .stButton > button {
      border-radius: 20px;
      border: 1.5px solid #e0e0e0;
      background: #fff;
      color: #333;
      padding: 8px 18px;
      font-size: 14px;
      transition: all 0.2s;
  }
  .stButton > button:hover {
      border-color: #ff6b35;
      color: #ff6b35;
      background: #fff5f2;
  }
</style>
""", unsafe_allow_html=True)
 
# ─── Base de Conhecimento ─────────────────────────────────────────────────────
BASE_CONHECIMENTO = {
    "Meu produto veio quebrado": {
        "prioridade": "Alta",
        "resposta": (
            "Lamentamos muito pelo inconveniente! 😟\n\n"
            "Para resolver o mais rápido possível:\n"
            "1. Fotografe o produto danificado\n"
            "2. Guarde a embalagem original\n"
            "3. **Seu caso já foi sinalizado como Prioridade Alta** e um especialista entrará em contato em até 2h úteis."
        ),
        "tags": ["quebrado", "danificado", "avariado", "chegou quebrado"],
    },
    "Quero o estorno da minha compra": {
        "prioridade": "Alta",
        "resposta": (
            "Entendido! Vamos iniciar o processo de estorno. 💳\n\n"
            "O prazo estimado é de **5 a 10 dias úteis** após a aprovação.\n"
            "**Seu caso foi encaminhado como Prioridade Alta** — um especialista confirmará os dados em breve."
        ),
        "tags": ["estorno", "reembolso", "devolver dinheiro", "cancelar pagamento"],
    },
    "Quero mudar o endereço de entrega": {
        "prioridade": "Normal",
        "resposta": (
            "Claro! Podemos alterar o endereço desde que o pedido ainda não tenha sido despachado. 📦\n\n"
            "Por favor, informe:\n"
            "- Número do pedido\n"
            "- Novo endereço completo com CEP\n\n"
            "Um assistente virtual responderá em breve!"
        ),
        "tags": ["endereço", "entrega", "local de entrega", "mudar endereço"],
    },
    "Meu pedido está atrasado": {
        "prioridade": "Alta",
        "resposta": (
            "Pedimos desculpas pelo atraso! ⏱️\n\n"
            "Estamos verificando sua entrega com a transportadora.\n"
            "**Caso Prioridade Alta** aberto — você receberá uma atualização em até 1h útil."
        ),
        "tags": ["atraso", "atrasado", "não chegou", "demora"],
    },
    "Tenho dúvidas sobre meu pedido": {
        "prioridade": "Normal",
        "resposta": (
            "Estou aqui para ajudar! 😊\n\n"
            "Você pode consultar o status do seu pedido diretamente pelo link de rastreio enviado por e-mail, "
            "ou me informar o número do pedido para que eu verifique para você."
        ),
        "tags": ["dúvida", "status", "onde está", "rastrear"],
    },
}
 
OPCOES_MENU = list(BASE_CONHECIMENTO.keys()) + ["Outro assunto"]
 
# ─── Helpers ──────────────────────────────────────────────────────────────────
 
def detectar_intencao(texto: str) -> str | None:
    texto = texto.lower()
    for titulo, dados in BASE_CONHECIMENTO.items():
        if any(tag in texto for tag in dados["tags"]):
            return titulo
    return None
 
 
def processar_opcao(opcao: str):
    if opcao == "Outro assunto":
        return (
            "🟡 **Transbordo Contextual**: Não encontrei uma resposta automática para isso.\n\n"
            "Desceva sua dúvida com detalhes e um especialista humano vai te atender!"
        ), "Outro", False
    dados = BASE_CONHECIMENTO[opcao]
    prioridade = dados["prioridade"]
    resposta = dados["resposta"]
    if prioridade == "Alta":
        resposta += "\n\n🔴 **Prioridade Alta** — especialista humano acionado agora mesmo."
    else:
        resposta += "\n\n🟢 **Prioridade Normal** — assistente virtual responderá em breve."
    return resposta, prioridade, True
 
 
def reset_avaliacao():
    st.session_state.aguardando_avaliacao = False
    st.session_state.ultima_opcao = None
 
 
# ─── Estado inicial ────────────────────────────────────────────────────────────
defaults = {
    "messages": [],
    "etapa": "menu",          # menu | livre | resolvido
    "prioridade": "—",
    "ultima_msg": "—",
    "aguardando_avaliacao": False,
    "ultima_opcao": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v
 
# ─── Layout ───────────────────────────────────────────────────────────────────
col_chat, col_painel = st.columns([3, 1])
 
with col_painel:
    st.subheader("🎛️ Painel do Controller (CX)")
    st.write(f"**Última Mensagem:** {st.session_state.ultima_msg}")
    st.write(f"**Prioridade Identificada:** {st.session_state.prioridade}")
    nivel = {"Alta": 100, "Normal": 60, "Outro": 30, "—": 5}.get(st.session_state.prioridade, 5)
    st.progress(nivel / 100)
 
    st.markdown("---")
    st.caption("**Fluxo atual:**")
    etapa_label = {
        "menu": "🔵 Seleção de opção",
        "livre": "🟡 Mensagem livre",
        "resolvido": "🟢 Resolvido",
    }.get(st.session_state.etapa, "—")
    st.write(etapa_label)
 
    if st.button("🔄 Reiniciar conversa"):
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()
 
with col_chat:
    st.title("🤖 Assistente de Triagem CX")
    st.markdown("---")
 
    # Exibe histórico
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
 
    # ── ETAPA: MENU (botões de opção) ─────────────────────────────────────────
    if st.session_state.etapa == "menu" and not st.session_state.aguardando_avaliacao:
        if not st.session_state.messages:
            boas_vindas = "Olá! 👋 Como posso ajudar você hoje?\n\nEscolha uma das opções abaixo ou escreva sua dúvida diretamente:"
            st.session_state.messages.append({"role": "assistant", "content": boas_vindas})
            with st.chat_message("assistant"):
                st.markdown(boas_vindas)
 
        # Botões de opção
        st.markdown("**Selecione o motivo do contato:**")
        cols = st.columns(2)
        for i, opcao in enumerate(OPCOES_MENU):
            with cols[i % 2]:
                if st.button(opcao, key=f"btn_{opcao}", use_container_width=True):
                    # Mensagem do usuário
                    st.session_state.messages.append({"role": "user", "content": opcao})
                    st.session_state.ultima_msg = opcao
 
                    # Resposta do bot
                    resposta, prioridade, base_ok = processar_opcao(opcao)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                    st.session_state.prioridade = prioridade
                    st.session_state.aguardando_avaliacao = base_ok
                    st.session_state.ultima_opcao = opcao
 
                    if not base_ok:  # "Outro assunto" → modo livre
                        st.session_state.etapa = "livre"
 
                    st.rerun()
 
    # ── AVALIAÇÃO: "Isso resolveu?" ────────────────────────────────────────────
    if st.session_state.aguardando_avaliacao:
        st.markdown("---")
        st.markdown("**Essa resposta resolveu o seu problema?**")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Sim, resolveu!", use_container_width=True):
                msg = "Ótimo! Fico feliz em ter ajudado. 😊 Seu ticket foi marcado como **resolvido** automaticamente. Até logo!"
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.session_state.etapa = "resolvido"
                reset_avaliacao()
                st.rerun()
        with c2:
            if st.button("❌ Não, preciso de mais ajuda", use_container_width=True):
                msg = (
                    "Entendido! Vou te conectar com um **especialista humano** agora. 🔴\n\n"
                    "Você pode descrever sua situação com mais detalhes abaixo para agilizar o atendimento:"
                )
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.session_state.etapa = "livre"
                st.session_state.prioridade = "Alta"
                reset_avaliacao()
                st.rerun()
 
    # ── ETAPA LIVRE: chat de texto (modo transbordo) ───────────────────────────
    if st.session_state.etapa == "livre":
        if prompt := st.chat_input("Descreva sua dúvida em detalhes..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.ultima_msg = prompt
 
            # Tenta detectar intenção mesmo no texto livre
            intencao = detectar_intencao(prompt)
            if intencao:
                resposta, prioridade, _ = processar_opcao(intencao)
                st.session_state.prioridade = prioridade
                st.session_state.aguardando_avaliacao = True
                st.session_state.ultima_opcao = intencao
            else:
                resposta = (
                    "Obrigado pelo detalhe! 📋 Sua mensagem foi registrada e um **especialista humano** "
                    "irá analisá-la em breve.\n\n"
                    "🔴 **Transbordo ativado** — tempo médio de resposta: 30 minutos."
                )
                st.session_state.prioridade = "Alta"
 
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            st.rerun()
 
    # ── ETAPA: RESOLVIDO ──────────────────────────────────────────────────────
    if st.session_state.etapa == "resolvido":
        st.success("✅ Atendimento encerrado. Ticket marcado como resolvido.")
        st.caption("Clique em **Reiniciar conversa** no painel ao lado para iniciar um novo atendimento.")
 
    # ── Campo de texto também disponível na etapa MENU ─────────────────────────
    if st.session_state.etapa == "menu" and not st.session_state.aguardando_avaliacao:
        if prompt := st.chat_input("Ou escreva sua dúvida diretamente..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.ultima_msg = prompt
 
            intencao = detectar_intencao(prompt)
            if intencao:
                resposta, prioridade, _ = processar_opcao(intencao)
                st.session_state.prioridade = prioridade
                st.session_state.aguardando_avaliacao = True
                st.session_state.ultima_opcao = intencao
            else:
                resposta = (
                    "Não encontrei uma resposta automática para isso. 🤔\n\n"
                    "Selecione uma das opções acima ou descreva melhor sua situação — "
                    "um especialista estará disponível em breve!"
                )
 
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            st.rerun()
