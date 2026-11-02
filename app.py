import streamlit as st
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# -------------------------
# CONFIGURATION PAGE
# -------------------------
st.set_page_config(
    page_title="HACCP Inspection Platform",
    page_icon="✅",
    layout="wide"
)

# -------------------------
# TITRE
# -------------------------
st.title("🍽️ CHECK-LIST D'INSPECTION HACCP")
st.subheader("Cuisine - Stocks - Bars - Réception - Hygiène")

# -------------------------
# SESSION
# -------------------------
if "inspections" not in st.session_state:
    st.session_state.inspections = []

# -------------------------
# MENU LATERAL
# -------------------------
with st.sidebar:

    st.header("Informations Inspection")

    inspecteur = st.text_input(
        "Nom Inspecteur",
        value="Khaled Dahmani"
    )

    service = st.selectbox(
        "Zone Auditée",
        [
            "Cuisine",
            "Stock",
            "Bar",
            "Réception",
            "Lavage des mains",
          
