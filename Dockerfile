FROM selenium/standalone-firefox:latest

USER root

WORKDIR /app

COPY ./requirements* ./

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY ./* ./

ENV MODE=EMARGEMENT

CMD ["python3", "-u", "script.py"]