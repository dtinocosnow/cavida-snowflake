import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Carregamento de dados no Tagetik")
c1,c2,c3=st.columns(3)
with c1:
    if st.button("🔄 Actualizar",key="r12"): st.rerun()
with c2:
    if st.button("🚀 Carregar Tagetik",type="primary",key="load12"):
        import time; time.sleep(3); st.success("✅ Carregamento concluído!")
with c3:
    if st.button("🔴 Reset",key="rs12"): st.warning("Apenas admin")
st.markdown("**PRÉ-REQUISITOS**")
pre=session.sql("SELECT DISTINCT pre_requisite AS \"Pré-Requisito\",pre_req_status AS \"Estado\" FROM CAVIDA_DEMO.RAW.SLV2_TAGETIK_PROCESSES WHERE reference_date='2025-06-30' AND pre_requisite IS NOT NULL").to_pandas()
if len(pre)>0: st.dataframe(pre,use_container_width=True,hide_index=True)
st.divider()
df=session.sql("""SELECT process_name AS "Processo",description AS "Descrição",status AS "Status",started_at AS "Início",completed_at AS "Fim" FROM CAVIDA_DEMO.RAW.SLV2_TAGETIK_PROCESSES WHERE reference_date='2025-06-30' ORDER BY process_id""").to_pandas()
def cs(v):
    if v=="Concluído": return "background-color:#C8E6C9;color:#1B5E20"
    return ""
st.dataframe(df.style.applymap(cs,subset=["Status"]),use_container_width=True,hide_index=True)
