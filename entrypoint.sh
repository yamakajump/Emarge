#!/bin/bash
set -e

cd /home/container

# Remplace les {{VAR}} par ${VAR} dans STARTUP pour compatibilité
STARTUP_PROCESSED=$(echo "${STARTUP}" | sed -e 's/{{/${/g' -e 's/}}/}/g')
echo "Starting bot with command: ${STARTUP_PROCESSED}"

# Exécute la commande demandée par la plateforme
eval "${STARTUP_PROCESSED}"
