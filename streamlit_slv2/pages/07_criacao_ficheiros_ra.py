import streamlit as st
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.subheader("Criação de Ficheiros Risk Agility")
t1,t2,t3=st.tabs(["Ativos e Passivos","Ativos","Passivos"])
with t1:
    c1,c2=st.columns(2)
    with c1:
        if st.button("🔄 Actualizar",key="ra7"): st.rerun()
    with c2:
        if st.button("🔴 Reset",key="rst7"): st.warning("Apenas admin")
    df=session.sql("""SELECT process_name AS "Processo",description AS "Descrição",status AS "Status",started_at AS "Início",completed_at AS "Fim" FROM CAVIDA_DEMO.RAW.SLV2_RISK_AGILITY_PROCESSES WHERE reference_date='2025-06-30' ORDER BY process_id""").to_pandas()
    def cs(v):
        if v=="Concluído": return "background-color:#C8E6C9;color:#1B5E20"
        elif v=="Em Curso": return "background-color:#FFF9C4;color:#F57F17"
        return ""
    st.dataframe(df.style.applymap(cs,subset=["Status"]),use_container_width=True,hide_index=True,height=400)
    done=len(df[df["Status"]=="Concluído"]); tot=len(df)
    st.progress(done/tot,text=f"{done}/{tot} concluídos")
with t2: st.info("Idêntico ao processo principal — apenas activos")
with t3: st.info("Idêntico ao processo principal — apenas passivos")
