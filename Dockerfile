FROM python:3.10-slim-buster

WORKDIR /myportfolio 

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

EXPOSE 5000