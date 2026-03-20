import streamlit as st

# Configurazione Pagina
st.set_page_config(page_title="Cerberus R&D - Professional Suite", layout="wide")

# --- 1. INIZIALIZZAZIONE STATO ---
if 'entry' not in st.session_state:
    st.session_state.entry = 22800.0
    st.session_state.sl = 22700.0
    st.session_state.tp = 23000.0

# --- 2. FUNZIONE DI RESET ---
def reset_inputs():
    asset = st.session_state.asset_selection
    if asset == "Indici (DAX)":
        st.session_state.entry = 22800.0
        st.session_state.sl = 22700.0
        st.session_state.tp = 23000.0
    elif asset == "Forex (EUR/USD)":
        st.session_state.entry = 1.08500
        st.session_state.sl = 1.08000
        st.session_state.tp = 1.09500
    elif asset == "Crypto (BTC)":
        st.session_state.entry = 65000.0
        st.session_state.sl = 64000.0
        st.session_state.tp = 67000.0

# --- 3. SIDEBAR ---
st.sidebar.title("🛡️ Cerberus R&D")
balance = st.sidebar.number_input("Capitale Conto (€)", value=10000.0, step=500.0)
risk_perc = st.sidebar.slider("Rischio per Operazione (%)", 0.10, 2.0, 0.25, 0.05)

# --- 4. SELEZIONE ASSET ---
# Il trigger 'on_change' chiama la funzione reset_inputs
st.selectbox(
    "Seleziona lo strumento:",
    ["Indici (DAX)", "Forex (EUR/USD)", "Crypto (BTC)"],
    key="asset_selection",
    on_change=reset_inputs
)

st.markdown("---")

# --- 5. INPUT DINAMICI ---
# valori dello state. Se l'utente scrive, lo state si aggiorna.
col1, col2, col3 = st.columns(3)
with col1:
    entry = st.number_input("Entrata", value=st.session_state.entry, format="%.5f")
    st.session_state.entry = entry
with col2:
    sl = st.number_input("Stop Loss", value=st.session_state.sl, format="%.5f")
    st.session_state.sl = sl
with col3:
    tp = st.number_input("Take Profit", value=st.session_state.tp, format="%.5f")
    st.session_state.tp = tp

# --- 6. CALCOLI ---
risk_euro = balance * (risk_perc / 100)
dist_sl = abs(entry - sl)
dist_tp = abs(tp - entry)

if dist_sl > 0:
    # Logica Lotti Cerberus
    if "Indici" in st.session_state.asset_selection:
        # 1 lotto = 10€/punto (quindi 0.01 = 0.10€)
        lotti = risk_euro / (dist_sl * 10)
    elif "Forex" in st.session_state.asset_selection:
        pips = dist_sl * 10000
        lotti = risk_euro / (pips * 10)
    else: # Crypto
        lotti = risk_euro / dist_sl

    lotti_finali = max(round(lotti, 2), 0.01)
    rr = dist_tp / dist_sl
    potenziale_profit = rr * risk_euro

    # --- OUTPUT RISULTATI ---
    st.success(f"### TAGLIA POSIZIONE: **{lotti_finali} Lotti**")
    
    res1, res2, res3 = st.columns(3)
    res1.metric("Rischio (€)", f"-{risk_euro:.2f} €")
    res2.metric("Target (€)", f"+{potenziale_profit:.2f} €")
    res3.metric("Rapporto R/R", f"1:{rr:.2f}")

    st.markdown("---")

    # --- 7. TABELLA MONEY MANAGEMENT DINAMICA ---
    st.subheader(" Piano di Crescita Mensile (Target 3%)")
    st.write(f"Con un rischio dello **{risk_perc}%**, ecco come gestire il tuo capitale di **{balance:.2f}€**:")

    # Calcoli per la tabella basati sul rischio selezionato
    win_RR2 = risk_euro * 2 # Profitto per singola operazione con RR 1:2
    target_3_percent = balance * 0.03
    op_necessarie = round(target_3_percent / win_RR2, 1) if win_RR2 > 0 else 0

    mm_data = [
        {"Parametro": "Rischio per Trade (€)", "Valore": f"{risk_euro:.2f} €"},
        {"Parametro": "Profitto Target (3% Mese)", "Valore": f"{target_3_percent:.2f} €"},
        {"Parametro": "Trade vinti necessari (RR 1:2)", "Valore": f"{op_necessarie}"},
        {"Parametro": "Perdita Massima Giornaliera (4 trade)", "Valore": f"{(risk_euro * 4):.2f} €"}
    ]
    
    st.table(mm_data)

else:
    st.error("Inserisci valori di prezzo validi per calcolare i lotti.")

st.caption("by Cerberus R&D - Risk Tool v2.1")
