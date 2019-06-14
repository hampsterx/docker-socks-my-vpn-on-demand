FROM python:3.7-slim

RUN apt-get update && apt-get install -y ssh openvpn iputils-ping net-tools gcc


ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

RUN mkdir /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt
COPY oscm /app/oscm/
COPY static /app/static/

COPY main.py /app/main.py

EXPOSE 8080


WORKDIR /app

CMD ["python", "/app/main.py"]

ENV docker "true"

STOPSIGNAL SIGHUP