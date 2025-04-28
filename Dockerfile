FROM selenium/standalone-firefox:latest

USER root

WORKDIR /app

COPY app/requirements* ./

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY app/* ./

ENV MODE=EMARGEMENT

CMD ["python3", "-u", "script.py"]