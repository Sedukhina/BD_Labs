FROM python:latest

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

CMD ["python", "-u", "app.py"]
#CMD ["python", "-u", "main_query.py"]
