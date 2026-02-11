import streamlit as st
import math

st.set_page_config(
    page_title='Trip Calc',
    layout='centered'
)

# CSS für größere Eingabefelder und zentrierte Ausgabe
st.markdown("""
    <style>
    /* Eingabefeld höher machen */
    input[type="text"] {
        font-size: 28px !important;
        height: 100px !important;
        padding: 0 20px !important;
        line-height: 100px !important;
        border: 2px solid #ccc !important;
        border-radius: 8px !important;
        text-align: center !important;
        box-sizing: border-box !important;
    }
    /* Container um das Eingabefeld */
    div[data-baseweb="input"] {
        height: 100px !important;
    }
    /* Kompaktere Abstände für mobile Ansicht */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    /* Reduzierte Abstände um Divider */
    hr {
        margin-top: 0.2rem !important;
        margin-bottom: 0.2rem !important;
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




# CSS für grünen, zentrierten Button
st.markdown("""
    <style>
    div[data-testid="stButton"] {
        display: flex;
        justify-content: center;
        margin-top: 0 !important;
    }
    div[data-testid="stButton"] > button {
        width: 50% !important;
        background-color: #28a745 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 15px !important;
        border: none !important;
        border-radius: 8px !important;
        margin-top: 0px !important;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #218838 !important;
    }
    </style>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button('Reset', use_container_width=True):
        # Reset durch Erhöhen des Counters - generiert neue Widget-Keys
        st.session_state.reset_counter += 1
        st.rerun()
