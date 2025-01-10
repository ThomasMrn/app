import streamlit as st
import pandas as pd
import gender_guesser.detector as gender

# Fonction pour détecter le genre en fonction du prénom
def detect_gender(first_name):
    detector = gender.Detector()
    gender_guess = detector.get_gender(first_name)
    if gender_guess in ["male", "mostly_male"]:
        return "Male"
    elif gender_guess in ["female", "mostly_female"]:
        return "Female"
    elif gender_guess == "andy":
        return "Unisex"
    else:
        return "Unknown"

# Configuration de l'application
st.title("Détection du genre dans un fichier Excel")

# Étape 1 : Chargement du fichier
uploaded_file = st.file_uploader("Téléchargez un fichier Excel", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # Chargement du fichier Excel
        df = pd.read_excel(uploaded_file)

       
        # Étape 2 : Sélection de la colonne des prénoms
        st.write("### Sélectionnez la colonne contenant les prénoms :")
        col1 = st.selectbox("Colonne contenant les prénoms", df.columns, key="col1")
        col_genre = st.selectbox("Colonne où enregistrer le genre", ["Créer une nouvelle colonne"] + list(df.columns), key="col_genre")

        # Bouton pour valider
        if st.button("Valider"):
            if col1:
                # Ajout ou mise à jour de la colonne sélectionnée pour le genre
                if col_genre == "Créer une nouvelle colonne":
                    df["Genre"] = df[col1].apply(detect_gender)
                    col_genre = "Genre"
                else:
                    df[col_genre] = df[col1].apply(detect_gender)

                st.write("### Résultat :")
                st.dataframe(df[[col1, col_genre]].head())

                # Enregistrer le fichier modifié en mémoire
                output_file = "fichier_avec_genre.xlsx"
                df.to_excel(output_file, index=False)

                st.success("Fichier modifié prêt à être téléchargé.")

                # Bouton pour télécharger le fichier modifié
                with open(output_file, "rb") as f:
                    st.download_button(label="Télécharger le fichier modifié", data=f, file_name=output_file)
            else:
                st.error("Veuillez sélectionner une colonne contenant les prénoms.")

    except Exception as e:
        st.error(f"Erreur lors du traitement du fichier : {e}")
