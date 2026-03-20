import streamlit as st

# Configurazione Pagina
st.set_page_config(page_title="Cerberus R&D - Professional Trader Tool", layout="wide")

# --- LOGICA RESET VALORI ---
# Inizializziamo i valori di default se non esistono
if 'last_asset' not in st.session_state:
    st.session_state.last_asset = "Indici (DAX)"
    st.session_state.entry = 22800.0
    st.session_state.sl = 22750.0
    st.session_state.tp = 22900.0

def reset_values():
    if st.session_state.asset_selection == "Indici (DAX)":
        st.session_state.entry = 22800.0
        st.session_state.sl = 22700.0
        st.session_state.tp = 23000.0
    elif st.session_state.asset_selection == "Forex (EUR/USD)":
        st.session_state.entry = 1.08500
        st.session_state.sl = 1.08000
        st.session_state.tp = 1.09500
    elif st.session_state.asset_selection == "Crypto (BTC)":
        st.session_state.entry = 65000.0
        st.session_state.sl = 64000.0
        st.session_state.tp = 68000.0

# --- SIDEBAR ---
st.sidebar.title("🛡️ Cerberus R&D")
balance = st.sidebar.number_input("Capitale Conto (€)", value=10000.0, step=1000.0)
risk_perc = st.sidebar.slider("Rischio per Operazione (%)", 0.10, 2.0, 0.25, 0.05)

# --- SELEZIONE ASSET CON CALLBACK PER RESET ---
asset = st.selectbox(
    "Seleziona Asset Class:",
    ["Indici (DAX)", "Forex (EUR/USD)", "Crypto (BTC)"],
    key="asset_selection",
    on_change=reset_values
)

st.markdown("---")

# --- INPUT DINAMICI ---
col1, col2, col3 = st.columns(3)
with col1:
    entry = st.number_input("Prezzo Entrata", value=st.session_state.entry, format="%.5f", key="entry_input")
with col2:
    sl = st.number_input("Stop Loss", value=st.session_state.sl, format="%.5f", key="sl_input")
with col3:
    tp = st.number_input("Take Profit", value=st.session_state.tp, format="%.5f", key="tp_input")

# --- CALCOLI ---
risk_euro = balance * (risk_perc / 100)
distanza_sl = abs(entry - sl)
distanza_tp = abs(tp - entry)

if distanza_sl > 0:
    # Calcolo Lotti basato sulle tue specifiche
    if "Indici" in asset:
        # 0.01 lotti = 0.10€/punto -> 1 lotto = 10€/punto
        lotti = risk_euro / (distanza_sl * 10)
    elif "Forex" in asset:
        # 1 lotto = 10€ a pip (approssimativo)
        pips = distanza_sl * 10000
        lotti = risk_euro / (pips * 10)
    else: # Crypto
        lotti = risk_euro / distanza_sl

    lotti = round(lotti, 2)
    if lotti < 0.01: lotti = 0.01
    
    rr = distanza_tp / distanza_sl
    target_euro = (distanza_tp / distanza_sl) * risk_euro

    # --- VISUALIZZAZIONE RISULTATI ---
    st.success(f"### TAGLIA POSIZIONE: **{lotti} Lotti**")
    
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Rischio €", f"-{risk_euro:.2f}€")
    res2.metric("Profitto €", f"+{target_euro:.2f}€")
    res3.metric("Rapporto R/R", f"1:{rr:.2f}")
    
    # Cos'altro puoi aggiungere? -> Calcolo del CONTROVALORE e LEVA
    notional = 0
    if "Indici" in asset: notional = lotti * entry * 1 # Esempio moltiplicatore 1
    elif "Forex" in asset: notional = lotti * 100000
    else: notional = lotti * entry
    
    res4.metric("Controvalore", f"{notional:,.0f}€")

    # Messaggio di Alert se la leva è troppo alta
    leva_effettiva = notional / balance
    if leva_effettiva > 10:
        st.warning(f"⚠️ Attenzione: Stai usando una leva effettiva di {leva_effettiva:.1f}x")
    else:
        st.info(f"Leva effettiva: {leva_effettiva:.1f}x")

else:
    st.error("Distanza Stop Loss non valida.")

st.markdown("---")
st.caption("by Cerberus R&D - Risk Management Suite v2.0")
