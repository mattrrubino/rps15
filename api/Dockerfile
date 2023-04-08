FROM python:3.11

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src src

EXPOSE 8000

CMD [ "python", "src/main.py" ]
