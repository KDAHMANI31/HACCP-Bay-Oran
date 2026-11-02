import streamlit as st
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

# Configuration
st.set_page_config(
    page_title="HACCP Inspection Platform",
    page_icon="✅",
    layout="wide"
)

st.title("🍽️ CHECK-LIST D'INSPECTION HACCP")
st.subheader("Pullman Oran")

# Session
if "inspections" not in st.session_state:
    st.session_state.inspections = []

# Sidebar
with st.sidebar:
    st.header("Informations")

    inspecteur = st.text_input(
        "Inspecteur",
        value="Khaled Dahmani"
    )

    service = st.selectbox(
        "Zone",
        [
            "Cuisine",
            "Stock",
            "Bar",
            "Réception",
            "Lavage des mains",
            "Lutte antiparasitaire",
            "Produits de nettoyage"
        ]
    )

# Checklist
checklist = {
    "Cuisine": [
        "Sols propres",
        "Plans de travail désinfectés",
        "Température chambre froide",
        "Séparation cru/cuit",
        "Étiquetage des produits",
        "Hygiène du personnel"
    ],

    "Stock": [
        "Produits hors sol",
        "FIFO respecté",
        "DLC conforme",
        "Stock propre",
        "Absence de nuisibles"
    ],

    "Bar": [
        "Machine à café propre",
        "Réfrigérateur propre",
        "Verres propres",
        "Stock organisé"
    ],

    "Réception": [
        "Salle propre",
       ],
