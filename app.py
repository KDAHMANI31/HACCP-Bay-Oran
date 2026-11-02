import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration
st.set_page_config(
    page_title="HACCP Pullman Oran",
    page_icon="✅",
    layout="wide"
)

# Session
if "historique" not in st.session_state:
    st.session_state.historique = []

# Titre
st.title("✅ CHECK-LIST D'INSPECTION HACCP")
st.subheader("Pullman Oran")

# Menu latéral
with st.sidebar:
    st.header("Informations")

    inspecteur = st.text_input(
        "Inspecteur",
        "Khaled Dahmani"
    )

    zone = st.selectbox(
        "Zone inspectée",
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

# Checklists
checklists = {
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
        "Absence de nuisibles",
        "Rapport prestataire disponible"
    ],

    "Produits de nettoyage": [
        "Produits étiquetés",
        "Stock fermé",
        "FDS disponible"
    ]
}

st.header(f"Inspection : {zone}")

conformes = 0
total = len(checklists[zone])

for point in checklistsstatut = st.radio(
        point,
        ["Conforme", "Non Conforme"],
        horizontal=True,
        key=point
    )

    if statut == "Conforme":
        conformes += 1

observation = st.text_area(
    "Observations / Actions Correctives"
)

if st.button("Enregistrer Inspection"):

    taux = round((conformes / total) * 100, 2)

    st.session_state.historique.append(
        {
            "Date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Inspecteur": inspecteur,
            "Zone": zone,
            "Conformité (%)": taux,
            "Observation": observation
        }
    )

    st.success("Inspection enregistrée")

# Historique
st.divider()

st.header("Tableau de Bord")

if len(st.session_state.historique) > 0:

    df = pd.DataFrame(
        st.session_state.historique
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Nombre d'inspections",
        len(df)
    )

    col2.metric(
        "Taux moyen",
        f"{round(df['Conformité (%)'].mean(),2)}%"
    )

    col3.metric(
        "Non-conformités",
        len(df[df["Conformité (%)"] < 100])
    )

    def colorer(val):
        if val >= 90:
            return "background-color: #92D050"
        elif val >= 70:
            return "background-color: #FFD966"
        else:
            return "background-color: #FF6666"

    st.dataframe(
        df.style.map(
            colorer,
            subset=["Conformité (%)"]
        ),
        use_container_width=True
    )

    fichier = "Rapport_HACCP.xlsx"

    with pd.ExcelWriter(
        fichier,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Audit HACCP"
        )

    with open(fichier, "rb") as f:

        st.download_button(
            "📥 Télécharger le rapport Excel",
            f,
            file_name=fichier
        )

else:

    st.info("Aucune inspection enregistrée.")
