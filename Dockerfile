FROM selenium/standalone-firefox:latest

USER root

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copier tout le code (hors requirements pour éviter rebuild sur chaque code modif)
COPY . /app

# Laisse le choix à l'utilisateur Pterodactyl de la commande de démarrage (ex: python3 script.py)
CMD ["/entrypoint.sh"]
