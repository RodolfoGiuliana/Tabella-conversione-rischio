import streamlit as st

# Configurazione Pagina
st.set_page_config(page_title="Cerberus R&D - Risk Suite", layout="wide")

# --- INIZIALIZZAZIONE SESSION STATE ---
# Questo serve a gestire i valori predefiniti per ogni asset
if 'asset_prev' not in st.session_state:
    st.session_state.asset_prev = "Indici (DAX)"
    st.session_state.entry = 22800.0
    st.session_state.sl = 22700.0
    st.session_state.tp = 23000.0

# --- FUNZIONE DI RESET AUTOMATICO ---
def handle_change():
    asset = st.session_state.asset_selection
    if asset == "Indici (DAX)":
        st.session_state.entry = 22800.0
        st.session_state.sl = 22700.0
        st.session_state.tp = 23000.0
    elif asset == "Forex (EUR/USD)":
        st.session_state.entry = 1.08500
        st.session_state.sl = 1.08000
        st.session_state.tp = 1.10000
    elif asset == "Crypto (BTC)":
        st.session_state.entry = 65000.0
        st.session_state.sl = 64000.0
        st.session_state.tp = 68000.0

# --- SIDEBAR ---
st.sidebar.title("🛡️ Cerberus R&D")
balance = st.sidebar.number_input("Capitale Conto (€)", value=10000.0, step=1000.0)
risk_perc = st.sidebar.select_slider("Rischio per Operazione (%)", options=[0.10, 0.25, 0.50, 0.75, 1.0], value=0.25)

# --- SELEZIONE ASSET ---
asset = st.selectbox(
    "Seleziona Asset Class:",
    ["Indici (DAX)", "Forex (EUR/USD)", "Crypto (BTC)"],
    key="asset_selection",
    on_change=handle_change
)

st.markdown("---")

# --- INPUT DINAMICI (Usano il Session State aggiornato) ---
col1, col2, col3 = st.columns(3)
with col1:
    entry = st.number_input("Prezzo Entrata", value=st.session_state.entry, format="%.5f", key="e_input")
with col2:
    sl = st.number_input("Stop Loss", value=st.session_state.sl, format="%.5f", key="s_input")
with col3:
    tp = st.number_input("Take Profit", value=st.session_state.tp, format="%.5f", key="t_input")

# --- CALCOLI TECNICI ---
risk_euro = balance * (risk_perc / 100)
dist_sl = abs(entry - sl)
dist_tp = abs(tp - entry)

if dist_sl > 0:
    # Calcolo Lotti
    if "Indici" in asset:
        lotti = risk_euro / (dist_sl * 10) # 0.01 lot = 0.10€/punto -> 1 lot = 10€/punto
    elif "Forex" in asset:
        pips = dist_sl * 10000
        lotti = risk_euro / (pips * 10)
    else: # Crypto
        lotti = risk_euro / dist_sl

    lotti = max(round(lotti, 2), 0.01)
    rr = dist_tp / dist_sl
    target_euro = rr * risk_euro

    # Visualizzazione Output Principale
    st.success(f"### TAGLIA POSIZIONE: **{lotti} Lotti**")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Rischio Operazione", f"-{risk_euro:.2f} €")
    c2.metric("Profitto Potenziale", f"+{target_euro:.2f} €")
    c3.metric("Rapporto R/R", f"1:{rr:.2f}")

st.markdown("---")

# --- TABELLA MONEY MANAGEMENT (Cerberus R&D Strategy) ---
st.header("📈 Cerberus R&D: Piano per Obiettivo 2-3% Mese")
st.write("Per fare il 3% mese rischiando solo lo 0.25% a operazione, ecco la tabella di marcia:")

data_table = [
    {"Frequenza": "Settimanale", "Profitto Target (%)": "0.75%", "Profitto Target (€)": f"{balance * 0.0075:.2f}€", "Operazioni Vinte (R/R 1:2)": "1.5"},
    {"Frequenza": "Mensile", "Profitto Target (%)": "3.00%", "Profitto Target (€)": f"{balance * 0.03:.2f}€", "Operazioni Vinte (R/R 1:2)": "6"},
    {"Frequenza": "Annuale", "Profitto Target (%)": "36.00%", "Profitto Target (€)": f"{balance * 0.36:.2f}€", "Note": "Senza Interesse Composto"}
]

st.table(data_table)

with st.expander("📌 Regole d'oro per il Rischio Bassissimo"):
    st.markdown(f"""
    1. **Rischio costante:** Non aumentare il rischio dopo una perdita. Mantieni lo **{risk_perc}%**.
    2. **Il potere del RR:** Con un Rapporto Rischio/Rendimento di 1:2, ti basta vincere il 35% delle volte per essere in profitto.
    3. **Stop al Trading:** Se perdi il 1% in un giorno (4 operazioni da 0.25%), chiudi i grafici.
    4. **Focus:** Per fare il 3% mese servono solo **6 operazioni in profitto** (con RR 1:2) in 20 giorni di borsa aperta.
    """)

st.caption("by Cerberus R&D - La disciplina batte il talento.")
