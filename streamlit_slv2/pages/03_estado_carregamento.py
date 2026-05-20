import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Estado do Carregamento Ficheiros CA Gestl")
c1,c2=st.columns(2)
with c1:
    if st.button("🔄 Actualizar",key="ref3"): st.rerun()
with c2:
    if st.button("🔴 Reset",key="rst3"): st.warning("Apenas administradores")
df=session.sql("""SELECT process_name AS "Processo",description AS "Descrição",status AS "Status",loaded_at AS "Data",row_count AS "Registos" FROM CAVIDA_DEMO.RAW.SLV2_CA_GESTL_FILES WHERE reference_date='2025-06-30' ORDER BY file_id""").to_pandas()
def cs(v):
    if v=="Concluído": return "background-color:#C8E6C9;color:#1B5E20"
    elif v=="Em Curso": return "background-color:#FFF9C4;color:#F57F17"
    return ""
st.dataframe(df.style.applymap(cs,subset=["Status"]),use_container_width=True,hide_index=True,height=500)
tot=len(df); done=len(df[df["Status"]=="Concluído"])
st.progress(done/tot,text=f"{done}/{tot} concluídos")
