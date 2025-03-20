FROM selenium/standalone-firefox:latest

WORKDIR /app

COPY app/requirements.txt ./

RUN sudo pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY app/* ./

CMD ["sudo", "--preserve-env=Us,Pa,TZ,ANNEE,TP,FORMATION,blacklist,TOPIC", "bash", "-c", "python3 -u script.py"]
