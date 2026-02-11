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
    </style>
    """, unsafe_allow_html=True)

st.title('Tip Calc')

# ---------------------------
# Eingaben
# ---------------------------

betrag_raw = st.text_input(
    'Rechnungsbetrag',
    placeholder='1234'
)

trinkgeld_prozent = st.slider(
    'Trinkgeld in Prozent',
    0,
    30,
    10
)

# ---------------------------
# Berechnung
# ---------------------------

betrag_clean = ''.join(ch for ch in betrag_raw.strip() if ch.isdigit())

if betrag_raw.strip() == '':
    st.info('Bitte Betrag eingeben.')

elif betrag_clean == '':
    st.error('Nur Zahlen eingeben.')

else:
    betrag = int(betrag_clean) / 100
    gesamt = betrag * (1 + trinkgeld_prozent / 100)
    gerundet = math.ceil(gesamt)

    st.divider()

    st.markdown('<p style="text-align: center; margin-top: 20px; margin-bottom: 5px; font-size: 18px;">Sage ganz lässig:</p>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="text-align: center; font-size: 72px; margin-top: 0; margin-bottom: 20px; font-weight: bold;">{gerundet} €</h1>', unsafe_allow_html=True)

    st.write(f'Rechnung: {betrag:.2f} €')
    st.write(f'Inkl. Trinkgeld ({trinkgeld_prozent}%): {gesamt:.2f} €')
