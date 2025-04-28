FROM selenium/standalone-firefox:latest

# Crée l'utilisateur "container" et lui donne un home dédié
RUN useradd -m -d /home/container container

USER root
WORKDIR /home/container

# Copie requirements & entrypoint
COPY ./requirements.txt .
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copie tout ton code (optionnel)
COPY . .

# Change les ownership sur le dossier de travail pour l'utilisateur "container"
RUN chown -R container:container /home/container

# Passe sur l’utilisateur restreint
USER container

# Par défaut, laisse Pterodactyl gérer l’entrée grâce à entrypoint.sh
CMD ["/bin/bash", "/entrypoint.sh"]
