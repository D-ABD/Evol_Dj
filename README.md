# Evol_Dj
# 📘 MyEvol

**MyEvol** est une application web Django de développement personnel. Elle permet de suivre son humeur au quotidien, définir des objectifs, débloquer des badges de progression et visualiser ses statistiques sous forme de graphiques.

---

## 🚀 Fonctionnalités principales

- ✍️ Écriture d’entrées de **journal** avec humeur et catégorie
- 🎯 Suivi des **objectifs personnels**
- 📊 Visualisation de **statistiques** (humeur, objectifs, catégories)
- 🏅 **Badges** de progression et niveaux à débloquer
- 🔔 **Notifications** automatiques lors du déblocage d’un badge
- 📈 Graphiques (Chart.js) intégrés au dashboard
- 👤 Authentification utilisateur (inscription, connexion, déconnexion)

---

## 🛠️ Tech Stack

- **Backend** : Django 4.2
- **Base de données** : SQLite (ou PostgreSQL)
- **Frontend** : HTML + Bootstrap 5 + Chart.js
- **Auth** : Django User Model personnalisé

---

## 📸 Aperçus

> _Exemples d’écrans à venir_  
> Tu peux ajouter ici des screenshots de ton dashboard, journal, ou badges.

---

## 📂 Structure du projet

Myevol_project/ ├── Myevol_app/ │ ├── models.py │ ├── views.py │ ├── forms.py │ ├── urls.py │ ├── templates/myevol/ │ ├── static/ │ └── utils/ ├── templates/base.html ├── manage.py └── requirements.txt


---

## ⚙️ Installation locale

Cloner le projet :
    git clone https://github.com/ton-user/my-evol.git
    cd my-evol

Activer environnement virtuel : 
    python3 -m venv env
    source env/bin/activate  # sous Linux/Mac
    env\Scripts\activate     # sous Windows


Installer les dépendances :
    pip install -r requirements.txt

Appliquer les migrations :
    python3 manage.py makemigrations
    python3 manage.py migrate

Lancer le serveur :    
    python3 manage.py runserver

Créer un super utilisateur (admin) :
    python3 manage.py createsuperuser

✅ TODO (roadmap)
    Journal quotidien
    Objectifs personnels
    Notifications et badges
    Dashboard avec stats et graphiques
    Export PDF / Excel
    Version mobile
    PWA ou version native via React Native 

🧠 Auteur
    Développé avec ❤️ par @Adserv    # Evol_Dj
# Evol_Dj
