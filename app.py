import streamlit as st

# Configurazione Pagina
st.set_config = st.set_page_config(page_title="Cerberus R&D - Risk Calculator", layout="centered")

st.title("📊 Calcolatore Lotti Cerberus R&D")
st.subheader("Modulo Scalping/Trading Professionale")
st.markdown("---")

# --- INPUT UTENTE ---
col_acc1, col_acc2 = st.columns(2)
with col_acc1:
    balance = st.number_input("Capitale del Conto (€)", min_value=0.0, value=10000.0, step=100.0)
with col_acc2:
    risk_percent = st.number_input("Percentuale di Rischio (%)", min_value=0.01, max_value=10.0, value=0.25, step=0.05, format="%.2f")

st.markdown("### Parametri Operazione (DAX / Indici)")
col1, col2, col3 = st.columns(3)

with col1:
    entry_price = st.number_input("Entrata", min_value=0.0, value=24500.0, step=1.0)
with col2:
    stop_loss = st.number_input("Stop Loss", min_value=0.0, value=24000.0, step=1.0)
with col3:
    take_profit = st.number_input("Take Profit", min_value=0.0, value=25000.0, step=1.0)

# --- LOGICA DI CALCOLO ---

# 1. Calcolo del rischio monetario
risk_amount = balance * (risk_percent / 100)

# 2. Calcolo distanza punti
punti_stop = abs(entry_price - stop_loss)
punti_target = abs(take_profit - entry_price)

# 3. Calcolo Lotti
# Logica richiesta: 0.01 lotti = 0.10€ a punto.
# Quindi 1 lotto intero (1.00) = 10€ a punto.
# Formula: Rischio (€) / Punti / Valore per punto di 1 lotto
if punti_stop > 0:
    valore_punto_lotto_standard = 10.0  # 1.00 lotto = 10€/punto
    lotti = risk_amount / (punti_stop * valore_punto_lotto_standard)
    
    # Arrotondamento a 2 decimali (step minimo 0.01)
    lotti = round(lotti, 2)
    if lotti < 0.01: lotti = 0.01

    # Calcolo Profitto Potenziale
    profit_potenziale = lotti * punti_target * valore_punto_lotto_standard

    # --- OUTPUT ---
    st.markdown("---")
    st.success(f"### TAGLIA POSIZIONE: **{lotti} Lotti**")

    c1, c2, c3 = st.columns(3)
    c1.metric("Rischio (€)", f"-{risk_amount:.2f} €")
    c2.metric("Profitto Target (€)", f"+{profit_potenziale:.2f} €")
    c3.metric("Rapporto R/R", f"1:{(punti_target/punti_stop):.2f}")

    st.info(f"💡 Con **{lotti}** lotti, ogni punto di movimento vale **{(lotti * 10):.2f} €**")

else:
    st.error("Lo Stop Loss deve essere diverso dal prezzo di entrata.")

st.markdown("---")
st.caption("© By Cerberus R&D - Proprietary Trading Tools")
