import streamlit as st
import pandas as pd
import altair as alt
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="SLV II Analytics — CA Vida", page_icon="📊", layout="wide")

session = get_active_session()

st.markdown("""
<style>
[data-testid="stMetric"] {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 16px; border-radius: 12px; color: white; box-shadow: 0 4px 15px rgba(102,126,234,0.3);}
[data-testid="stMetric"] label {color: rgba(255,255,255,0.85) !important;}
[data-testid="stMetric"] [data-testid="stMetricValue"] {color: white !important; font-size: 2rem !important;}
[data-testid="stMetric"] [data-testid="stMetricDelta"] {color: rgba(255,255,255,0.9) !important;}
.main-header {background: linear-gradient(135deg, #1B5E20 0%, #4CAF50 100%); padding: 20px 30px; border-radius: 12px; margin-bottom: 24px;}
.main-header h1 {color: white; margin: 0; font-size: 1.8rem;}
.main-header p {color: rgba(255,255,255,0.85); margin: 4px 0 0 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
<h1>📊 CA Vida — Solvency II Analytics Dashboard</h1>
<p>Dados da camada GOLD | Actualização automática via dbt pipeline</p>
</div>
""", unsafe_allow_html=True)

portfolio = session.sql("SELECT * FROM CAVIDA_DEMO.GOLD.MART_SLV2_REPORT").to_pandas()
capital = session.sql("SELECT * FROM CAVIDA_DEMO.GOLD.SLV2_AVAILABLE_CAPITAL").to_pandas()
balance = session.sql("SELECT * FROM CAVIDA_DEMO.GOLD.MART_ECONOMIC_BALANCE_SHEET").to_pandas()
report_status = session.sql("SELECT * FROM CAVIDA_DEMO.GOLD.SLV2_REPORT_STATUS").to_pandas()

total_portfolio = portfolio["TOTAL_VALUE"].sum()
total_instruments = portfolio["INSTRUMENT_COUNT"].sum()
total_capital_scr = capital[capital["DESCRIPTION"].str.contains("available.*SCR", case=False)]["VALUE"].sum()
n_classes = portfolio["ASSET_CLASS"].nunique()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Carteira Total", f"{total_portfolio/1e9:.2f} B€")
with col2:
    st.metric("Instrumentos", f"{int(total_instruments):,}")
with col3:
    st.metric("Capital SCR", f"{total_capital_scr/1e6:.0f} M€")
with col4:
    st.metric("Classes Activo", n_classes)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["📈 Carteira", "🏦 Capital", "📋 Balanço", "🎯 Status"])

with tab1:
    st.subheader("Distribuição da Carteira de Investimentos")
    col_chart, col_table = st.columns([2, 1])

    with col_chart:
        pie_data = portfolio[["ASSET_CLASS", "TOTAL_VALUE"]].copy()
        pie_data["PCT"] = pie_data["TOTAL_VALUE"] / pie_data["TOTAL_VALUE"].sum() * 100

        donut = alt.Chart(pie_data).mark_arc(innerRadius=60, outerRadius=120).encode(
            theta=alt.Theta("TOTAL_VALUE:Q"),
            color=alt.Color("ASSET_CLASS:N", legend=alt.Legend(title="Classe", orient="bottom")),
            tooltip=["ASSET_CLASS", alt.Tooltip("TOTAL_VALUE:Q", format=",.0f"), alt.Tooltip("PCT:Q", format=".1f")]
        ).properties(height=350, title="Alocação por Classe de Activo")
        st.altair_chart(donut, use_container_width=True)

    with col_table:
        st.markdown("**Top Classes por Valor**")
        display_df = portfolio[["ASSET_CLASS", "TOTAL_VALUE", "INSTRUMENT_COUNT", "PCT_PORTFOLIO"]].sort_values("TOTAL_VALUE", ascending=False)
        display_df["TOTAL_VALUE"] = display_df["TOTAL_VALUE"].apply(lambda x: f"{x/1e6:,.0f} M€")
        display_df.columns = ["Classe", "Valor", "Instr.", "% Port."]
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=350)

    st.subheader("Valor por Classe de Activo")
    bar = alt.Chart(portfolio).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
        x=alt.X("ASSET_CLASS:N", sort="-y", title="Classe de Activo"),
        y=alt.Y("TOTAL_VALUE:Q", title="Valor Total (EUR)"),
        color=alt.Color("ASSET_CLASS:N", legend=None),
        tooltip=["ASSET_CLASS", alt.Tooltip("TOTAL_VALUE:Q", format=",.0f"), "INSTRUMENT_COUNT"]
    ).properties(height=300)
    st.altair_chart(bar, use_container_width=True)

