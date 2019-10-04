FROM python:3.7-alpine

WORKDIR /code
COPY . .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 5555
