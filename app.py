import streamlit as st
import json
import random
from pathlib import Path

st.set_page_config(page_title="QCM – UTBM", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0f172a; }
    .stApp { background-color: #0f172a; }
    h1 { color: #38bdf8 !important; }
    h2 { color: #7dd3fc !important; }
    h3 { color: #e2e8f0 !important; }

    .subject-card {
        background: linear-gradient(135deg, #1e293b, #1a2744);
        border: 2px solid #334155;
        border-radius: 16px;
        padding: 32px 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        margin: 8px;
    }
    .subject-icon   { font-size: 3rem; margin-bottom: 12px; }
    .subject-title  { font-size: 1.6rem; font-weight: 800; color: #f1f5f9; margin-bottom: 6px; }
    .subject-subtitle { font-size: 0.9rem; color: #94a3b8; margin-bottom: 16px; }
    .subject-stats  { font-size: 0.85rem; color: #7dd3fc; }

    .question-card {
        background: linear-gradient(135deg, #1e293b, #1a2744);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .question-text { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; margin-bottom: 16px; line-height: 1.6; }
    .correct-answer { background: linear-gradient(135deg,#064e3b,#065f46); border: 2px solid #10b981; border-radius: 8px; padding: 12px 16px; color: #6ee7b7; font-weight: 600; margin: 6px 0; }
    .wrong-answer   { background: linear-gradient(135deg,#450a0a,#7f1d1d); border: 2px solid #ef4444; border-radius: 8px; padding: 12px 16px; color: #fca5a5; font-weight: 600; margin: 6px 0; }
    .neutral-answer { background: #1e293b; border: 1px solid #475569; border-radius: 8px; padding: 12px 16px; color: #94a3b8; margin: 6px 0; }
    .explication-box { background: linear-gradient(135deg,#1e3a5f,#1e2d4a); border-left: 4px solid #38bdf8; border-radius: 0 8px 8px 0; padding: 14px 18px; color: #bae6fd; margin-top: 12px; font-size: 0.95rem; }

    .fiche-header {
        background: linear-gradient(135deg, #1e293b, #0f2a4a);
        border: 2px solid #38bdf8;
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 18px;
        box-shadow: 0 4px 20px rgba(56,189,248,0.15);
    }
    .fiche-intro { color: #cbd5e1; font-size: 1rem; line-height: 1.7; margin: 0; }
    .fiche-section {
        background: #1e293b;
        border: 1px solid #334155;
        border-left: 4px solid #38bdf8;
        border-radius: 0 10px 10px 0;
        padding: 16px 20px;
        margin-bottom: 14px;
    }
    .fiche-section-title { color: #7dd3fc; font-size: 1rem; font-weight: 700; margin-bottom: 10px; }
    .fiche-item { color: #cbd5e1; font-size: 0.92rem; line-height: 1.75; margin: 4px 0; padding-left: 8px; }
    .fiche-retenir {
        background: linear-gradient(135deg, #1c3a2a, #14532d);
        border: 2px solid #22c55e;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 6px;
    }
    .fiche-retenir-title { color: #86efac; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px; }
    .fiche-retenir-text  { color: #bbf7d0; font-size: 0.9rem; line-height: 1.6; }

    .score-card { background: linear-gradient(135deg,#1e293b,#0f2a4a); border: 2px solid #38bdf8; border-radius: 16px; padding: 30px; text-align: center; box-shadow: 0 8px 32px rgba(56,189,248,0.2); }
    .score-number { font-size: 3.5rem; font-weight: 800; background: linear-gradient(135deg,#38bdf8,#818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .badge-excellent { color: #10b981; font-size: 1.2rem; font-weight: 700; }
    .badge-good      { color: #f59e0b; font-size: 1.2rem; font-weight: 700; }
    .badge-fail      { color: #ef4444; font-size: 1.2rem; font-weight: 700; }
    .progress-text   { color: #94a3b8; font-size: 0.9rem; }
    .cat-badge { display: inline-block; background: #1e3a5f; color: #7dd3fc; border: 1px solid #38bdf8; border-radius: 20px; padding: 3px 12px; font-size: 0.8rem; margin-bottom: 10px; }

    /* ── Onglets élargis ── */
    .stTabs [data-baseweb="tab-list"]  { background: #1e293b; border-radius: 10px; gap: 6px; padding: 4px; }
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
        min-width: 180px !important;
    }
    .stTabs [aria-selected="true"] { background: #1d4ed8 !important; color: white !important; }

    div[data-testid="stButton"] button { background: linear-gradient(135deg,#1d4ed8,#2563eb) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; }
    div[data-testid="stButton"] button:hover { background: linear-gradient(135deg,#2563eb,#3b82f6) !important; transform: translateY(-1px) !important; box-shadow: 0 4px 12px rgba(37,99,235,0.4) !important; }

    .stRadio label { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] { background-color: #1e293b !important; }
    .stMetric label { color: #7dd3fc !important; }
    .stMetric [data-testid="stMetricValue"] { color: #f1f5f9 !important; }
    .breadcrumb { color: #64748b; font-size: 0.85rem; margin-bottom: 4px; }
    .breadcrumb span { color: #38bdf8; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_subject(json_file: str):
    path = Path(__file__).parent / json_file
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    all_q = []
    for cat in data["categories"]:
        for q in cat["questions"]:
            q["categorie"] = cat["nom"]
            all_q.append(q)
    return data["titre"], data["categories"], all_q

@st.cache_data
def load_cours():
    path = Path(__file__).parent / "cours.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)

SUBJECTS = {
    "SR72": {
        "file": "questions_sr72.json",
        "icon": "🖥️",
        "label": "SR72",
        "subtitle": "Architecture des Systèmes d'Exploitation",
        "description": "Synchronisation, Sémaphores, Moniteurs, Interblocages",
        "color": "#38bdf8",
    },
    "GE79": {
        "file": "questions_ge79.json",
        "icon": "📋",
        "label": "GE79",
        "subtitle": "Management de Projet",
        "description": "RH, Communication, Procurement, Risques, Qualité",
        "color": "#a78bfa",
    },
    "BD71": {
        "file": "questions_bd71.json",
        "icon": "💾",
        "label": "BD71",
        "subtitle": "Big Data & NoSQL",
        "description": "Hadoop, HDFS, MapReduce, Spark, Flink, CAP, NoSQL",
        "color": "#890D85",
    },
    "TI73": {
        "file": "questions_ti73.json",
        "icon": "🎤",
        "label": "TI73",
        "subtitle": "Communication Professionnelle",
        "description": "PowerPoint, Prise de parole, Réunion, Brainstorming",
        "color": "#f59e0b",
    },
}


def init():
    defaults = {
        "mode": "menu",
        "subject_key": None,
        "questions_session": [],
        "index": 0,
        "reponses_utilisateur": {},
        "repondu": False,
        "choix_courant": None,
        "score": 0,
        "historique": {},
        "session_saved": False,
        "fiche_cat": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()


def get_badge(pct):
    if pct >= 80: return "🏆 Excellent !", "badge-excellent"
    if pct >= 60: return "👍 Bien joué !", "badge-good"
    return "📚 À retravailler", "badge-fail"

def start_quiz(questions, melanger=True):
    qs = questions.copy()
    if melanger:
        random.shuffle(qs)
        for q in qs:
            random.shuffle(q["reponses"])
    st.session_state.questions_session = qs
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.reponses_utilisateur = {}
    st.session_state.repondu = False
    st.session_state.choix_courant = None
    st.session_state.session_saved = False
    st.session_state.mode = "quiz"

def save_session_once():
    if not st.session_state.session_saved:
        key   = st.session_state.subject_key
        score = st.session_state.score
        total = len(st.session_state.questions_session)
        pct   = int(score / total * 100) if total > 0 else 0
        if key not in st.session_state.historique:
            st.session_state.historique[key] = []
        st.session_state.historique[key].append({"score": score, "total": total, "pct": pct})
        st.session_state.session_saved = True

def md(text: str) -> str:
    """Convert **bold**, *italic* and ⚠️ markers to HTML."""
    import re
    # **bold**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # *italic* (single star, not already consumed)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # `code`
    text = re.sub(r'`(.+?)`', r'<code style="background:#0f172a;padding:2px 5px;border-radius:4px;">\1</code>', text)
    return text

def render_fiche(cat_nom, cat_data):
    emoji = cat_data.get("emoji", "📖")
    st.markdown(f"## {emoji} {cat_nom}")
    st.markdown(
        f'<div class="fiche-header"><p class="fiche-intro">{md(cat_data["intro"])}</p></div>',
        unsafe_allow_html=True,
    )
    for section in cat_data.get("sections", []):
        html_items = "".join(
            f'<div class="fiche-item">• {md(item)}</div>' for item in section["contenu"]
        )
        st.markdown(
            f'<div class="fiche-section">'
            f'<div class="fiche-section-title">📌 {md(section["titre"])}</div>'
            f'{html_items}'
            f'</div>',
            unsafe_allow_html=True,
        )
    if "a_retenir" in cat_data:
        st.markdown(
            f'<div class="fiche-retenir">'
            f'<div class="fiche-retenir-title">💡 À retenir absolument</div>'
            f'<div class="fiche-retenir-text">{md(cat_data["a_retenir"])}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 QCM – UTBM")
    st.markdown("---")
    if st.button("🏠 Menu principal", use_container_width=True):
        st.session_state.mode = "menu"
        st.rerun()
    if st.session_state.subject_key:
        key = st.session_state.subject_key
        if st.button(f"📚 Accueil {key}", use_container_width=True):
            st.session_state.mode = "accueil"
            st.rerun()
    if st.session_state.mode == "quiz":
        st.markdown("---")
        idx   = st.session_state.index
        total = len(st.session_state.questions_session)
        if total:
            st.metric("Question", f"{idx + 1} / {total}")
            st.metric("Score",    f"{st.session_state.score}")
            st.progress(idx / total)
    histo = st.session_state.historique
    if any(histo.values()):
        st.markdown("---")
        st.markdown("**Historique :**")
        for subj, sessions in histo.items():
            if sessions:
                last = sessions[-1]
                st.markdown(f"**{subj}** – {last['score']}/{last['total']} ({last['pct']}%)")
    st.markdown("---")
    st.markdown('<p style="color:#475569;font-size:0.75rem">UTBM • 2025</p>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE : MENU PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.mode == "menu":
    st.markdown("# 🎓 QCM – Révisions UTBM")
    st.markdown("### Choisis ta matière pour commencer")
    st.markdown("---")
    cols = st.columns(len(SUBJECTS))
    for col, (key, subj) in zip(cols, SUBJECTS.items()):
        try:
            _, cats, all_q = load_subject(subj["file"])
            nb_q    = len(all_q)
            nb_cats = len(cats)
            histo   = st.session_state.historique.get(key, [])
            last_str = f"Dernière : {histo[-1]['pct']}%" if histo else "Pas encore joué"
        except Exception:
            nb_q, nb_cats, last_str = 0, 0, "Fichier introuvable"
        with col:
            st.markdown(f"""
            <div class="subject-card">
                <div class="subject-icon">{subj['icon']}</div>
                <div class="subject-title">{subj['label']}</div>
                <div class="subject-subtitle">{subj['subtitle']}</div>
                <div style="color:#64748b;font-size:0.82rem;margin-bottom:12px">{subj['description']}</div>
                <div class="subject-stats">📝 {nb_q} questions · 📂 {nb_cats} thèmes</div>
                <div style="color:#475569;font-size:0.8rem;margin-top:6px">{last_str}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"▶️ Lancer {key}", key=f"btn_{key}", use_container_width=True):
                st.session_state.subject_key = key
                st.session_state.mode = "accueil"
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE : ACCUEIL MATIÈRE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.mode == "accueil":
    key  = st.session_state.subject_key
    subj = SUBJECTS[key]

    try:
        titre, categories, toutes_questions = load_subject(subj["file"])
    except FileNotFoundError:
        st.error(f"Fichier '{subj['file']}' introuvable.")
        st.stop()

    try:
        cours_data = load_cours()
        fiches = cours_data.get(key, {})
    except Exception:
        fiches = {}

    st.markdown(f'<p class="breadcrumb">🏠 Menu › <span>{key} – {subj["subtitle"]}</span></p>', unsafe_allow_html=True)
    st.markdown(f"# {subj['icon']} {titre}")
    st.markdown("---")

    tab_quiz, tab_fiches = st.tabs(["📝  S'entraîner au QCM  ", "📖  Fiches de révision  "])

    with tab_quiz:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("#### ⚡ Lancer un quiz")
            cat_options  = ["Toutes les catégories"] + [c["nom"] for c in categories]
            cat_choisie  = st.selectbox("Catégorie :", cat_options, key="cat_select")
            nb_max       = len(toutes_questions)
            nb_questions = st.slider("Nombre de questions :", 5, nb_max, min(15, nb_max), 5)
            melanger     = st.checkbox("🔀 Mélanger", value=True)
            if st.button("▶️ Commencer !", use_container_width=True):
                pool = toutes_questions if cat_choisie == "Toutes les catégories" \
                       else [q for q in toutes_questions if q["categorie"] == cat_choisie]
                if melanger:
                    random.shuffle(pool)
                start_quiz(pool[:nb_questions], melanger=melanger)
                st.rerun()
        with col2:
            st.markdown("#### 📚 Contenu")
            st.markdown(f"**Total :** {len(toutes_questions)} questions")
            for cat in categories:
                st.markdown(f"- {cat['nom']} : **{len(cat['questions'])}** questions")
            histo = st.session_state.historique.get(key, [])
            if histo:
                st.markdown("---")
                st.markdown("**Mes sessions :**")
                for i, h in enumerate(reversed(histo[-5:])):
                    badge, _ = get_badge(h["pct"])
                    st.markdown(f"Session {len(histo)-i} : **{h['score']}/{h['total']}** ({h['pct']}%) {badge}")

        st.markdown("---")
        st.markdown("#### 🎯 Quiz par catégorie")
        cols = st.columns(3)
        for i, cat in enumerate(categories):
            with cols[i % 3]:
                if st.button(f"📖 {cat['nom']}", key=f"cat_quiz_{i}", use_container_width=True):
                    pool = [q for q in toutes_questions if q["categorie"] == cat["nom"]]
                    start_quiz(pool)
                    st.rerun()

    with tab_fiches:
        if not fiches:
            st.info("Aucune fiche de révision disponible pour cette matière.")
        else:
            cat_names = list(fiches.keys())
            st.markdown("### 📖 Fiches de révision par thème")
            st.markdown("Clique sur un thème pour lire le résumé de cours, puis lance le QCM associé !")
            st.markdown("")

            cols = st.columns(3)
            for i, cat_nom in enumerate(cat_names):
                cat_data = fiches[cat_nom]
                emoji    = cat_data.get("emoji", "📄")
                with cols[i % 3]:
                    is_selected = st.session_state.fiche_cat == cat_nom
                    prefix = "▶ " if is_selected else ""
                    if st.button(f"{prefix}{emoji} {cat_nom}", key=f"fiche_btn_{i}", use_container_width=True):
                        st.session_state.fiche_cat = None if is_selected else cat_nom
                        st.rerun()

            st.markdown("---")

            if st.session_state.fiche_cat and st.session_state.fiche_cat in fiches:
                cat_nom  = st.session_state.fiche_cat
                cat_data = fiches[cat_nom]
                render_fiche(cat_nom, cat_data)
                st.markdown("---")
                pool = [q for q in toutes_questions if q["categorie"] == cat_nom]
                if pool:
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.markdown(f"**{len(pool)} question(s)** disponibles sur ce thème")
                    with col_b:
                        if st.button(f"🎯 QCM – {cat_nom}", use_container_width=True):
                            start_quiz(pool)
                            st.rerun()
            else:
                st.markdown(
                    '<div style="color:#475569;text-align:center;padding:40px;font-size:1rem">'
                    '👆 Clique sur un thème ci-dessus pour afficher sa fiche de révision'
                    '</div>',
                    unsafe_allow_html=True,
                )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE : QUIZ
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.mode == "quiz":
    key       = st.session_state.subject_key
    questions = st.session_state.questions_session
    idx       = st.session_state.index

    if idx >= len(questions):
        save_session_once()
        score = st.session_state.score
        total = len(questions)
        pct   = int(score / total * 100) if total else 0
        badge_txt, badge_cls = get_badge(pct)

        st.markdown(f'<p class="breadcrumb">🏠 Menu › <span>{key}</span> › Résultats</p>', unsafe_allow_html=True)
        st.markdown('<div class="score-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="score-number">{score} / {total}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{badge_cls}">{badge_txt}</div>', unsafe_allow_html=True)
        st.markdown(f'**{pct}% de bonnes réponses**')
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📋 Récapitulatif")
        for i, q in enumerate(questions):
            rep_u  = st.session_state.reponses_utilisateur.get(i)
            bonnes = [r["texte"] for r in q["reponses"] if r["correct"]]
            icon   = "✅" if rep_u in bonnes else "❌"
            with st.expander(f"{icon} Q{i+1} : {q['question'][:80]}..."):
                st.markdown(f"**Ta réponse :** {rep_u or '—'}")
                st.markdown(f"**Bonne(s) réponse(s) :** {', '.join(bonnes)}")
                if "explication" in q:
                    st.markdown(f"💡 {q['explication']}")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔁 Rejouer", use_container_width=True):
                start_quiz(questions, melanger=True)
                st.rerun()
        with c2:
            if st.button("📚 Retour accueil matière", use_container_width=True):
                st.session_state.mode = "accueil"
                st.rerun()
        with c3:
            if st.button("🏠 Menu principal", use_container_width=True):
                st.session_state.mode = "menu"
                st.rerun()

    else:
        q     = questions[idx]
        total = len(questions)

        st.markdown(f'<p class="breadcrumb">🏠 Menu › <span>{key}</span> › Question {idx+1}/{total}</p>', unsafe_allow_html=True)
        st.progress(idx / total)
        st.markdown(f'<p class="progress-text">Question {idx+1} sur {total} · Score : {st.session_state.score}</p>', unsafe_allow_html=True)

        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.markdown(f'<span class="cat-badge">📂 {q["categorie"]}</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text">❓ {q["question"]}</div>', unsafe_allow_html=True)

        reponses = q["reponses"]
        labels   = [f"{chr(65+i)}. {r['texte']}" for i, r in enumerate(reponses)]

        if not st.session_state.repondu:
            choix = st.radio("Choisis ta réponse :", labels, key=f"radio_{idx}", index=None)
            st.session_state.choix_courant = choix
            if st.button("✅ Valider", disabled=(choix is None)):
                texte_choisi = choix[3:]
                bonnes = [r["texte"] for r in reponses if r["correct"]]
                st.session_state.reponses_utilisateur[idx] = texte_choisi
                if texte_choisi in bonnes:
                    st.session_state.score += 1
                st.session_state.repondu = True
                st.rerun()
        else:
            texte_choisi = st.session_state.reponses_utilisateur.get(idx, "")
            bonnes = [r["texte"] for r in reponses if r["correct"]]

            for i, r in enumerate(reponses):
                label = f"{chr(65+i)}. {r['texte']}"
                if r["texte"] in bonnes:
                    st.markdown(f'<div class="correct-answer">✅ {label}</div>', unsafe_allow_html=True)
                elif r["texte"] == texte_choisi:
                    st.markdown(f'<div class="wrong-answer">❌ {label} (ta réponse)</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="neutral-answer">{label}</div>', unsafe_allow_html=True)

            if texte_choisi in bonnes:
                st.success("🎉 Bonne réponse !")
            else:
                st.error(f"❌ La bonne réponse : **{bonnes[0]}**")

            if "explication" in q:
                st.markdown(
                    f'<div class="explication-box">💡 <strong>Explication :</strong> {q["explication"]}</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("")
            col_next, col_fiche = st.columns([2, 1])
            with col_next:
                if st.button("⏭️ Question suivante →", use_container_width=True):
                    st.session_state.index  += 1
                    st.session_state.repondu = False
                    st.session_state.choix_courant = None
                    st.rerun()
            with col_fiche:
                if st.button("📖 Voir la fiche", use_container_width=True):
                    st.session_state.fiche_cat = q.get("categorie", "")
                    st.session_state.mode = "fiche_rapide"
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE : FICHE RAPIDE (depuis le quiz)
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.mode == "fiche_rapide":
    key     = st.session_state.subject_key
    cat_nom = st.session_state.fiche_cat

    try:
        cours_data = load_cours()
        fiches = cours_data.get(key, {})
    except Exception:
        fiches = {}

    st.markdown(
        f'<p class="breadcrumb">🏠 Menu › <span>{key}</span> › Quiz › <span>Fiche : {cat_nom}</span></p>',
        unsafe_allow_html=True,
    )

    if cat_nom and cat_nom in fiches:
        render_fiche(cat_nom, fiches[cat_nom])
    else:
        st.warning("Fiche non disponible pour cette catégorie.")

    st.markdown("---")
    if st.button("⬅️ Retour au quiz", use_container_width=False):
        st.session_state.mode = "quiz"
        st.rerun()