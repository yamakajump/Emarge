FROM selenium/standalone-firefox:latest

WORKDIR /app

COPY app/* ./

RUN sudo pip install --no-cache-dir -r requirements.txt --break-system-packages

CMD ["sudo", "--preserve-env=Us,Pa,TZ,ANNEE,TP,SEMESTRE", "bash", "-c", "python3 -u script.py"]
