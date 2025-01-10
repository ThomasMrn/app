from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import markdown

text = """
voci un exemple des du raisnoment que tu devrais avoir
Stratégie de prospection très ciblée pour Cambon Partners, une approche personnalisée :

Cibles prioritaires à prospecter :
Entreprises tech/SaaS :
CA : 5-50M€
Croissance >30%
Secteurs : FinTech, MarTech, E-commerce, etc…
Maturité : Série B à Exit (according ticket moyen sur le site Cambon)
Sources de deal :
Fonds de croissance actifs (Eurazeo, Sagard, BPI)
Directions M&A des grands groupes tech
Conseils (experts-comptables, avocats d’affaires)
Canaux de prospection :

LinkedIn Sales Navigator pour identifier les décideurs
Base de données Dealroom/CB Insights pour le ciblage
Events sectoriels (France Digitale, Tech Tour)
Timing optimal : 6-12 mois avant une potentielle opération pour maximiser les options stratégiques.

Message Opener nouveau contact LI ou email:
Bonjour [Prénom],

Je suis [Votre nom] de Cambon Partners, cabinet de conseil en M&A spécialisé dans l’accompagnement des entreprises technologiques en forte croissance.

J’ai noté avec intérêt le développement de [Entreprise] sur [segment spécifique]. Votre positionnement sur [élément différenciant] et votre croissance de [X%] ces dernières années sont particulièrement remarquables.

Nous accompagnons régulièrement des sociétés similaires dans leurs opérations stratégiques (ex: [exemple récent pertinent dans leur secteur]). Notre expertise sectorielle nous permet d’identifier les meilleures options de développement, qu’il s’agisse de levées de fonds, de LBO ou de rapprochements industriels.

Seriez-vous disponible pour un court échange sur vos enjeux de développement ?

Bien cordialement, [Signature]

Run de prospection
Les messages sont conçus pour être envoyés à intervalles d’une semaine.

CONSULTING & IT SERVICES:
Message 1:

Bonjour [Prénom],

En tant que Partner chez Cambon Partners, je suis impressionné
 par la croissance de [Société] dans le conseil IT et la transformation
  digitale.

Notre cabinet a récemment accompagné plusieurs acteurs de référence
 du secteur (Manao/Inetum, Maltem/Audensiel, Omnilog/Audensiel)
  dans leurs opérations stratégiques.

Pourrions-nous échanger sur les enjeux de développement 
dans notre secteur ?

Cordialement,
[Nom]
Message 2:

Bonjour [Prénom],

Je reviens vers vous car le secteur du conseil IT connaît une forte
 consolidation, avec des multiples de valorisation attractifs
  (10-12x EBITDA).

Cambon Partners a réalisé plus de 80 transactions dans ce secteur,
 pour un total de 1,5Md€.

Un échange de 20 minutes vous permettrait-il d'avoir notre vision 
du marché ?

Bien à vous,
[Nom]
Message 3:

Bonjour [Prénom],

La transformation digitale et l'IA créent de nouvelles opportunités
 de rapprochements stratégiques dans le conseil IT.

Notre connaissance approfondie de l'écosystème (400+ transactions)
 nous permet d'identifier les meilleures options de développement 
 pour nos clients.

Seriez-vous intéressé par un petit-déjeuner informel pour partager
 nos perspectives ?

Cordialement,
[Nom]
FINANCIAL SERVICES:
Message 1:

Bonjour [Prénom],

Je suis Partner chez Cambon Partners et j'ai noté le développement
 remarquable de [Société] dans les services financiers digitaux.

Notre cabinet accompagne régulièrement des acteurs innovants du 
secteur (Eres/Eurazeo, EUODIA/ODEALIM, Groupe APICIL/ALPHEYS) 
dans leurs opérations stratégiques.

Pourrions-nous échanger sur les opportunités du marché ?

Cordialement,
[Nom]
Message 2:

Bonjour [Prénom],

La digitalisation des services financiers crée de nouvelles 
opportunités de consolidation, notamment dans [segment spécifique].

Cambon Partners a réalisé plus de 60 transactions dans la fintech
 et les services financiers, représentant plus de 800M€.

Un café vous permettrait-il d'avoir notre vision des tendances
 du marché ?

Bien à vous,
[Nom]
Message 3:

Bonjour [Prénom],

L'évolution réglementaire et technologique favorise les 
rapprochements stratégiques dans les services financiers.

Notre expertise sectorielle et notre réseau international 
nous permettent d'identifier les meilleures options de croissance
 externe ou de partenariats.

Seriez-vous disponible pour un échange confidentiel sur vos projets ?

Cordialement,
[Nom]
E-TRAVEL & HOSPITALITY:
Message 1:

Bonjour [Prénom],

Je suis Partner chez Cambon Partners et le développement de [Société] 
dans le travel-tech a retenu mon attention.

Nous avons accompagné récemment Travelsoft dans l'acquisition de 
TravelgateX/ATCORE, LoungeUp/D-EDGE, et bnetwork dans son LBO avec CAPZA.

Un échange sur les dynamiques du secteur vous intéresserait-il ?

Cordialement,
[Nom]
Message 2:

Bonjour [Prénom],

La reprise post-Covid a créé de nouvelles opportunités dans le 
travel-tech, particulièrement dans [segment spécifique].

Notre expertise (50+ transactions dans le secteur) nous permet
 d'identifier les meilleures options de croissance externe ou de
  levée de fonds.

Pourrions-nous partager notre vision du marché autour d'un café ?

Bien à vous,
[Nom]
Message 3:

Bonjour [Prénom],

Les nouveaux usages et la consolidation du marché créent des 
opportunités uniques dans le travel-tech.

Nous avons une compréhension fine des valorisations et des acteurs 
stratégiques, avec un réseau international établi.

Seriez-vous disponible pour un échange confidentiel sur vos 
enjeux de développement ?

Cordialement,
[Nom]
ENTERPRISE SOFTWARE:
Message 1:

Bonjour [Prénom],

En tant que Partner chez Cambon Partners, je suis impressionné 
par la croissance de [Société] dans le SaaS.

Notre cabinet a récemment conseillé Polar/H.I.G Capital, AnaCAP/Cleva,
 et ORISHA dans leurs opérations stratégiques.

Un échange sur les tendances du marché vous intéresserait-il ?

Cordialement,
[Nom]
Message 2:

Bonjour [Prénom],

Le SaaS connaît une forte consolidation avec des valorisations 
attractives, notamment dans [segment spécifique].

Cambon Partners a réalisé 70+ transactions dans le software, 
donnant une vision unique des multiples et des acquéreurs stratégiques.

Pourrions-nous partager nos perspectives lors d'un déjeuner ?

Bien à vous,
[Nom]
Message 3:

Bonjour [Prénom],

L'évolution vers le cloud et l'IA crée de nouvelles opportunités
 de rapprochement dans le software.

Notre expertise sectorielle nous permet d'identifier les meilleures
 options stratégiques pour maximiser la valeur de votre entreprise.

Un échange confidentiel sur vos projets vous conviendrait-il ?

Cordialement,
[Nom]
E-COMMERCE & RETAIL:
Message 1:

Bonjour [Prénom],

Partner chez Cambon Partners, j'ai suivi avec intérêt le développement 
de [Société] dans l'e-commerce.

Nous avons accompagné Pony, AQUAchiara/TowerBrook, et Ecodrop/Amundi 
dans leurs opérations stratégiques récentes.

Pourrions-nous échanger sur les dynamiques du marché e-commerce ?

Cordialement,
[Nom]
Message 2:

Bonjour [Prénom],

L'évolution du commerce unifié crée de nouvelles opportunités, 
particulièrement dans [segment spécifique].

Notre track-record (60+ transactions e-commerce) offre une 
vision unique des multiples et options stratégiques.

Un échange sur les perspectives du secteur vous intéresserait-il ?

Bien à vous,
[Nom]
Message 3:

Bonjour [Prénom],

La consolidation du marché e-commerce s'accélère, avec des valorisations
 attractives pour les acteurs performants.

Notre expertise nous permet d'identifier les meilleures options de
 développement (LBO, M&A, levée de fonds).

Seriez-vous disponible pour un déjeuner confidentiel ?

Cordialement,
[Nom]
DIGITAL MEDIA:
Message 1:

Bonjour [Prénom],

Partner chez Cambon Partners, je suis impressionné par le positionnement 
de [Société] dans le digital media.

Nous avons récemment accompagné ESKIMOZ/SIPAREX, Mentorshow/Educapital,
 et YKONE dans leurs opérations stratégiques.

Un échange sur les tendances du marché vous intéresserait-il ?

Cordialement,
[Nom]
Message 2:

Bonjour [Prénom],

Le secteur des médias digitaux connaît une forte consolidation, 
notamment dans [segment spécifique].

Notre expertise (40+ transactions) nous donne une vision unique des
 multiples et des acquéreurs potentiels.

Pourrions-nous partager nos perspectives autour d'un café ?

Bien à vous,
[Nom]
Message 3:

Bonjour [Prénom],

L'évolution des modèles économiques crée des opportunités uniques 
dans le digital media.

Notre connaissance approfondie du marché nous permet d'identifier 
les meilleures options stratégiques de développement.

Seriez-vous ouvert à un échange confidentiel sur vos projets ?

Cordialement,
[Nom]
HEALTHCARE:
Message 1:

Bonjour [Prénom],

Partner chez Cambon Partners, j'ai noté le développement 
remarquable de [Société] dans la healthtech.

Nous avons accompagné VITALLIANCE/PARQUEST, FAMECO/SURPLUS SOLUTIONS,
 et Keosys/Banook dans leurs opérations stratégiques.

Pourrions-nous échanger sur les dynamiques du secteur ?

Cordialement,
[Nom]
Message 2:

Bonjour [Prénom],

La digitalisation de la santé crée de nouvelles opportunités, 
particulièrement dans [segment spécifique].

Notre expertise (30+ transactions healthtech) nous permet d'identifier
 les meilleures options de développement.

Un petit-déjeuner pour partager notre vision du marché vous
 conviendrait-il ?

Bien à vous,
[Nom]
Message 3:

Bonjour [Prénom],

La consolidation du secteur healthcare s'accélère, avec des 
valorisations attractives pour les acteurs innovants.

Notre réseau international et notre compréhension du marché nous
 permettent d'optimiser vos options stratégiques.

Seriez-vous disponible pour un échange confidentiel ?

Cordialement,
[Nom]
"""

