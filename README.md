# 🎓 QCM – Révisions UTBM

Application web de révision interactive pour les étudiants de l'UTBM, construite avec **Streamlit**.
Elle propose des QCM par matière et par thème, avec des fiches de révision intégrées.

---

## Matières disponibles

| Matière | Intitulé | Thèmes | Questions | Année | Semestre |
|---------|----------|--------|-----------|-------|----------|
| 🖥️ **SR72** | Architecture des Systèmes d'Exploitation | Synchronisation, Sémaphores, Moniteurs, Interblocages, Algorithme du Banquier | ~40 | A1 | S2 |
| 📋 **GE79** | Management de Projet | RH, Conflits, Leadership, Communication, Procurement, Risques, Qualité, Organisation matricielle | ~43 | A1 | S2 |
| 💾 **BD71** | Big Data & NoSQL | Fondamentaux, HDFS, MapReduce, NoSQL, CAP, Architecture, Frameworks (Spark, Flink, YARN…) | ~48 | A1 | S2 |
| 🎤 **TI73** | Communication Professionnelle | PowerPoint, Prise de parole, Réunion, Brainstorming, Design de diaporama | ~29 | A1 | S2 |

---

## Installation et lancement

### Prérequis

- Python 3.8+
- pip
- cloner le répertoire git

### Installation

```bash
# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# Installer les dépendances
pip install streamlit
```

### Lancement

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans le navigateur à l'adresse `http://localhost:8501`.

---

## 📁 Structure du projet

```
FISA-INFO-QCM/
│
├── app.py                  # Application principale Streamlit
│
├── questions_sr72.json     # Questions QCM – SR72
├── questions_ge79.json     # Questions QCM – GE79
├── questions_bd71.json     # Questions QCM – BD71
├── questions_ti73.json     # Questions QCM – TI73
│
└── cours.json              # Fiches de révision
```

> ⚠️ Tous les fichiers doivent être dans le **même dossier** que `app.py`.

---

## Fonctionnalités

### 📝 Mode QCM
- Sélection de la matière, de la catégorie et du nombre de questions
- Mélange aléatoire des questions et des réponses
- Validation avec correction immédiate et explication détaillée
- Bouton **"Voir la fiche"** en cas d'erreur pour réviser le thème en cours
- Récapitulatif complet en fin de session avec badge de performance

### 📖 Fiches de révision
- Accessibles depuis l'onglet **"Fiches de révision"** de chaque matière
- Organisées par thème avec : introduction, sections détaillées, encadré "💡 À retenir"
- Bouton de lancement direct du QCM associé à chaque fiche

### 📊 Historique
- Suivi des 5 dernières sessions par matière
- Score, total et pourcentage affichés dans la sidebar

### Badges de performance
| Score | Badge |
|-------|-------|
| ≥ 80% | 🏆 Excellent ! |
| ≥ 60% | 👍 Bien joué ! |
| < 60% | 📚 À retravailler |

---

## Format des fichiers JSON

### `questions_xxx.json`

```json
{
  "titre": "NOM – Intitulé complet",
  "categories": [
    {
      "nom": "Nom de la catégorie",
      "questions": [
        {
          "question": "Texte de la question ?",
          "reponses": [
            {"texte": "Bonne réponse", "correct": true},
            {"texte": "Mauvaise réponse", "correct": false}
          ],
          "explication": "Explication affichée après validation."
        }
      ]
    }
  ]
}
```

### `cours.json`

```json
{
  "CODE_MATIERE": {
    "Nom de la catégorie": {
      "emoji": "📖",
      "intro": "Introduction de la fiche.",
      "sections": [
        {
          "titre": "Titre de section",
          "contenu": [
            "**Point clé 1** : description",
            "**Point clé 2** : description"
          ]
        }
      ],
      "a_retenir": "Résumé essentiel à mémoriser."
    }
  }
}
```

> Le markdown (`**gras**`, `*italique*`, `` `code` ``) est supporté dans les fiches.

---

## ➕ Ajouter une nouvelle matière

1. **Créer** le fichier `questions_xx99.json` en suivant le format ci-dessus
2. **Ajouter** les fiches dans `cours.json` sous la clé `"XX99"`
3. **Déclarer** la matière dans `app.py` dans le dictionnaire `SUBJECTS` :

```python
SUBJECTS = {
    ...
    "XX99": {
        "file": "questions_xx99.json",
        "icon": "🔬",
        "label": "XX99",
        "subtitle": "Intitulé complet",
        "description": "Thème 1, Thème 2, Thème 3",
        "color": "#34d399",
    },
}
```

---

## Technologies utilisées

- **[Streamlit](https://streamlit.io/)** — framework web Python pour applications de données
- **JSON** — stockage des questions et fiches de révision
- **CSS personnalisé** — thème sombre, animations, mise en page responsive