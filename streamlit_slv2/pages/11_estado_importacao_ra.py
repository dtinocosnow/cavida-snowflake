import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Estado da Importação do ficheiro do Risk Agility")
c1,c2=st.columns(2)
with c1:
    if st.button("🔄 Actualizar",key="r11"): st.rerun()
with c2:
    if st.button("🔴 Reset",key="rs11"): st.warning("Apenas admin")
df=session.sql("""SELECT file_name AS "Processo",file_type AS "Descrição",CASE WHEN status='Disponível' THEN 'Concluído' ELSE status END AS "Status" FROM CAVIDA_DEMO.RAW.SLV2_RISK_AGILITY_FILES WHERE reference_date='2025-06-30' AND file_type='Output' LIMIT 1""").to_pandas()
if len(df)>0:
    def cs(v):
        if v=="Concluído": return "background-color:#C8E6C9;color:#1B5E20"
        elif v=="Pendente": return "background-color:#FFF9C4;color:#F57F17"
        return ""
    st.dataframe(df.style.applymap(cs,subset=["Status"]),use_container_width=True,hide_index=True)
else:
    st.info("Nenhum ficheiro importado para este período")
