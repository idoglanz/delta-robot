FROM python:3.8-slim-buster
RUN apt-get update
RUN apt-get install nano
 
RUN mkdir wd
WORKDIR /wd
COPY requirements.txt .
RUN pip3 install -r requirements.txt
  
COPY app/ ./
RUN mkdir gcode

CMD [ "gunicorn", "--workers=1", "--threads=1", "-b 0.0.0.0:8050", "app:server"]