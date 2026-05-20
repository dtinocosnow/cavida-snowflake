import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Actualização do Período de Referência")
df = session.sql("SELECT * FROM CAVIDA_DEMO.RAW.SLV2_REFERENCE_PERIODS ORDER BY report_date DESC").to_pandas()
col1, col2 = st.columns(2)
with col1:
    sel = st.selectbox("Data de Referência", df["REPORT_DATE"].tolist())
    row = df[df["REPORT_DATE"] == sel].iloc[0]
    st.markdown(f"""
| Campo | Valor |
|-------|-------|
| **Entidade** | CA Vida |
| **Data Referência** | {row['REPORT_DATE']} |
| **Tipo Período** | {row['PERIOD_TYPE']} |
| **Período** | Q{row['PERIOD_NUMBER']} |
| **Guarantor Tagetik** | {row['GUARANTOR_TAGETIK']} |
""")
with col2:
    st.dataframe(df[["REPORT_DATE","PERIOD_TYPE","STATUS","UPDATED_BY"]], use_container_width=True, hide_index=True)
is_current = st.checkbox("Reporte Actual", value=(row["STATUS"]=="Em Curso"))
if st.button("💾 Actualizar Período", type="primary"):
    ns = "Em Curso" if is_current else "Aberto"
    session.sql(f"UPDATE CAVIDA_DEMO.RAW.SLV2_REFERENCE_PERIODS SET status='{ns}',updated_at=CURRENT_TIMESTAMP(),updated_by=CURRENT_USER() WHERE report_date='{sel}'").collect()
    st.success(f"✅ Período {sel} actualizado para '{ns}'")
    st.rerun()
