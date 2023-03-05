FROM python:3.11

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src src

EXPOSE 8000

CMD [ "uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0" ]
