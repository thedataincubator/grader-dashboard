FROM ubuntu:18.04

RUN apt-get update && apt-get -y install python3-pip -y
RUN pip3 install --upgrade pip

ADD ./requirements.txt /tmp/requirements.txt

RUN pip3 install -qr /tmp/requirements.txt --no-cache-dir

ADD ./graderdashboard /app/graderdashboard/
ADD ./app.py ./wsgi.py ./grades.db  /app/

WORKDIR /app

ENV DB_URI=sqlite:////app/grades.db

CMD gunicorn --bind 0.0.0.0:5000 wsgi
  