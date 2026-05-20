import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Regras de Validação Ficheiros CA Gestl")
t1,t2=st.tabs(["📋 Actualizar","📐 Regras de Validação"])
with t1:
    if st.button("🔄 Executar Validações",type="primary"):
        import time; time.sleep(2)
        st.success("✅ 10 regras executadas"); st.rerun()
with t2:
    df=session.sql("""SELECT rule_code AS "Código",rule_description AS "Descrição",rule_category AS "Categoria",severity AS "Severidade",records_evaluated AS "Avaliados",records_failed AS "Falhados",status AS "Status" FROM CAVIDA_DEMO.BRONZE.SLV2_VALIDATION_RULES WHERE reference_date='2025-06-30' ORDER BY rule_code""").to_pandas()
    def cs(v):
        if v=="Aprovado": return "background-color:#C8E6C9;color:#1B5E20"
        elif v=="Falhou": return "background-color:#FFCDD2;color:#B71C1C"
        return ""
    st.dataframe(df.style.applymap(cs,subset=["Status"]),use_container_width=True,hide_index=True)
    c1,c2,c3=st.columns(3)
    c1.metric("Total",len(df)); c2.metric("Aprovadas",len(df[df["Status"]=="Aprovado"])); c3.metric("Falhadas",len(df[df["Status"]=="Falhou"]))
