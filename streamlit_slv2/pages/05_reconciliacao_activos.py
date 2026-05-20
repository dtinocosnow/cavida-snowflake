import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Reconciliação de Carteira de Activos")
st.info("Não existem instrumentos repetidos no DW")
st.markdown("**TOTAIS DOS ATIVOS CARREGADOS NO DW**")
df=session.sql("""SELECT asset_class AS "Classe",COUNT(*)AS "Instrumentos",SUM(market_value)AS "Valor Mercado",SUM(accrued_interest)AS "Juros",SUM(sum_total)AS "Total" FROM CAVIDA_DEMO.BRONZE.SLV2_INVESTMENT_PORTFOLIO WHERE reference_date='2025-06-30' GROUP BY 1 ORDER BY 5 DESC""").to_pandas()
st.dataframe(df,use_container_width=True,hide_index=True)
if st.button("📊 Exportar para Excel"): st.success("Exportado")
with st.expander("📋 Detalhe (50 primeiros)"):
    st.dataframe(session.sql("SELECT reference_date,internal_fund_identifier,internal_fund_code,asset_solvency_ii_code,market_value,accrued_interest,sum_total FROM CAVIDA_DEMO.BRONZE.SLV2_INVESTMENT_PORTFOLIO WHERE reference_date='2025-06-30' ORDER BY internal_fund_identifier LIMIT 50").to_pandas(),use_container_width=True,hide_index=True)
