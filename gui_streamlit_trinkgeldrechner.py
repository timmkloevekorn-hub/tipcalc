import streamlit as st
import math

st.set_page_config(
    page_title='Trip Calc',
    layout='centered'
)

st.markdown("""
<style>

/* ========================================
   APP-HINTERGRUND: #F2F2F7
   ======================================== */
body {
    background-color: #F2F2F7;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 1rem;
    background-color: #F2F2F7;
}

/* ========================================
   CARD-HINTERGRUND: #FFFFFF
   ======================================== */
div[data-baseweb="input"] {
    min-height: 120px !important;
}

/* Inneres Input-Feld */
div[data-baseweb="input"] input {
    background-color: #FFFFFF !important;
    font-size: 30px !important;
    padding: 35px 20px !important;
    text-align: center !important;
    border-radius: 12px !important;
    border: 1.5px solid #D1D1D6 !important;
    color: #1C1C1E !important;
}

/* ========================================
   SLIDER - Styling wird über .streamlit/config.toml
   gesteuert (primaryColor = #007AFF)
   ======================================== */

/* Thumb-Design */
div[data-baseweb="slider"] div[role="slider"] {
    border: 3px solid #FFFFFF !important;
    box-shadow: 0 2px 8px rgba(0, 122, 255, 0.3) !important;
}

/* ========================================
   RESET-BUTTON
   HINTERGRUND: #E5E5EA
   HOVER: #D1D1D6
   TEXT: #1C1C1E
   ======================================== */
div[data-testid="stButton"] {
    display: flex !important;
    justify-content: center !important;
    margin-top: 0 !important;
}

div[data-testid="stButton"] > button {
    width: 50% !important;
    background-color: #E5E5EA !important;
    color: #1C1C1E !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 14px !important;
    transition: background-color 0.2s ease !important;
}

div[data-testid="stButton"] > button:hover {
    background-color: #D1D1D6 !important;
}

/* ========================================
   PRIMÄRER TEXT: #1C1C1E
   ======================================== */
h1, h2, h3 {
    color: #1C1C1E !important;
}

/* ========================================
   SEKUNDÄRER TEXT: #6E6E73
   ======================================== */
label {
    color: #6E6E73 !important;
    font-size: 14px !important;
}

p {
    color: #1C1C1E !important;
}

/* Kleinere Texte und Beschreibungen */
.stMarkdown p small {
    color: #6E6E73 !important;
}

/* ========================================
   SONSTIGES
   ======================================== */
hr {
    margin-top: 0.3rem !important;
    margin-bottom: 0.3rem !important;
    border-color: #D1D1D6 !important;
}

</style>
""", unsafe_allow_html=True)



st.title('Tip Calc')

# ---------------------------
# Eingaben
# ---------------------------

# Session State für Reset-Funktion initialisieren
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

# Hilfsfunktion: Formatiert Ziffern mit Komma (z.B. "1234" -> "12,34")
def format_betrag(ziffern):
    if len(ziffern) == 0:
        return ''
    elif len(ziffern) == 1:
        return f'0,0{ziffern}'
    elif len(ziffern) == 2:
        return f'0,{ziffern}'
    else:
        euros = ziffern[:-2]
        cents = ziffern[-2:]
        return f'{euros},{cents}'

# Callback Funktion für das Eingabefeld
def on_betrag_change():
    raw = st.session_state[f'betrag_{st.session_state.reset_counter}']
    digits = ''.join(ch for ch in raw if ch.isdigit())
    formatted = format_betrag(digits)
    if formatted and formatted != raw:
        st.session_state[f'betrag_{st.session_state.reset_counter}'] = formatted

betrag_raw = st.text_input(
    'Rechnungsbetrag',
    key=f'betrag_{st.session_state.reset_counter}',
    on_change=on_betrag_change,
    placeholder='hier Betrag eingeben'
)

# Nur Ziffern extrahieren
betrag_clean = ''.join(ch for ch in betrag_raw.strip() if ch.isdigit())

trinkgeld_prozent = st.slider(
    'Trinkgeld in Prozent',
    0,
    30,
    10,
    key=f'slider_{st.session_state.reset_counter}'
)

# ---------------------------
# Berechnung
# ---------------------------

if betrag_clean:
    betrag = int(betrag_clean) / 100
    gesamt = betrag * (1 + trinkgeld_prozent / 100)
    gerundet = math.ceil(gesamt)

   

    st.markdown('<p style="text-align: center; margin-top: 10px; margin-bottom: 0px; font-size: 18px;">Sage ganz lässig:</p>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="text-align: center; font-size: 72px; margin-top: 0; margin-bottom: 7px; font-weight: bold;">{gerundet} €</h1>', unsafe_allow_html=True)

    st.write(f'Rechnung: {betrag:.2f} €')
    st.write(f'Inkl. Trinkgeld ({trinkgeld_prozent}%): {gesamt:.2f} €')

# ---------------------------
# Clear Button
# ---------------------------

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button('Reset', use_container_width=True):
        # Reset durch Erhöhen des Counters - generiert neue Widget-Keys
        st.session_state.reset_counter += 1
        st.rerun()
