import streamlit as st

st.set_page_config(
    page_title="HACCP Pullman Oran",
    page_icon="✅",
    layout="wide"
)

st.title("✅ CHECK-LIST D'INSPECTION HACCP")

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
        "Réception"
    ]
)

st.write("Inspecteur :", inspecteur)
st.write("Zone :", zone)

if st.button("Tester"):
    st.success("Application fonctionnelle")
