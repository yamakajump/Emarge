FROM selenium/standalone-firefox:latest

USER root
WORKDIR /home/container

# Copie requirements & entrypoint
COPY ./requirements.txt /home/container/requirements.txt
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copie le code de l'app (optionnel)
COPY . /home/container

# Laisses Pterodactyl gérer la commande grâce à entrypoint.sh
CMD ["/bin/bash", "/entrypoint.sh"]
