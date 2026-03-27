import streamlit as st
import requests
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="Cerberus R&D - Professional Suite", layout="wide")

# --- 0. CONFIGURAZIONE API NEWS ---
# Ti consiglio di mettere la tua API Key nei "Secrets" di Railway/Github per sicurezza
API_KEY = "LA_TUA_API_KEY_QUI" 
NEWS_URL = "https://www.jblanked.com/news/api/list/"

def get_economic_news():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}",
    }
    try:
        response = requests.get(NEWS_URL, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Errore nel recupero news: {e}")
        return None

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
st.selectbox(
    "Seleziona lo strumento:",
    ["Indici (DAX)", "Forex (EUR/USD)", "Crypto (BTC)"],
    key="asset_selection",
    on_change=reset_inputs
)

st.markdown("---")

# --- 5. NEWS ECONOMICHE (Nuova Sezione) ---
with st.expander("📅 Calendario Economico & News del Giorno", expanded=False):
    news_data = get_economic_news()
    if news_data:
        # Convertiamo in DataFrame per una visualizzazione migliore
        df_news = pd.DataFrame(news_data)
        
        # Selezioniamo solo le colonne interessanti se esistono (es: Time, Name, Impact, Currency)
        # Nota: i nomi delle colonne dipendono dall'esatta risposta dell'API JBlanked
        st.dataframe(df_news, use_container_width=True)
    else:
        st.warning("Impossibile caricare le news. Controlla la tua API Key o il limite di richieste.")

# --- 6. INPUT DINAMICI ---
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

# --- 7. CALCOLI ---
risk_euro = balance * (risk_perc / 100)
dist_sl = abs(entry - sl)
dist_tp = abs(tp - entry)

if dist_sl > 0:
    if "Indici" in st.session_state.asset_selection:
        lotti = risk_euro / (dist_sl * 10)
    elif "Forex" in st.session_state.asset_selection:
        pips = dist_sl * 10000
        lotti = risk_euro / (pips * 10)
    else: # Crypto
        lotti = risk_euro / dist_sl

    lotti_finali = max(round(lotti, 2), 0.01)
    rr = dist_tp / dist_sl
    potenziale_profit = rr * risk_euro

    st.success(f"### TAGLIA POSIZIONE: **{lotti_finali} Lotti**")
    
    res1, res2, res3 = st.columns(3)
    res1.metric("Rischio (€)", f"-{risk_euro:.2f} €")
    res2.metric("Target (€)", f"+{potenziale_profit:.2f} €")
    res3.metric("Rapporto R/R", f"1:{rr:.2f}")

    st.markdown("---")

    # --- 8. TABELLA MONEY MANAGEMENT ---
    st.subheader("📈 Piano di Crescita Mensile (Target 3%)")
    win_RR2 = risk_euro * 2
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

st.markdown("---")
st.subheader("⚡ Scalping Mode (Solo Punti)")
punti_sl_rapido = st.number_input("Distanza Stop Loss (Punti)", value=20)
lotti_scalp = risk_euro / (punti_sl_rapido * 10)
st.info(f"Per uno stop di {punti_sl_rapido} punti, usa **{lotti_scalp:.2f}** lotti.")

st.caption("by Cerberus R&D - Risk Tool v2.1")
