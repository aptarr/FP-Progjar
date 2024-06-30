FROM python:3.11-alpine

WORKDIR /app

COPY . .

EXPOSE 8889

CMD ["python3", "server.py"]