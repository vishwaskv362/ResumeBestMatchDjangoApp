FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 81

CMD ["python", "manage.py", "runserver", "0.0.0.0:81"]