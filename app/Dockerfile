FROM python:latest

WORKDIR /app

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY "main.py" .
COPY 'Odata2019File.csv' .
COPY 'Odata2020File.csv' .
COPY 'Odata2021File.csv' .

CMD ["python", "-u", "main.py"]
