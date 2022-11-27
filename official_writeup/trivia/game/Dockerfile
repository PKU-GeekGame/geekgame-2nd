FROM python:3

# install python requirements

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# copy src

COPY data.py ./
COPY game.py ./

CMD ["python", "game.py"]