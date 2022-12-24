FROM python:3.7-slim 
LABEL maintainer="sgl@pdx.edu"

RUN apt-get update && apt-get install -y python3-pip
COPY . /app 
WORKDIR /app 
RUN pip install -r requirements.txt 

CMD gunicorn --bind :$PORT --workers 1 --threads 8 app:app
