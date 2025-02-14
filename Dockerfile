FROM selenium/standalone-firefox:latest

WORKDIR /app

COPY app/* .

RUN sudo pip install --no-cache-dir -r requirements.txt --break-system-packages

CMD ["sudo", "python3", "script.py"]
