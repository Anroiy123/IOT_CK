FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860 \
    MODEL_PATH=models/gesture-cnn-baseline-s05-partial.keras \
    MODEL_TYPE=cnn \
    MODEL_VERSION=cnn-s05-partial-v1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libglib2.0-0 libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY deploy/huggingface/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY common ./common
COPY cloud ./cloud
COPY models/gesture-cnn-baseline-s05-partial.keras ./models/gesture-cnn-baseline-s05-partial.keras

EXPOSE 7860

CMD ["sh", "-c", "uvicorn cloud.app:app --host 0.0.0.0 --port ${PORT}"]
