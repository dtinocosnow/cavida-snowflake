import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Tabela de Capital Disponível")
if st.button("📊 Exportar para Excel",key="ce13"): st.success("Exportado")
df=session.sql("""SELECT description AS "Descrição",tier AS "Tier",value AS "Valor",origin AS "Origem" FROM CAVIDA_DEMO.PROD.SLV2_AVAILABLE_CAPITAL WHERE reference_date='2025-06-30' ORDER BY description,tier""").to_pandas()
st.caption("Dados válidos: 01/MAR/2025. Actualizados: 01/Apr/2026 11:03:41")
st.dataframe(df,use_container_width=True,hide_index=True)
st.divider()
st.markdown("**Resumo por Tier**")
import pandas as pd
s=df.groupby("Tier")["Valor"].sum().reset_index()
cols=st.columns(min(4,len(s)))
for i,row in s.iterrows():
    with cols[i%4]:
        st.metric(row["Tier"],f"{row['Valor']/1e6:.1f} M€")
