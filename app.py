import streamlit as st
import json
import os

st.set_page_config(page_title="Aura-English - Test Diagnostique", page_icon="🎬", layout="centered")

st.title("Test Diagnostique")
st.write("Salut Cédric ! Ce test va nous permettre de voir où tu en es en grammaire et en écoute. Fais de ton mieux, sans stress !")

# Chargement sécurisé du JSON
@st.cache_data
def load_quiz_data():
    with open("data/diagnostic.json", "r", encoding="utf-8") as f:
        return json.load(f)

try:
    data = load_quiz_data()
except Exception as e:
    st.error("Impossible de charger le fichier 'data/diagnostic.json'. Assure-toi de l'avoir créé.")
    st.stop()

# --- PARTIE 1 : COMPRÉHENSION ORALE ---
st.header("🎵 1. Compréhension Orale")
st.write("Écoute l'extrait audio puis réponds à la question ci-dessous.")

# On affiche un lecteur audio si tu as mis un fichier local
audio_file_path = "assets/audio/diagnostic.mp3"
if os.path.exists(audio_file_path):
    st.audio(audio_file_path, format="audio/mp3")
else:
    # Fallback propre si tu utilises un lien YouTube pour l'instant
    st.info(f"🔗 [Clique ici pour écouter l'audio sur YouTube]({data['listening']['youtube_url']})")

user_audio_choice = st.radio(
    data["listening"]["question"],
    options=None,
    index=None,
    key="audio_diagnostic"
)

st.write("---")

# --- PARTIE 2 : GRAMMAIRE / ORTHOGRAPHE / CONJUGAISON ---
st.header("📚 2. Grammaire, Orthographe & Conjugaison")
st.write("Choisis la bonne option pour compléter chaque phrase.")

user_answers = {}
for q in data["grammar_quiz"]:
    st.markdown(f"**Question {q['id']}** — *{q['category']}*")
    user_answers[q["id"]] = st.radio(
        q["question"],
        options=q["options"],
        index=None,
        key=f"grammar_{q['id']}"
    )
    st.write("") # Petit espace

st.write("---")

# --- VALIDATION ET COMPTAGE DES POINTS ---
if st.button("Valider mes réponses", type="primary"):
    # Vérification que tout est coché
    unanswered_grammar = [q_id for q_id, ans in user_answers.items() if ans is None]
    
    if user_audio_choice is None or unanswered_grammar:
        st.warning("⚠️ Oups ! Tu as oublié de répondre à certaines questions. Prends le temps de tout cocher.")
    else:
        st.balloons()
        st.header("📊 Tes Résultats")
        
        score_audio = 0
        score_grammar = 0
        total_grammar = len(data["grammar_quiz"])
        
        # 1. Bilan Audio
        st.subheader("🎵 Compréhension Orale")
        if user_audio_choice == data["listening"]["correct_answer"]:
            st.success("✅ Correct ! Tu as une excellente oreille.")
            score_audio += 1
        else:
            st.error("❌ Ce n'est pas la bonne réponse.")
            with st.expander("Voir l'explication"):
                st.write(f"**Bonne réponse :** {data['listening']['correct_answer']}")
                st.write(f"**Pourquoi ?** {data['listening']['explanation']}")
                
        # 2. Bilan Grammaire
        st.subheader("📚 Grammaire, Orthographe & Conjugaison")
        
        for q in data["grammar_quiz"]:
            user_ans = user_answers[q["id"]]
            correct_ans = q["correct_answer"]
            
            if user_ans == correct_ans:
                score_grammar += 1
                st.success(f"Question {q['id']} : ✅ Correct !")
            else:
                st.error(f"Question {q['id']} : ❌ Erreur.")
                with st.expander(f"Voir la correction de la question {q['id']}"):
                    st.write(f"**Phrase correcte :** {q['question'].replace('__________', f'**{correct_ans.split()[1]}**') if len(correct_ans.split()) > 1 else q['question'].replace('__________', f'**{correct_ans}**')}")
                    st.write(f"**Explication :** {q['explanation']}")
        
        # Section Scores
        st.markdown("### 🏆 Récapitulatif")
        col1, col2 = st.columns(2)
        col1.metric("Score Audio", f"{score_audio} / 1")
        col2.metric("Score Grammaire", f"{score_grammar} / {total_grammar}")
        
        # Analyse pédago
        global_score = score_audio + score_grammar
        global_total = total_grammar + 1
        
        if global_score >= (global_total * 0.8):
            st.success("Félicitations Cédric ! Tu as de superbes bases, on va pouvoir attaquer le TOEIC très vite ! 🚀")
        elif global_score >= (global_total * 0.5):
            st.warning("Bon travail ! Les bases sont là mais il y a quelques confusions à éclaircir ensemble. 👍")
        else:
            st.info("C'est un bon point de départ. Ce test montre exactement ce qu'on doit travailler en priorité. Pas d'inquiétude ! 💪")