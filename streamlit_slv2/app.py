import streamlit as st
import os

st.set_page_config(page_title="SLV II Workflow — CA Vida", page_icon="🏛️", layout="wide", initial_sidebar_state="collapsed")

STEPS = [
    "Período de Referência",
    "Importação Carteira Investimentos",
    "Estado Carregamento CA Gestl",
    "Regras de Validação",
    "Reconciliação Carteira de Activos",
    "Reconciliação Risk Agility (Activos)",
    "Criação Ficheiros Risk Agility",
    "Reconciliação Risk Agility (Passivos)",
    "Download Ficheiros Risk Agility",
    "Importação Output Risk Agility",
    "Estado Importação Risk Agility",
    "Carregamento Tagetik",
    "Capital Disponível",
    "Balanço Económico",
    "Fecho Report SLV II",
    "Download Ficheiros Tagetik"
]

if "current_step" not in st.session_state:
    st.session_state.current_step = 0

st.markdown("""
<style>
.header-bar {background:linear-gradient(135deg,#1B5E20 0%,#388E3C 100%);padding:16px 24px;border-radius:8px;color:white;margin-bottom:16px;}
.header-bar h2{margin:0;color:white;} .header-bar p{margin:4px 0 0 0;opacity:0.85;}
</style>
<div class="header-bar">
<h2>🏛️ Workflow Solvency II — CA Vida</h2>
<p>Processo de Reporting Regulatório | Plataforma Snowflake</p>
</div>
""", unsafe_allow_html=True)

cols = st.columns(16)
for i in range(16):
    with cols[i]:
        btn_type = "primary" if i == st.session_state.current_step else "secondary"
        if st.button(f"P{i+1}", key=f"nav_{i}", type=btn_type):
            st.session_state.current_step = i
            st.rerun()

st.markdown(f"### Passo {st.session_state.current_step+1}: {STEPS[st.session_state.current_step]}")
st.divider()

from snowflake.snowpark.context import get_active_session
session = get_active_session()

page_files = [
    "01_periodo_referencia.py","02_importacao_carteira.py","03_estado_carregamento.py",
    "04_regras_validacao.py","05_reconciliacao_activos.py","06_reconciliacao_ra_activos.py",
    "07_criacao_ficheiros_ra.py","08_reconciliacao_ra_passivos.py","09_download_ficheiros_ra.py",
    "10_importacao_output_ra.py","11_estado_importacao_ra.py","12_carregamento_tagetik.py",
    "13_capital_disponivel.py","14_balanco_economico.py","15_fecho_report.py","16_download_tagetik.py"
]

page_path = os.path.join(os.path.dirname(__file__), "pages", page_files[st.session_state.current_step])
with open(page_path) as f:
    exec(f.read(), {"st": st, "session": session, "__builtins__": __builtins__})

st.divider()
c1, c2, c3 = st.columns([1,6,1])
with c1:
    if st.session_state.current_step > 0:
        if st.button("⬅️ Anterior"):
            st.session_state.current_step -= 1
            st.rerun()
with c3:
    if st.session_state.current_step < 15:
        if st.button("Seguinte ➡️"):
            st.session_state.current_step += 1
            st.rerun()
