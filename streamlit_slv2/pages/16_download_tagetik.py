import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Download dos ficheiros para o Tagetik")
c1,c2=st.columns([2,1])
with c1: st.selectbox("Pasta",["//SRVPROD","//SRVPROD/Tagetik/Outputs"],key="tf16")
with c2: st.selectbox("Período",["T2/2025","T1/2025","T4/2024"],key="tp16")
st.markdown("**Ficheiros disponíveis:**")
files=[{"name":"QPT5_Profs_Assets_1stHalf2025_30MAY2025_11_09_30.csv","size":"3.2 MB"}]
for f in files:
    c1,c2,c3=st.columns([4,1,1])
    with c1: st.text(f["name"])
    with c2: st.text(f["size"])
    with c3: st.button("⬇️ Download",key=f"dt16_{f['name'][:10]}")
st.info("Ficheiros gerados após conclusão do carregamento Tagetik.")
