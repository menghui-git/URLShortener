FROM python:3.8.3
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y vim

COPY . .
RUN ["chmod", "+x", "/usr/src/app/django-entrypoint.sh"]
ENTRYPOINT ["sh", "/usr/src/app/django-entrypoint.sh"]

