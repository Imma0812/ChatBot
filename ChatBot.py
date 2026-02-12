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
# On récupère la clé depuis les "Secrets" de Streamlit (voir tuto déploiement)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Erreur : Clé API manquante. Ajoute-la dans les secrets Streamlit.")
    st.stop()

# --- DEFINITION DU CERVEAU (MODEL) ---
# C'est ici qu'on donne la personnalité à l'IA
system_instruction = """
Tu es un assistant spécialisé EXCLUSIVEMENT dans l'informatique, le développement logiciel, 
la data science et les technologies numériques.
Tes réponses doivent être précises, techniques et inclure des exemples de code si nécessaire.
SI l'utilisateur te pose une question qui n'a AUCUN rapport avec l'informatique (ex: cuisine, sport, politique),
refuse poliment de répondre en disant que tu es programmé uniquement pour la tech.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # Modèle rapide et gratuit
    system_instruction=system_instruction
)

# --- MEMOIRE DE LA CONVERSATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

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
        response = st.session_state.chat_session.send_message(user_input)
        bot_reply = response.text
        
        # 3. Afficher la réponse du bot
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
            
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")