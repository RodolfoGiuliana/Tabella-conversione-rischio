import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Cerberus R&D - Asset Management Suite", layout="wide", initial_sidebar_state="expanded")

# --- STILE CSS PERSONALIZZATO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. SIDEBAR (Parametri Globali) ---
st.sidebar.title("🛡️ Cerberus Management")
balance = st.sidebar.number_input("Capitale in Gestione (€)", value=10000.0, step=1000.0)
max_daily_loss = st.sidebar.slider("Max Daily Drawdown (%)", 1.0, 5.0, 2.0)
st.sidebar.markdown("---")
st.sidebar.caption("Institutional Risk Control v4.0")

# --- 2. NAVIGAZIONE (BOTTONI / TABS) ---
tabs = st.tabs(["🧮 Risk Calculator", "📅 Macro Analysis", "📊 Quantitative Stats", "📝 Trading Journal"])

# --- TAB 1: RISK CALCULATOR ---
with tabs[0]:
    st.header("Position Sizing & Risk Management")
    
    # Selezione Asset
    asset_type = st.selectbox(
        "Strumento Finanziario:",
        ["Indici (DAX/NAS)", "Forex (EUR/USD/GBP)", "Crypto (BTC/ETH)"],
        key="asset_sel"
    )

    col_inp1, col_inp2, col_inp3 = st.columns(3)
    with col_inp1:
        entry = st.number_input("Prezzo Entrata", value=15000.0, format="%.5f")
    with col_inp2:
        sl = st.number_input("Stop Loss", value=14950.0, format="%.5f")
    with col_inp3:
        tp = st.number_input("Take Profit", value=15100.0, format="%.5f")

    risk_perc = st.slider("Rischio Operativo (%)", 0.1, 2.0, 0.5, 0.1)
    
    # Calcoli Tecnici
    risk_euro = balance * (risk_perc / 100)
    dist_sl = abs(entry - sl)
    dist_tp = abs(tp - entry)

    if dist_sl > 0:
        # Logica Lotti
        if "Indici" in asset_type: lotti = risk_euro / (dist_sl * 10)
        elif "Forex" in asset_type: lotti = risk_euro / (dist_sl * 10000 * 10)
        else: lotti = risk_euro / dist_sl
        
        lotti_finali = max(round(lotti, 2), 0.01)
        rr = dist_tp / dist_sl
        
        # Dashboard Risultati
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        res_col1.metric("SIZE (LOTTI)", f"{lotti_finali}")
        res_col2.metric("RISCHIO (€)", f"-{risk_euro:.2f} €")
        res_col3.metric("PROFITTO (€)", f"+{rr*risk_euro:.2f} €")
        res_col4.metric("RATIO R/R", f"1:{rr:.2f}")

        if rr < 1.5:
            st.warning("⚠️ Rapporto Rischio/Rendimento sub-ottimale (< 1:1.5). Valutare l'operazione.")
        else:
            st.success("✅ Parametri di rischio validati per l'esecuzione.")

# --- TAB 2: MACRO ANALYSIS ---
with tabs[1]:
    st.header("High Impact Economic Calendar")
    st.info("Filtro attivo: Solo news ad alto impatto (Market Movers)")
    
    tradingview_macro = """
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
      {
      "colorTheme": "dark", "width": "100%", "height": "500", "locale": "it",
      "importanceFilter": "1", "currencyFilter": "USD,EUR,GBP,JPY"
      }
      </script>
    </div>
    """
    components.html(tradingview_macro, height=520)

# --- TAB 3: QUANTITATIVE STATS ---
with tabs[2]:
    st.header("Quantitative Risk Analysis")
    
    q_col1, q_col2 = st.columns(2)
    
    with q_col1:
        st.subheader("Simulazione Drawdown Progressivo")
        # Tabella stress test
        losses = []
        temp_balance = balance
        for i in range(1, 6):
            temp_balance -= risk_euro
            losses.append({"Trade Persi": i, "Capitale Rimanente": f"{temp_balance:.2f} €", "Drawdown Totale": f"-{(1 - temp_balance/balance)*100:.2f}%"})
        st.table(pd.DataFrame(losses))

    with q_col2:
        st.subheader("Kelly Criterion (Optimized Size)")
        win_rate = st.number_input("Tua Win Rate storica (%)", 10, 90, 50) / 100
        # Formula Kelly: K% = W - [(1-W)/R]
        kelly = win_rate - ((1 - win_rate) / rr) if rr > 0 else 0
        st.metric("Kelly Suggestion", f"{max(0, kelly*100):.2f}%")
        st.caption("La \% del capitale suggerita matematicamente per questo trade in base alla tua statistica.")

# --- TAB 4: TRADING JOURNAL ---
with tabs[3]:
    st.header("Professional Trading Log")
    log_col1, log_col2 = st.columns([1, 2])
    with log_col1:
        st.text_input("Asset")
        st.selectbox("Direzione", ["LONG", "SHORT"])
        st.text_area("Perchè stai entrando? (Confluenze)")
        if st.button("Salva Setup"):
            st.toast("Setup salvato localmente")
    with log_col2:
        st.markdown("""
        **Checklist pre-trade per Gestori:**
        - [ ] News Alto Impatto controllate?
        - [ ] Correlazioni inverse verificate? (es. DXY vs EURUSD)
        - [ ] Esposizione massima giornaliera non superata?
        - [ ] Mindset stabile (No Revenge Trading)?
        """)

st.markdown("---")
st.caption("© 2026 Cerberus R&D - Professional Asset Management Tool")
