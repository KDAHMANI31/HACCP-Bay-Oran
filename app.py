import streamlit as st
import pandas as pd
from datetime import datetime

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="HACCP Pullman Oran",
    page_icon="✅",
    layout="wide"
)

# --------------------------------------------------
# SESSION
# --------------------------------------------------
if "historique" not in st.session_state:
    st.session_state.historique = []

# --------------------------------------------------
# TITRE
# --------------------------------------------------
st.title("✅ CHECK-LIST D'INSPECTION HACCP")
st.subheader("Pullman Oran")

# --------------------------------------------------
# MENU LATERAL
# --------------------------------------------------
with st.sidebar:

    st.header("Informations")

    inspecteur = st.text_input(
        "Inspecteur",
        "Khaled Dahmani"
    )

    zone = st.select
