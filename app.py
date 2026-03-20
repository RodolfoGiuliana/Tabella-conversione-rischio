import streamlit as st

# Configurazione Pagina
st.set_page_config(page_title="Cerberus R&D - Multi-Asset Calculator", layout="centered")

st.title("📊 Multi-Asset Risk Calculator")
st.subheader("By Cerberus R&D")
st.markdown("---")

# --- SEZIONE 1: IMPOSTAZIONI ACCOUNT ---
st.sidebar.header("Impostazioni Account")
balance = st.sidebar.number_input("Capitale del Conto (€)", min_value=0.0, value=10000.0, step=100.0)
risk_percent = st.sidebar.slider("Rischio per Operazione (%)", 0.10, 5.0, 0.25, 0.05)

# --- SEZIONE 2: SELEZIONE ASSET ---
asset_class = st.selectbox(
    "Seleziona lo strumento:",
    ["Indici (DAX, NASDAQ, ecc.)", "Forex (EURUSD, GBPUSD, ecc.)", "Crypto (BTC, ETH, ecc.)"]
)

st.markdown(f"### Parametri {asset_class}")

col1, col2, col3 = st.columns(3)
with col1:
    entry = st.number_input("Prezzo Entrata", min_value=0.0, value=24500.0, format="%.5f")
with col2:
    sl = st.number_input("Stop Loss", min_value=0.0, value=24000.0, format="%.5f")
with col3:
    tp = st.number_input("Take Profit", min_value=0.0, value=25000.0, format="%.5f")

# --- LOGICA DI CALCOLO ---
risk_euros = balance * (risk_percent / 100)
distanza_sl = abs(entry - sl)
distanza_tp = abs(tp - entry)

if distanza_sl > 0:
    if asset_class == "Indici (DAX, NASDAQ, ecc.)":
        # Tua specifica: 0.01 lotti = 0.10€ a punto -> 1 lotto = 10€/punto
        valore_per_unita = 10.0
        lotti = risk_euros / (distanza_sl * valore_per_unita)
        
    elif asset_class == "Forex (EURUSD, GBPUSD, ecc.)":
        # Calcolo Standard Forex: 1 lotto (100k) = 10$ (circa 9.20€) a pip
        # 1 pip = 0.0001 (per la maggior parte delle coppie)
        pips = distanza_sl * 10000
        # Assumendo valore pip standard di circa 10€ per 1 lotto intero
        lotti = risk_euros / (pips * 10)
        
    else:  # Crypto
        # Nelle Crypto (es. BTC) 1 lotto = 1 intero asset. 
        # Il rischio è semplicemente la differenza di prezzo.
        lotti = risk_euros / distanza_sl

    # Arrotondamento per il broker (solitamente 2 decimali)
    lotti_finali = round(lotti, 2)
    if lotti_finali < 0.01: lotti_finali = 0.01

    # Calcolo Risultati monetari
    profitto_tp = (distanza_tp / distanza_sl) * risk_euros if distanza_sl > 0 else 0
    rr = distanza_tp / distanza_sl if distanza_sl > 0 else 0

    # --- OUTPUT VISIVO ---
    st.markdown("---")
    st.success(f"## TAGLIA CONSIGLIATA: **{lotti_finali} Lotti**")

    res1, res2, res3 = st.columns(3)
    res1.metric("Rischio (€)", f"-{risk_euros:.2f} €")
    res2.metric("Target (€)", f"+{profitto_tp:.2f} €")
    res3.metric("Rapporto R/R", f"1:{rr:.2f}")

    # Tabella di riepilogo tecnica
    st.table({
        "Asset": [asset_class],
        "Distanza SL": [f"{distanza_sl:.5f}"],
        "Valore punto/pip stimato": ["Standard Broker"]
    })

else:
    st.error("Lo Stop Loss non può essere uguale all'entrata.")

st.markdown("---")
st.caption("© By Cerberus R&D - Proprietary Trading Tools")