with tab2:
    st.subheader("Capital Disponível por Tipo e Tier")
    col1, col2 = st.columns(2)

    with col1:
        scr_data = capital[capital["DESCRIPTION"].str.contains("SCR", case=False)]
        grouped = scr_data.groupby("TIER")["VALUE"].sum().reset_index()
        grouped["VALUE_M"] = grouped["VALUE"] / 1e6

        tier_chart = alt.Chart(grouped).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
            x=alt.X("TIER:N", title="Tier"),
            y=alt.Y("VALUE_M:Q", title="Valor (M€)"),
            color=alt.Color("TIER:N", scale=alt.Scale(scheme="viridis"), legend=None),
            tooltip=["TIER", alt.Tooltip("VALUE_M:Q", format=",.1f")]
        ).properties(height=300, title="Capital por Tier (SCR)")
        st.altair_chart(tier_chart, use_container_width=True)

    with col2:
        st.markdown("**Detalhe Capital Disponível**")
        cap_display = capital[["DESCRIPTION", "TIER", "VALUE"]].copy()
        cap_display["VALUE"] = cap_display["VALUE"].apply(lambda x: f"{x/1e6:,.1f} M€")
        cap_display.columns = ["Descrição", "Tier", "Valor"]
        st.dataframe(cap_display, use_container_width=True, hide_index=True, height=350)

    st.divider()
    st.subheader("Rácio de Solvência")
    scr_total = capital[capital["DESCRIPTION"].str.contains("available.*SCR")]["VALUE"].sum()
    mcr_total = capital[capital["DESCRIPTION"].str.contains("available.*MCR")]["VALUE"].sum()
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.metric("Capital SCR", f"{scr_total/1e6:,.0f} M€")
    with col_s2:
        st.metric("Capital MCR", f"{mcr_total/1e6:,.0f} M€")
    with col_s3:
        ratio = (scr_total / mcr_total * 100) if mcr_total > 0 else 0
        st.metric("Rácio SCR/MCR", f"{ratio:.0f}%")

with tab3:
    st.subheader("Balanço Económico — Saldos por Rubrica")

    balance_sorted = balance.sort_values("SALDO_PERIODO", ascending=False)
    balance_sorted["SALDO_M"] = balance_sorted["SALDO_PERIODO"] / 1e6

    hbar = alt.Chart(balance_sorted).mark_bar(cornerRadiusBottomRight=6, cornerRadiusTopRight=6).encode(
        y=alt.Y("ASSET_TYPE:N", sort="-x", title="Rubrica"),
        x=alt.X("SALDO_M:Q", title="Saldo (M€)"),
        color=alt.Color("SALDO_M:Q", scale=alt.Scale(scheme="blues"), legend=None),
        tooltip=["ASSET_TYPE", alt.Tooltip("SALDO_M:Q", format=",.0f")]
    ).properties(height=350, title="Saldos por Rubrica (Período Actual)")
    st.altair_chart(hbar, use_container_width=True)

    st.subheader("Detalhe Completo")
    bal_display = balance[["ASSET_TYPE", "SALDO_PERIODO", "SALDO_PERIODO_ANTERIOR", "VARIACAO_ABSOLUTA"]].copy()
    bal_display["SALDO_PERIODO"] = bal_display["SALDO_PERIODO"].apply(lambda x: f"{x/1e6:,.0f} M€")
    bal_display["SALDO_PERIODO_ANTERIOR"] = bal_display["SALDO_PERIODO_ANTERIOR"].apply(lambda x: f"{x/1e6:,.0f} M€" if pd.notna(x) else "—")
    bal_display["VARIACAO_ABSOLUTA"] = bal_display["VARIACAO_ABSOLUTA"].apply(lambda x: f"{x/1e6:,.0f} M€" if pd.notna(x) else "—")
    bal_display.columns = ["Rubrica", "Saldo Actual", "Saldo Anterior", "Variação"]
    st.dataframe(bal_display, use_container_width=True, hide_index=True)

with tab4:
    st.subheader("Estado dos Reports SLV II")

    if len(report_status) > 0:
        for _, row in report_status.iterrows():
            status = row.get("STATUS", "Desconhecido")
            icon = "🟢" if status == "Fechado" else "🟡" if status == "Em Curso" else "🔴"
            col_a, col_b, col_c = st.columns([3, 1, 2])
            with col_a:
                st.markdown(f"**{row.get('REPORT_NAME', 'Report')}**")
            with col_b:
                st.markdown(f"{icon} {status}")
            with col_c:
                st.markdown(f"`{row.get('REFERENCE_DATE', '')}`")
    else:
        st.info("Nenhum report registado.")

    st.divider()
    st.markdown("### Pipeline Metadata")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown("**Fonte**")
        st.code("CAVIDA_DEMO.BRONZE.*")
    with col_m2:
        st.markdown("**Transformação**")
        st.code("dbt → SILVER (views)")
    with col_m3:
        st.markdown("**Consumo**")
        st.code("GOLD (tables) → Dashboard")

st.divider()
st.caption("CA Vida — Solvency II Analytics | Dados: CAVIDA_DEMO.GOLD | Pipeline: dbt (CAVIDA_SLV2_PROJECT) | Plataforma: Snowflake Business Critical")
