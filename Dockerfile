FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PYTHONUNBUFFERED=1
ENV INPUT_DIR=data/input
ENV OUTPUT_DIR=data/output

CMD ["python", "-m", "app.pipeline.cli", "--input-dir", "data/input", "--output-dir", "data/output"]