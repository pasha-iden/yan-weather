FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY tools/ ./tools/
COPY handlers/ ./handlers/
COPY cron/ ./cron/
COPY fonts/ ./fonts/

EXPOSE 8000

CMD ["python", "main.py"]