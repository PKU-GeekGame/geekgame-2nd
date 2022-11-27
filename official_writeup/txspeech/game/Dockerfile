FROM python:3

RUN apt-get update && apt-get install -y ffmpeg

# install python requirements

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# copy src

COPY recog.py ./
COPY templates/ ./templates/
COPY game.py ./

CMD ["uwsgi", "--http", ":5000", "--wsgi-file", "game.py", "--callable", "app", "--master", "--processes", "1", "--threads", "1"]
EXPOSE 5000