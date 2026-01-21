FROM debian:latest

ARG DEBIAN_FRONTEND=noninteractive

# Définir la variable HOME pour l'utilisateur non-root
ENV HOME=/home/container
ENV TZ=Europe/Paris

# S'assurer d'être en root pour l'installation des paquets système
USER root

# Installation des dépendances de base
RUN apt-get update && \
    apt-get install -y \
      curl \
      git \
      gnupg \
      jq \
      less \
      python3-pip \
      tree \
      unzip \
      vim \
      wget \
    && rm -rf /var/lib/apt/lists/*

# Installation de Google Chrome
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-key.gpg

RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list

RUN apt-get update && apt-get install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*

# Installation de ChromeDriver
RUN CHROME_VERSION="$(google-chrome --product-version)" && \
    wget -q --continue -P /tmp/ "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip -q /tmp/chromedriver-linux64.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver-linux64.zip /tmp/chromedriver-linux64

WORKDIR /home/container

# Copie requirements & entrypoint
COPY ./requirements.txt .
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copie tout ton code
COPY . .

# Crée l'utilisateur "container" et lui donne un home dédié
RUN useradd -m -d /home/container container

# Change les ownership sur le dossier de travail pour l'utilisateur "container"
RUN chown -R container:container /home/container

# Passe sur l'utilisateur restreint
USER container

ENV MODE=EMARGEMENT

# Par défaut, laisse Pterodactyl gérer l'entrée grâce à entrypoint.sh
CMD ["/bin/bash", "/entrypoint.sh"]
