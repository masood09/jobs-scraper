FROM python:3.14

WORKDIR /app

COPY requirements/requirements.base.txt requirements.base.txt
COPY requirements/requirements.prod.txt requirements.prod.txt

RUN pip3 install -r requirements.prod.txt

COPY . .

CMD [ "python3", "scripts/run.py" , "prod"]
