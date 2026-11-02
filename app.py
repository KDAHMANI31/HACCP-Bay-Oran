import streamlit as st
import pandas as pd
from datetime import datetime

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

observation = st.text_area(
    "Observations / Actions Correctives"
)

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

    st.metric(
        "Taux de conformité",
        f"{taux}%"
    )

st.markdown("---")
st.header("Tableau de bord")

df_historique = pd.DataFrame(
    st.session_state.inspections
)

if not df_historique.empty:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Nombre d'inspections",
        len(df_historique)
    )

    moyenne = round(
        df_historique["Conformité (%)"].mean(),
        2
    )

    col2.metric(
        "Conformité moyenne",
        f"{moyenne}%"
    )

    non_conf = len(
        df_historique[df_historique["Conformité (%)"] < 100]
    )

    col3.metric(
        "Inspections avec NC",
        non_conf
    )

    st.dataframe(
        df_historique,
        use_container_width=True
    )

    excel = "rapport_haccp.xlsx"

    df_historique.to_excel(
        excel,
        index=False
    )

    with open(excel, "rb") as file:
        st.download_button(
            "📥 Télécharger le rapport Excel",
            data=file,
            file_name=excel
        )

else:
    st.info("Aucune inspection enregistrée.")
