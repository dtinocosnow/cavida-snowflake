import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Importação do Ficheiro de Output do Risk Agility")
st.code("Output_Risk_Agility_YYYY_MM_DD.csv")
uploaded=st.file_uploader("Escolher ficheiro",type=["csv"],key="ra10")
if uploaded: st.success(f"📄 {uploaded.name} ({uploaded.size/1024:.1f} KB)")
if st.button("📥 Importar",type="primary",disabled=(uploaded is None),key="imp10"):
    import time; time.sleep(3)
    st.success("✅ Ficheiro importado!"); st.balloons()
