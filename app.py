import io
import pandas as pd
import streamlit as st
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

st.set_page_config(
    page_title="HACCP Inspection Platform",
    page_icon="✅",
    layout="wide"
)

st.title("🍽️ CHECK-LIST D'INSPECTION HACCP")
st.subheader("Cuisine - Stocks - Bars - Réception - Hygiène")

if "inspections" not in st.session_state:
    st.session_state.inspections = []

with st.sidebar:
    st.header("Informations")

    inspecteur = st.text_input("Inspecteur")
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

st.header("Contrôle HACCP")

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
        "Déchets évacués",
        "Surface désinfectée"
    ],
    "Lavage des mains": [
        "Savon disponible",
        "Essuie-mains disponible",
        "Eau chaude disponible"
    ],
    "Lutte antiparasitaire": [
        "Pièges présents",
        "Aucune trace de nuisibles",
        "Rapport société disponible"
    ],
    "Produits de nettoyage": [
        "Produits étiquetés",
        "Stock fermé",
        "FDS disponible"
    ]
}

conformes = 0
total = len(checklist[service])
results = []

st.markdown("### Points de contrôle")

for item in checklist[service]:
    status = st.radio(
        item,
        ["Conforme", "Non Conforme"],
        horizontal=True,
        key=item
    )

    if status == "Conforme":
        conformes += 1

    results.append({
        "Point": item,
        "Statut": status
    })

observation = st.text_area("Observations / Actions Correctives")

if st.button("Enregistrer l'inspection"):
    taux = round((conformes / total) * 100, 2)

    inspection = {
        "Date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Inspecteur": inspecteur,
        "Zone": service,
        "Conformité (%)": taux,
        "Observations": observation
    }

    st.session_state.inspections.append(inspection)
    st.success("Inspection enregistrée")

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)
    st.metric("Taux de conformité", f"{taux}%")

st.markdown("---")
st.header("Tableau de bord")

df_historique = pd.DataFrame(st.session_state.inspections)

if not df_historique.empty:
    col1, col2, col3 = st.columns(3)

    col1.metric("Nombre d'inspections", len(df_historique))

    moyenne = round(df_historique["Conformité (%)"].mean(), 2)
    col2.metric("Conformité moyenne", f"{moyenne}%")

    non_conf = len(df_historique[df_historique["Conformité (%)"] < 100])
    col3.metric("Inspections avec NC", non_conf)

    st.dataframe(df_historique, use_container_width=True)

    # ---------------------------------------------------------
    # Génération du fichier Excel structuré & stylisé
    # ---------------------------------------------------------
    buffer = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Rapport HACCP"

    # En-têtes
    headers = list(df_historique.columns)
    ws.append(headers)

    # Styles openpyxl
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=11)
    bold_font = Font(name="Calibri", size=11, bold=True)
    
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    total_border = Border(
        top=Side(style='thin', color='000000'),
        bottom=Side(style='double', color='000000')
    )

    # Style de l'en-tête
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Données
    for row_idx, row_data in enumerate(df_historique.values, start=2):
        for col_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.font = data_font
            cell.border = thin_border
            
            # Formats spécifiques par colonne
            col_name = headers[col_idx - 1]
            if col_name in ["Date", "Zone"]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_name == "Conformité (%)":
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '0.00"%"'
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    # Ligne de synthèse (Moyenne générale)
    last_row = len(df_historique) + 2
    ws.cell(row=last_row, column=1, value="Moyenne générale").font = bold_font
    ws.cell(row=last_row, column=1).border = total_border
    
    for col_idx in range(2, len(headers) + 1):
        cell = ws.cell(row=last_row, column=col_idx)
        cell.border = total_border
        if headers[col_idx - 1] == "Conformité (%)":
            cell.value = moyenne
            cell.font = bold_font
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '0.00"%"'

    # Ajustement automatique de la largeur des colonnes
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 5, 14)

    wb.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="📥 Télécharger le rapport Excel (Formaté)",
        data=buffer,
        file_name=f"Rapport_HACCP_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Aucune inspection enregistrée.")
