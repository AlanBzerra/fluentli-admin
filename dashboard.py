import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- TENTATIVA DE IMPORTAR O DESENHO LIVRE ---
try:
    from streamlit_excalidraw import excalidraw
    HAS_DRAWING = True
except ImportError:
    HAS_DRAWING = False

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Fluentli Hub", page_icon="🚀", layout="wide")

# --- ESTILO CSS PRO ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .kanban-card {
        background-color: #262730; padding: 15px; border-radius: 8px;
        margin-bottom: 10px; border-left: 5px solid #555; color: white;
    }
    .status-todo { border-left-color: #FF4B4B; }
    .status-doing { border-left-color: #FFAA00; }
    .status-done { border-left-color: #00CC96; }
</style>
""", unsafe_allow_html=True)

# --- DADOS ---
if 'kanban_db' not in st.session_state:
    st.session_state.kanban_db = [
        {"id": 1, "task": "Configurar Wav2Vec2", "status": "Feito", "tag": "AI"},
        {"id": 2, "task": "Interface Neon", "status": "Feito", "tag": "Front"},
        {"id": 3, "task": "Dashboard Livre", "status": "Fazendo", "tag": "Gestão"},
    ]
if 'mvp_text' not in st.session_state:
    st.session_state.mvp_text = "Documentação do MVP:\n1. Backend processa áudio...\n2. IA corrige..."

# --- SIDEBAR (MÉTRICAS) ---
with st.sidebar:
    st.title("📊 Status")
    total = len(st.session_state.kanban_db)
    done = len([t for t in st.session_state.kanban_db if t['status'] == 'Feito'])
    progresso = int((done / total) * 100) if total > 0 else 0
    
    fig = go.Figure(data=[go.Pie(labels=['Feito', 'Restante'], values=[progresso, 100-progresso], hole=.7, marker_colors=['#00CC96', '#333'])])
    fig.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0), height=150, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"<h3 style='text-align:center'>{progresso}% Pronto</h3>", unsafe_allow_html=True)

# --- ÁREA PRINCIPAL ---
st.title("🚀 Fluentli V2 - Command Center")

# AVISO DE ERRO AMIGÁVEL (SE O SERVIDOR FALHAR)
if not HAS_DRAWING:
    st.warning("⚠️ O módulo de desenho (Excalidraw) não foi instalado pelo servidor. Verifique o requirements.txt. As outras abas funcionam normal.")

tab_draw, tab_kanban, tab_docs = st.tabs(["🎨 Quadro Branco", "📌 Kanban Visual", "📝 Docs"])

# ABA 1: DESENHO (Só aparece se o servidor instalar)
with tab_draw:
    if HAS_DRAWING:
        st.subheader("Arquitetura Livre")
        st.info("Desenhe livremente: Use a barra superior para criar formas e textos.")
        excalidraw(height=700)
    else:
        st.error("Erro de Dependência: O servidor não instalou 'streamlit-excalidraw'.")
        st.markdown("Por favor, delete o App no Streamlit Cloud e crie novamente para forçar a instalação.")

# ABA 2: KANBAN
with tab_kanban:
    with st.expander("➕ Nova Tarefa"):
        t_nome = st.text_input("Tarefa")
        t_tag = st.selectbox("Tag", ["Dev", "Design", "Gestão"])
        if st.button("Adicionar"):
            st.session_state.kanban_db.append({"id": len(st.session_state.kanban_db)+1, "task": t_nome, "status": "A Fazer", "tag": t_tag})
            st.rerun()
            
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("### 🔴 A Fazer")
        for i in st.session_state.kanban_db:
            if i['status'] == 'A Fazer':
                st.markdown(f"<div class='kanban-card status-todo'><b>{i['task']}</b><br><small>{i['tag']}</small></div>", unsafe_allow_html=True)
                if st.button("Mover ➡️", key=f"m1_{i['id']}"): 
                    i['status'] = 'Fazendo'
                    st.rerun()
                    
    with c2:
        st.markdown("### 🟡 Fazendo")
        for i in st.session_state.kanban_db:
            if i['status'] == 'Fazendo':
                st.markdown(f"<div class='kanban-card status-doing'><b>{i['task']}</b><br><small>{i['tag']}</small></div>", unsafe_allow_html=True)
                if st.button("⬅️", key=f"m2_{i['id']}"): 
                    i['status'] = 'A Fazer'
                    st.rerun()
                if st.button("➡️", key=f"m3_{i['id']}"): 
                    i['status'] = 'Feito'
                    st.rerun()

    with c3:
        st.markdown("### 🟢 Feito")
        for i in st.session_state.kanban_db:
            if i['status'] == 'Feito':
                st.markdown(f"<div class='kanban-card status-done'><s>{i['task']}</s></div>", unsafe_allow_html=True)

# ABA 3: DOCS
with tab_docs:
    st.subheader("Dossiê Técnico")
    txt = st.text_area("Edite:", value=st.session_state.mvp_text, height=400)
    if st.button("Salvar"):
        st.session_state.mvp_text = txt
        st.success("Salvo!")
