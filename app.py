import streamlit as st

# Configurazione Pagina
st.set_page_config(page_title="Cerberus R&D - Risk Calculator", layout="centered")

st.title("📊 Calcolatore Lotti Cerberus R&D")
st.markdown("---")

# Input Principali
balance = st.number_input("Capitale del Conto ($)", min_value=0.0, value=10000.0, step=100.0)
risk_percent = st.number_input("Percentuale di Rischio (%)", min_value=0.01, max_value=100.0, value=0.25, step=0.05)

# Selezione Strumento
asset_type = st.radio("Tipo di Strumento", ["Valute (Forex)", "Indici (es. DAX)"])

col1, col2 = st.columns(2)

with col1:
    entry_price = st.number_input("Prezzo di Entrata", min_value=0.0, value=1.00000, format="%.5f")
with col2:
    stop_loss = st.number_input("Prezzo di Stop Loss", min_value=0.0, value=0.99900, format="%.5f")

# Calcolo della dimensione della posizione
risk_amount = balance * (risk_percent / 100)
distanza_prezzo = abs(entry_price - stop_loss)

if distanza_prezzo > 0:
    if asset_type == "Valute (Forex)":
        # Calcolo standard: 1 lotto = 10$ a pip (per coppie con USD al secondo posto)
        # Pip = 0.0001
        pips = distanza_prezzo * 10000
        lotti = risk_amount / (pips * 10) if pips > 0 else 0
    else:
        # Calcolo Indici (es. DAX): 1 punto = valore del contratto (es. 1€ o 25€)
        # Qui impostiamo 1 lotto = 1 punto = 1 unità di valuta per semplicità
        lotti = risk_amount / distanza_prezzo
    
    st.success(f"### Risultato: {lotti:.2f} Lotti")
    
    # Tabella di Riepilogo
    st.table({
        "Parametro": ["Rischio Monetario", "Distanza (Pips/Punti)", "Taglia Posizione"],
        "Valore": [f"{risk_amount:.2f} $", f"{distanza_prezzo:.5f}", f"{lotti:.2f} Lotti"]
    })
else:
    st.warning("Lo Stop Loss non può essere uguale al Prezzo di Entrata.")

st.markdown("---")
st.caption("by Cerberus R&D")
