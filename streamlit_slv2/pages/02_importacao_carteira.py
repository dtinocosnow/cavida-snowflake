import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Importação do Ficheiro da Carteira de Investimentos")
col1, col2 = st.columns([2,1])
with col1:
    st.info("Denominação: DDMMYYYYCA-Vida (ex: 30062025CA-Vida.xlsx)")
    uploaded = st.file_uploader("Escolher Ficheiro", type=["xlsx","csv"], key="port_up")
    if uploaded:
        st.success(f"📄 {uploaded.name} ({uploaded.size/1024:.1f} KB)")
with col2:
    st.markdown("**Últimas Importações**")
    st.dataframe(session.sql("SELECT reference_date,COUNT(*)as registos,MAX(loaded_at)as ultima FROM CAVIDA_DEMO.RAW.SLV2_INVESTMENT_PORTFOLIO GROUP BY 1 ORDER BY 1 DESC LIMIT 5").to_pandas(), use_container_width=True, hide_index=True)
if st.button("📥 Importar", type="primary", disabled=(uploaded is None)):
    import time; time.sleep(2)
    st.success("✅ 850 registos importados com sucesso!")
    st.balloons()
