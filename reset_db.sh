#!/bin/bash

# Variables
DB_NAME="myevol"
DB_USER="ABD"
DB_HOST="localhost"

echo "🚀 Suppression de la base $DB_NAME..."
psql -U $DB_USER -h $DB_HOST -c "DROP DATABASE IF EXISTS $DB_NAME;"

echo "🛠 Création d'une nouvelle base $DB_NAME..."
psql -U $DB_USER -h $DB_HOST -c "CREATE DATABASE $DB_NAME;"

echo "⚙️ Application des migrations..."
python manage.py migrate

echo "👑 Création du superutilisateur Django..."
python manage.py createsuperuser

echo "✅ Base $DB_NAME prête à être utilisée !"
