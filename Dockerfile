FROM python:3.11-slim

WORKDIR /app

COPY sandbox_server.py .

RUN pip install flask

EXPOSE 8000

CMD ["python", "sandbox_server.py"]
