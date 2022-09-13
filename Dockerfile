FROM tiangolo/meinheld-gunicorn:python3.8

COPY requirements.txt .
RUN pip3 install -r requirements.txt

LABEL com.centurylinklabs.watchtower.enable="true"

COPY main.py /app
COPY website /app/website

EXPOSE 80
