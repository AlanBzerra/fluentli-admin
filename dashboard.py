import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit.components.v1 as components # O TRUQUE ESTÁ AQUI

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Fluentli Hub", page_icon="🚀", layout="wide")

# --- ESTILO ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .kanban-card { background-color: #262730; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #555; color: white; }
    .status-todo { border-left-color: #FF4B4B; }
    .status-doing { border-left-color: #FFAA00; }
    .status-done { border-left-color: #00CC96; }
</style>
""", unsafe_allow_html=True)

# --- DADOS (MEMÓRIA) ---
if 'kanban_db' not in st.session_state:
    st.session_state.kanban_db = [
        {"id": 1, "task": "Interface Neon", "status": "Feito", "tag": "Front"},
        {"id": 2, "task": "Dashboard Whiteboard", "status": "Fazendo", "tag": "Gestão"},
    ]
if 'mvp_text' not in st.session_state:
    st.session_state.mvp_text = "Documentação do MVP:\n1. Backend processa áudio...\n2. IA corrige..."

# --- SIDEBAR ---
with st.sidebar:
    st.title("📊 Status")
    # Gráfico simples para não dar erro
    done = len([t for t in st.session_state.kanban_db if t['status'] == 'Feito'])
    total = len(st.session_state.kanban_db)
    progresso = int((done/total)*100) if total > 0 else 0
    st.metric("Progresso", f"{progresso}%")

# --- ÁREA PRINCIPAL ---
st.title("🚀 Fluentli V2 - Command Center")

tab_draw, tab_kanban, tab_docs = st.tabs(["🎨 Quadro Branco (Livre)", "📌 Kanban Visual", "📝 Docs"])

# ==============================================================================
# ABA 1: QUADRO BRANCO (HACK DO IFRAME - ZERO ERRO)
# ==============================================================================
with tab_draw:
    st.subheader("Arquitetura Livre")
    st.caption("Desenhe, arraste e solte livremente. Ferramenta embutida via Web.")
    
    # AQUI ESTÁ A MÁGICA. Em vez de instalar biblioteca, usamos o site direto.
    # Isso traz a versão COMPLETA do Excalidraw para dentro do seu app.
    components.iframe("https://excalidraw.com/", height=800, scrolling=True)

# ==============================================================================
# ABA 2: KANBAN
# ==============================================================================
with tab_kanban:
    with st.expander("➕ Nova Tarefa"):
        t_nome = st.text_input("Tarefa")
        t_tag = st.selectbox("Tag", ["Dev", "Design", "Gestão"])
        if st.button("Adicionar"):
            st.session_state.kanban_db.append({"id": len(st.session_state.kanban_db)+1, "task": t_nome, "status": "A Fazer", "tag": t_tag})
            st.rerun()

    c1, c2, c3 = st.columns(3)
    
    # Colunas visuais
    cols = {"A Fazer": c1, "Fazendo": c2, "Feito": c3}
    colors = {"A Fazer": "status-todo", "Fazendo": "status-doing", "Feito": "status-done"}
    
    for status, col in cols.items():
        with col:
            st.markdown(f"### {status}")
            for i in st.session_state.kanban_db:
                if i['status'] == status:
                    st.markdown(f"<div class='kanban-card {colors[status]}'><b>{i['task']}</b><br><small>{i['tag']}</small></div>", unsafe_allow_html=True)
                    # Botões de movimento simples
                    if status == "A Fazer" and st.button("➡️", key=f"go_{i['id']}"):
                        i['status'] = "Fazendo"
                        st.rerun()
                    if status == "Fazendo" and st.button("✅", key=f"fin_{i['id']}"):
                        i['status'] = "Feito"
                        st.rerun()

# ==============================================================================
# ABA 3: DOCS
# ==============================================================================
with tab_docs:
    st.subheader("Dossiê Técnico")
    txt = st.text_area("Edite:", value=st.session_state.mvp_text, height=400)
    if st.button("Salvar na Sessão"):
        st.session_state.mvp_text = txt
        st.success("Salvo!")
