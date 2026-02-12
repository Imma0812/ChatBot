import streamlit as st
from google import genai

# --- CONFIGURATION ---
st.set_page_config(page_title="Tech-Guru Bot", page_icon="🤖")

st.title("🤖 Tech-Guru : L'Assistant 100% Info")
st.markdown("""
Je suis un expert en : **Python, Java, Data, Réseaux, et DevOps**.
Pose-moi une question technique, je suis là pour ça.
*(Je ne réponds pas aux questions hors sujet !)*
""")

# --- CLE API ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("⚠️ Erreur : Clé API introuvable.")
    st.stop()

# --- PERSONNALITÉ ---
system_instruction = """
Tu es un assistant spécialisé EXCLUSIVEMENT dans l'informatique,
le développement logiciel, la data science et les technologies numériques.
Tes réponses doivent être précises et inclure du code si nécessaire.
Si la question est hors sujet, refuse poliment.
"""

# --- MÉMOIRE SIMPLE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AFFICHAGE HISTORIQUE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT UTILISATEUR ---
user_input = st.chat_input("Pose ta question tech ici...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # modèle recommandé
            contents=f"{system_instruction}\n\nQuestion utilisateur: {user_input}"
        )

        bot_reply = response.text

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        with st.chat_message("assistant"):
            st.markdown(bot_reply)

    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
