FROM python:3
EXPOSE 8002

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH /app/src