client = """
entreprises dans le transport maritine aviation route logistique mobilité verte infrastructures électriques durables industrie manufactuière (rail hors France) pas d’acteur publiuc ou parapubliue
"""
#GROK API
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
API_KEY = "xai-L1ABYqViMpbZoBIuYtMs8aFyLmgxGM9yKBTQgiS4RlFUJLFUGlnGXFHXVNLBtnSzNthkNO1fT0hm8RyE"

app = Flask(__name__)
combined_scrap =""
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process/pre_prompt", methods=["POST"])
def process_pre_prompt():
    data = request.json
    messages = data.get("messages", [])  # Liste des liens
    if not messages:
        return {"error": "Aucun lien fourni"}, 400

    # Traitement des données pour générer le Pre Prompt
    scrap_results = [scrapping(message) for message in messages]
    combined_scrap = " ".join(scrap_results)
    system_content = "Tu es un expert génération de prepromt de context pour les llms"
    
    user_content = f"Peux-tu me générer un prepromt de context pour définir le rôle d'un llm specialiser en prospection qui travaille dans l'entreprise décrite par ces données {combined_scrap}"
    pre_prompt = markdown.markdown(prompt(system_content, user_content))

    return {"pre_prompt": pre_prompt}


@app.route("/process/step_1", methods=["POST"])
def process_step_1():
    data = request.json
    pre_prompt = data.get("pre_prompt")  # Le Pre Prompt généré précédemment
    if not pre_prompt:
        return {"error": "Pre Prompt manquant"}, 400

    # Génération de Step 1 à partir du Pre Prompt
    system_content = pre_prompt
    user_content = f"Voici un exmple exemple de rasionement : {text} , j'aimerais que tu me rediges les messages en adaptant avec ces informations {combined_scrap} pour ces clinets  : {client}"
    step1 = markdown.markdown(prompt(system_content, user_content))

    return {"step1": step1}


