import streamlit as st
import validators
import requests
from bs4 import BeautifulSoup
import markdown

#GROK API
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
API_KEY = "xai-L1ABYqViMpbZoBIuYtMs8aFyLmgxGM9yKBTQgiS4RlFUJLFUGlnGXFHXVNLBtnSzNthkNO1fT0hm8RyE"


def prompt(system_content, user_content):
    """Simule une fonction qui génère un pré-prompt"""
    return f"System: {system_content}\nUser: {user_content}"

# Initialiser ou récupérer la liste des liens
if "links" not in st.session_state:
    st.session_state["links"] = []

if "scraped_content" not in st.session_state:
    st.session_state["scraped_content"] = ""

def add_link(link):
    """Ajoute un lien à la liste si valide."""
    if validators.url(link):
        if link not in st.session_state["links"]:
            st.session_state["links"].append(link)
    else:
        st.error("Lien non valide")

def remove_link(link):
    """Supprime un lien de la liste."""
    if link in st.session_state["links"]:
        st.session_state["links"].remove(link)

def scrapping(url: str) -> str:
    response = requests.get(url)
    # Vérifier le statut de la requête
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraire tout le texte de la page
        all_text = soup.get_text(separator='\n')

        # Nettoyer le texte pour supprimer les lignes vides ou contenant uniquement des espaces
        cleaned_text = "\n".join([line.strip() for line in all_text.splitlines() if line.strip()])

        # Retourner le texte nettoyé
        return cleaned_text

    else:
        return f"Erreur : {response.status_code}"

def scap(links):
    """Scrape les contenus des liens."""
    scraped_data = []
    for link in links:
        try:
            content = scrapping(link)
            scraped_data.append(f"# Contenu extrait de {link}\n\n{content}")
        except Exception as e:
            scraped_data.append(f"# Contenu extrait de {link}\n\nErreur lors du scraping : {e}")
    return "\n\n".join(scraped_data)

def process_pre_prompt():
    """Génère un pré-prompt à partir du contenu extrait."""
    if not st.session_state["scraped_content"]:
        st.error("Aucun contenu extrait disponible pour générer le pré-prompt.")
        return

    scrap_results = st.session_state["scraped_content"]
    system_content = "Tu es un expert génération de prepromt de context pour les llms"

    user_content = f"Peux-tu me générer un prepromt de context pour définir le rôle d'un llm specialiser en prospection qui travaille dans l'entreprise décrite par ces données {scrap_results}"
    pre_prompt = markdown.markdown(prompt(system_content, user_content))

    st.session_state["pre_prompt"] = pre_prompt

st.title("Gestionnaire de Liens")

# Entrée pour ajouter un nouveau lien
new_link = st.text_input("Nouveau lien :")
if st.button("Ajouter"):
    add_link(new_link)

st.write("### Liste des liens")

# Afficher la liste des liens
if st.session_state["links"]:
    for link in st.session_state["links"]:
        col1, col2 = st.columns([4, 1])
        col1.write(link)
        col2.button("Supprimer", key=f"remove_{link}", on_click=remove_link, args=(link,))
else:
    st.info("Aucun lien ajouté pour le moment.")

# Bouton pour valider et scraper les contenus des liens
if st.session_state["links"]:
    if st.button("Valider"):
        st.session_state["scraped_content"] = scap(st.session_state["links"])

# Zone de texte pour afficher et éditer le contenu extrait
if st.session_state["scraped_content"]:
    st.write("### Contenu extrait")
    st.session_state["scraped_content"] = st.text_area("", value=st.session_state["scraped_content"], height=400)

    # Bouton pour générer le pré-prompt
    if st.button("Générer le Pré-Prompt"):
        process_pre_prompt()

# Afficher le pré-prompt généré
if "pre_prompt" in st.session_state:
    st.write("### Pré-Prompt généré")
    st.text_area("", value=st.session_state["pre_prompt"], height=200)
