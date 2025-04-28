#!/bin/sh
set -e

cd /app
# Installe les dépendances à chaque démarrage (seulement si requirements.txt différent déjà installé)
pip install --no-cache-dir --break-system-packages -r requirements.txt

# Lancer le script Python par défaut, change ici si besoin :
exec python3 -u script.py
