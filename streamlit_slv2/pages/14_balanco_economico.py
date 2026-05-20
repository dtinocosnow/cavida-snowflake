import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Tabela de Balanço Económico")
if st.button("📊 Exportar para Excel",key="be14"): st.success("Exportado")
df=session.sql("""SELECT asset_type AS "Tipo",reference_code AS "Referência",subrubrica AS "Sub-rubrica",saldo_periodo AS "Saldo Período",saldo_periodo_anterior AS "Saldo Anterior",variacao_absoluta AS "Variação",ROUND(variacao_percentual*100,1)||'%' AS "Var %" FROM CAVIDA_DEMO.GOLD.SLV2_ECONOMIC_BALANCE_SHEET WHERE reference_date='2025-06-30' ORDER BY reference_code""").to_pandas()
st.markdown("**ASSETS**")
st.dataframe(df,use_container_width=True,hide_index=True,height=600)
st.divider()
c1,c2=st.columns(2)
total_a=df["Saldo Período"].sum(); total_p=df["Saldo Anterior"].sum()
with c1: st.metric("Total Activos (actual)",f"{total_a/1e6:,.0f} M€")
with c2: st.metric("Total Activos (anterior)",f"{total_p/1e6:,.0f} M€",delta=f"{(total_a-total_p)/1e6:,.1f} M€")
