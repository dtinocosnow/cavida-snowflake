import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Reconciliação de Inputs do Risk Agility (Passivos)")
st.markdown("**TOTAIS DOS PASSIVOS CARREGADOS NO DW**")
c1,c2=st.columns(2)
with c1:
    if st.button("📊 Exportar Para Excel",key="ep8"): st.success("Exportado")
with c2:
    if st.button("📋 Exportar Tabela",key="et8"): st.success("Exportado")
df=session.sql("""SELECT reference_date AS "Data",risk_agility_input_file AS "Ficheiro RA",math_provisions AS "Math. Provisions",insured_capital AS "Capital Segurado",record_count AS "Registos" FROM CAVIDA_DEMO.BRONZE.SLV2_RISK_AGILITY_INPUTS_LIABILITIES WHERE reference_date='2025-06-30' ORDER BY 2""").to_pandas()
st.dataframe(df,use_container_width=True,hide_index=True)
for ft in ['CAPIT','FIXED','TAE']:
    with st.expander(f"📁 REGISTOS VAZIOS — {ft}"):
        import pandas as pd
        if ft=='CAPIT':
            d=pd.DataFrame({"Ficheiro":["CAPIT"]*3,"Coluna":["ptrans","portfolio_int","action_dc"],"Info":["6081 registos vazios","Totalmente vazia","Totalmente vazia"]})
        elif ft=='FIXED':
            d=pd.DataFrame({"Ficheiro":["FIXED"]*2,"Coluna":["ptrans","ptrans"],"Info":["34 registos vazios","Totalmente vazia"]})
        else:
            d=pd.DataFrame({"Ficheiro":["TAE"],"Coluna":["ptrans"],"Info":["Sem registos vazios"]})
        st.dataframe(d,use_container_width=True,hide_index=True)
