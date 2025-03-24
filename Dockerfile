FROM selenium/standalone-firefox:latest AS emargement

WORKDIR /app

COPY app/requirements* ./

RUN sudo pip install --no-cache-dir -r requirements.txt --break-system-packages

RUN sudo pip install --no-cache-dir -r requirements-selenium.txt --break-system-packages

COPY app/* ./

ENV MODE=EMARGEMENT

CMD ["sudo", "--preserve-env=Us,Pa,TZ,ANNEE,TP,FORMATION,blacklist,TOPIC,MODE", "bash", "-c", "python3 -u script.py"]

FROM python:3 AS notification

WORKDIR /app

COPY app/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app/* ./

ENV MODE=NOTIFICATION

CMD ["python3", "-u", "script.py"]
