import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="Tech-Guru Bot", page_icon="🤖")

st.title("🤖 Tech-Guru : L'Assistant 100% Info")
st.markdown("""
Je suis un expert en : **Python, Java, Data, Réseaux, et DevOps**.
Pose-moi une question technique, je suis là pour ça.
*(Je ne réponds pas aux questions hors sujet !)*
""")

# --- GESTION DE LA CLE API (Sécurité) ---
try:
    # On cherche la clé dans les secrets Streamlit (.streamlit/secrets.toml)
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ Erreur : Clé API introuvable.")
    st.info("Crée un dossier .streamlit et un fichier secrets.toml avec ta clé GOOGLE_API_KEY.")
    st.stop()

# --- DEFINITION DU CERVEAU (MODEL) ---
# 1. La personnalité de l'IA
system_instruction = """
Tu es un assistant spécialisé EXCLUSIVEMENT dans l'informatique, le développement logiciel, 
la data science et les technologies numériques.
Tes réponses doivent être précises, techniques et inclure des exemples de code si nécessaire.
SI l'utilisateur te pose une question qui n'a AUCUN rapport avec l'informatique (ex: cuisine, sport, politique),
refuse poliment de répondre en disant que tu es programmé uniquement pour la tech.
"""

# 2. Le choix du modèle (CORRECTION ICI : On utilise le 1.5 Flash)
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # Le modèle rapide et actuel
        system_instruction=system_instruction # On lui donne sa personnalité ici !
    )
except Exception as e:
    st.error(f"Erreur de chargement du modèle : {e}")
    st.stop()

# --- MEMOIRE DE LA CONVERSATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialisation du chat avec l'historique
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- AFFICHAGE DE L'HISTORIQUE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ZONE DE CHAT ---
user_input = st.chat_input("Pose ta question tech ici...")

if user_input:
    # 1. Afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Envoyer à l'IA et récupérer la réponse
    try:
        # On envoie le message à la session de chat
        response = st.session_state.chat_session.send_message(user_input)
        bot_reply = response.text
        
        # 3. Afficher la réponse du bot
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
            
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")