@app.route("/process/messages", methods=["POST"])
def process_messages():
    data = request.json
    step1 = data.get("step1")  # Le Step 1 généré précédemment
    if not step1:
        return {"error": "Step 1 manquant"}, 400

    # Génération des messages à partir de Step 1
    user_content = f"{step1}"
    step2 = prompt(step1, user_content)

    html_content = markdown.markdown(step2)
    messages_list = html_content.split("//")  # Diviser les messages générés en une liste

    return {"messages_list": messages_list}


def prompt(sys_content, user_cotent):

    payload = {
        "messages": [
            {
                "role": "system",
                "content": sys_content
            },
            {
                "role": "user",
                "content": user_cotent
            }
        ],
        "model": "grok-beta",
        "stream": False,
        "temperature": 0
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
     
    response = requests.post(GROK_API_URL, json=payload, headers=headers)
    response_data = response.json()
    content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Contenu non trouvé")
    return content

def scrapping(url : str) -> str:
    response = requests.get(url)
# Vérifier le statut de la requête
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraire tout le texte de la page
        all_text = soup.get_text(separator='\n')
        
        # Nettoyer le texte pour supprimer les lignes vides ou contenant uniquement des espaces
        cleaned_text = "\n".join([line.strip() for line in all_text.splitlines() if line.strip()])
        
        # Afficher le texte nettoyé
        return(cleaned_text)
    
    else:
        print(f"Erreur : {response.status_code}")

if __name__ == "__main__":
    app.run(debug=True)

