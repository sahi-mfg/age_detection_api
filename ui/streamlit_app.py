import io

import requests  # type: ignore
import streamlit as st  # type: ignore
from PIL import Image  # type: ignore

# Configuration de la page
st.set_page_config(
    page_title="Application de Détection d'âge",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personnalisé pour améliorer l'apparence de l'application
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
        border-radius: 0.5rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Titre et description de l'application
st.title("🔍 Détection d'âge")
st.markdown("### Prédisez la tranche d'âge d'une personne à partir d'une image")

# Barre latérale pour des informations supplémentaires
with st.sidebar:
    st.header("À propos")
    st.info(
        "Cette application utilise l'IA pour prédire la tranche d'âge d'une personne à partir d'une image téléchargée."
    )
    st.write("Types de fichiers pris en charge : JPG, JPEG, PNG")


def api_call(img_bytes):
    response = requests.post(
        "https://fastapi-app-ml-msze6264nq-od.a.run.app/predict",
        files={"file": ("image.png", img_bytes, "image/png")},
    )
    return response


# Contenu principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Télécharger une Image")
    fichier_telecharge = st.file_uploader(
        "Choisissez une photo d'une personne",
        type=["jpg", "jpeg", "png"],
        help="Glissez-déposez ou cliquez pour télécharger",
    )

    if fichier_telecharge is not None:
        image = Image.open(fichier_telecharge)
        st.image(image, caption="Image Téléchargée", use_column_width=True)

        with st.spinner("Analyse de l'image en cours..."):
            # Conversion de l'image en bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="PNG")
            img_bytes = img_byte_arr.getvalue()

            # Envoi d'une requête POST à l'endpoint de l'API
            reponse = api_call(img_bytes)

        if reponse.status_code == 200:
            req = reponse.json()
            prediction = req["predictions"]

            with col2:
                st.subheader("Résultat de la Prédiction")
                st.success("🎉 Tranche d'âge Prédite")
                st.markdown(f"### {prediction} ans")
        else:
            st.error("Échec de la réponse de l'API. Veuillez réessayer.")

# Pied de page
st.markdown("---")
st.markdown("Developed with ❤️ by [Mohamed Francis Sahi](https://github.com/sahi-mfg)")
