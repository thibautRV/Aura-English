import streamlit as st
import json
import os

st.set_page_config(page_title="FrameByFrame - Diagnostic", page_icon="🎬", layout="centered")

st.title("🎬 FrameByFrame — Diagnostic initial")
st.write("Bienvenue Cédric ! Ce premier test rapide va nous aider à cibler tes points forts et tes axes de progression.")

# Charger les données du quiz
@st.cache_data
def load_quiz_data():
    with open("data/diagnostic.json", "r", encoding="utf-8") as f:
        return json.load(f)

try:
    data = load_quiz_data()
except Exception as e:
    st.error("Erreur lors du chargement des données. Vérifie que le fichier data/diagnostic.json existe.")
    st.stop()

# --- PARTIE 1 : COMPRÉHENSION ORALE ---
st.header("🎵 1. Compréhension Orale")
st.write("Écoute l'extrait audio ci-dessous, puis réponds à la question.")

audio_file_path = data["listening"]["audio_path"]
if os.path.exists(audio_file_path):
    st.audio(audio_file_path, format="audio/mp3")
else:
    st.warning("⚠️ Fichier audio d'entraînement manquant dans `assets/audio/`. Charge ton enregistrement pour l'écouter !")

user_audio_choice = st.radio(
    data["listening"]["question"],
    options=data["listening"]["options"],
    index=None,
    key="audio_diagnostic"
)

st.write("---")

# --- PARTIE 2 : COMPRÉHENSION ÉCRITE ---
st.header("📚 2. Compréhension Écrite & Grammaire")

user_reading_choices = {}
for q in data["reading"]:
    st.subheader(f"Question {q['id']} — {q['category']}")
    st.markdown(q["question"])
    user_reading_choices[q["id"]] = st.radio(
        "Choisis la bonne réponse :",
        options=q["options"],
        index=None,
        key=f"reading_{q['id']}"
    )
    st.write("---")

# --- SOUMISSION ---
if st.button("Valider mes réponses", type="primary"):
    # Vérification
    all_answered = (user_audio_choice is not None) and all(ans is not None for ans in user_reading_choices.values())
    
    if not all_answered:
        st.warning("Prends le temps de répondre à toutes les questions avant de valider.")
    else:
        st.balloons()
        st.header("📊 Analyse du Diagnostic")
        
        score = 0
        total = len(data["reading"]) + 1
        
        # Check Audio
        st.subheader("Compréhension Orale")
        if user_audio_choice == data["listening"]["correct_answer"]:
            st.success("✅ Excellent ! Tu as capté l'élément clé de la consigne du réalisateur.")
            score += 1
        else:
            st.error(f"❌ Ce n'est pas tout à fait ça.")
            st.info(f"💡 **Correction :** {data['listening']['correct_answer']}\n\n*Explication : {data['listening']['explanation']}*")
            
        # Check Reading
        st.subheader("Compréhension Écrite")
        for q in data["reading"]:
            user_ans = user_reading_choices[q["id"]]
            if user_ans == q["correct_answer"]:
                st.success(f"Question {q['id']} : ✅ Correct !")
                score += 1
            else:
                st.error(f"Question {q['id']} : ❌ Retente ta chance au prochain essai.")
                st.info(f"💡 **Correction :** {q['correct_answer']}\n\n*Explication : {q['explanation']}*")
        
        # Score final
        st.metric(label="Ton score global", value=f"{score} / {total}")