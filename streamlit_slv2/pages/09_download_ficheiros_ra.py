import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Download de Ficheiros de Input para Risk Agility")
if st.button("🔄 Actualizar",key="dl9"): st.rerun()
c1,c2=st.columns([2,1])
with c1: st.selectbox("Pasta",["//SRVPROD","//SRVPROD/RiskAgility/Inputs"],key="f9")
with c2: st.selectbox("Período",["T2/2025","T1/2025","T4/2024"],key="p9")
df=session.sql("""SELECT file_name AS "Ficheiro",file_size_kb||' KB' AS "Tamanho",generated_at AS "Gerado em",status AS "Estado" FROM CAVIDA_DEMO.RAW.SLV2_RISK_AGILITY_FILES WHERE reference_date='2025-06-30' AND direction='Download' ORDER BY file_id""").to_pandas()
for i,row in df.iterrows():
    c1,c2,c3=st.columns([4,1,1])
    with c1: st.text(row["Ficheiro"])
    with c2: st.text(row["Tamanho"])
    with c3: st.button("⬇️",key=f"dl9_{i}")
