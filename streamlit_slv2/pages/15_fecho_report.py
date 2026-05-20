import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Fecho Report de SLV II")
if st.button("🔒 Fecho Report SLV II",type="primary",key="close15"):
    import time; time.sleep(3)
    session.sql("UPDATE CAVIDA_DEMO.PROD.SLV2_REPORT_STATUS SET status='Fechado',closed_by=CURRENT_USER(),closed_at=CURRENT_TIMESTAMP() WHERE reference_date='2025-06-30' AND status='Em Curso'").collect()
    st.success("✅ Report SLV II fechado!"); st.balloons()
c1,c2=st.columns(2)
with c1:
    if st.button("🔄 Actualizar",key="r15"): st.rerun()
with c2:
    if st.button("🔴 Reset",key="rs15"): st.warning("Apenas admin")
st.markdown("**Status execução batch**")
df=session.sql("SELECT report_name AS \"Relatório\",reference_date AS \"Data\",status AS \"Status\",closed_by AS \"Fechado por\",closed_at AS \"Data Fecho\" FROM CAVIDA_DEMO.PROD.SLV2_REPORT_STATUS ORDER BY reference_date DESC").to_pandas()
def cs(v):
    if v=="Fechado": return "background-color:#C8E6C9;color:#1B5E20"
    elif v=="Em Curso": return "background-color:#FFF9C4;color:#F57F17"
    return ""
st.dataframe(df.style.applymap(cs,subset=["Status"]),use_container_width=True,hide_index=True)
