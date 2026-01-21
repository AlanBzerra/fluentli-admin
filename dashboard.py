import streamlit as st
import pandas as pd
from streamlit_excalidraw import excalidraw
from streamlit_sortables import sort_items

# --- 1. CONFIGURAÇÃO E CSS PROFISSIONAL (O VISUAL QUE VOCÊ GOSTA) ---
st.set_page_config(page_title="Fluentli Ultimate Hub", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    /* Fundo Dark Profissional */
    .stApp { background-color: #0E1117; }
    
    /* Estilo dos Textos */
    h1, h2, h3 { color: #4F8BF9 !important; font-family: 'Roboto', sans-serif; }
    
    /* Ajuste para o componente de Kanban ficar bonito */
    div[data-testid="stVerticalBlock"] > div {
        background-color: transparent;
    }
    
    /* Cards de Métricas */
    .metric-box {
        background: #1E1E1E;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. MEMÓRIA (SESSION STATE) ---
# Inicializa as colunas do Kanban se não existirem
if 'kanban_state' not in st.session_state:
    st.session_state.kanban_state = {
        "todo": ["Otimizar Backend (Python)", "Configurar Wav2Vec2"],
        "doing": ["Dashboard V3 (Ultimate)"],
        "done": ["Interface Neon", "Integração Gemini"]
    }

if 'mvp_docs' not in st.session_state:
    st.session_state.mvp_docs = """
    📘 DOCUMENTAÇÃO MVP (Editável)
    --------------------------------
    1. Arquitetura: Híbrida (Expo + Hugging Face).
    2. IA: Gemini Pro para lógica + Wav2Vec2 para fonética.
    3. Status: Interface pronta, falta otimizar latência.
    """

# --- 3. BARRA SUPERIOR (MÉTRICAS REAIS) ---
st.title("🧠 Fluentli V2 - Engineering Master")
st.markdown("**Status:** 🟢 Sistema Operante | **Versão:** Ultimate Drag & Drop")

# Cálculo de progresso baseado no Kanban
total_tasks = len(st.session_state.kanban_state["todo"]) + len(st.session_state.kanban_state["doing"]) + len(st.session_state.kanban_state["done"])
done_tasks = len(st.session_state.kanban_state["done"])
progress = int((done_tasks / total_tasks) * 100) if total_tasks > 0 else 0

col1, col2, col3 = st.columns(3)
col1.markdown(f'<div class="metric-box"><h3>🚀 Progresso</h3><h2>{progress}%</h2></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-box"><h3>📝 Tarefas Totais</h3><h2>{total_tasks}</h2></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-box"><h3>🔥 Sprint Atual</h3><h2>Backend Optimization</h2></div>', unsafe_allow_html=True)

st.markdown("---")

# --- 4. ABAS DO PROJETO ---
tab_board, tab_kanban, tab_docs = st.tabs(["🎨 Quadro Branco (LIVRE)", "📌 Kanban (ARRASTAR E SOLTAR)", "📝 Docs (SALVAR)"])

# ==============================================================================
# ABA 1: ARQUITETURA LIVRE (EXCALIDRAW)
# ==============================================================================
with tab_board:
    st.subheader("🛠️ Bancada de Engenharia (100% Livre)")
    st.info("💡 DICA PRO: Pressione `Win + .` (Windows) ou `Cmd + Ctrl + Espaço` (Mac) para abrir o menu de Emojis e colar ícones de tecnologia (🐍, ⚛️, ☁️) direto no quadro.")
    
    # Este componente permite desenhar, arrastar, conectar linhas manualmente.
    # Nada fixo. Você é o dono do desenho.
    excalidraw(height=800)

# ==============================================================================
# ABA 2: KANBAN COM DRAG & DROP REAL
# ==============================================================================
with tab_kanban:
    st.subheader("Gestão de Tarefas (Drag & Drop)")
    st.caption("Arraste os itens entre as colunas. As mudanças são salvas automaticamente.")

    # O componente 'sort_items' cria as listas arrastáveis
    kanban_data = sort_items(
        [
            st.session_state.kanban_state["todo"],
            st.session_state.kanban_state["doing"],
            st.session_state.kanban_state["done"]
        ],
        multi_containers=True,
        header=["🔴 A FAZER", "🟡 FAZENDO", "🟢 FEITO (CONCLUÍDO)"],
        direction="vertical",
        key="kanban_sortable"
    )

    # Lógica para salvar o estado depois de arrastar
    # O componente retorna a nova lista. Atualizamos a memória.
    if kanban_data:
        st.session_state.kanban_state["todo"] = kanban_data[0]
        st.session_state.kanban_state["doing"] = kanban_data[1]
        st.session_state.kanban_state["done"] = kanban_data[2]

    st.markdown("---")
    
    # Adicionar Nova Tarefa
    with st.expander("➕ Adicionar Nova Tarefa ao Kanban"):
        new_task = st.text_input("Descrição da Tarefa:")
        if st.button("Criar Card"):
            if new_task:
                st.session_state.kanban_state["todo"].append(new_task)
                st.success("Tarefa adicionada em 'A Fazer'! Recarregue a página se não aparecer imediatamente.")
                st.rerun()

# ==============================================================================
# ABA 3: DOCUMENTAÇÃO QUE SALVA
# ==============================================================================
with tab_docs:
    st.subheader("Dossiê Técnico")
    
    # Formulário para garantir o salvamento
    with st.form("docs_form"):
        text_area = st.text_area("Edite o documento:", 
                                 value=st.session_state.mvp_docs, 
                                 height=500)
        
        save_btn = st.form_submit_button("💾 SALVAR DADOS MVP")
        
        if save_btn:
            st.session_state.mvp_docs = text_area
            st.success("✅ Documentação atualizada e salva na memória!")
