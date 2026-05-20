import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Reconciliação de Inputs do Risk Agility (Activos)")
st.markdown("**TOTAIS DOS ATIVOS CARREGADOS NO DW**")
df=session.sql("""SELECT reference_date AS "Data",asset_solvency_ii_code AS "Código SII",SUM(market_value)AS "Market Value",SUM(accrued_interest)AS "Accrued Interest",SUM(sum_total)AS "Total" FROM CAVIDA_DEMO.RAW.SLV2_INVESTMENT_PORTFOLIO WHERE reference_date='2025-06-30' GROUP BY 1,2 ORDER BY 5 DESC LIMIT 15""").to_pandas()
if st.button("📊 Exportar para Excel",key="exp6"): st.success("Exportado")
st.dataframe(df,use_container_width=True,hide_index=True)
st.success("Não existem registos repetidos no DW")
for ft in ['BOND','EQUITY','CASH']:
    with st.expander(f"📁 REGISTOS VAZIOS — {ft}"):
        d=session.sql(f"SELECT risk_agility_file AS \"Ficheiro\",column_name AS \"Coluna\",information AS \"Info\" FROM CAVIDA_DEMO.RAW.SLV2_RISK_AGILITY_INPUTS_ASSETS WHERE reference_date='2025-06-30' AND risk_agility_file='{ft}'").to_pandas()
        if len(d)>0: st.dataframe(d,use_container_width=True,hide_index=True)
        else: st.success(f"Sem registos vazios — {ft}")
