FROM python:3.14

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]