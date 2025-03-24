FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE=1

RUN pip3 install pika
RUN pip3 install faker

COPY . .


CMD ["python3", "-u", "./producer.py"]