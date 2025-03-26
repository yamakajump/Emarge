FROM selenium/standalone-firefox:latest AS emargement

USER root

WORKDIR /app

COPY app/requirements* ./

RUN pip install --no-cache-dir -r requirements.txt -r requirements-selenium.txt --break-system-packages

COPY app/* ./

ENV MODE=EMARGEMENT

CMD ["python3", "-u", "script.py"]



FROM python:3 AS notification

WORKDIR /app

COPY app/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app/* ./

ENV MODE=NOTIFICATION

CMD ["python3", "-u", "script.py"]
