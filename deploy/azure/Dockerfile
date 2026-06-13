FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860 \
    MODEL_PATH=models/gesture-cnn-baseline-s05-partial.keras \
    MODEL_TYPE=cnn \
    MODEL_VERSION=cnn-s05-partial-v1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates libglib2.0-0 libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY deploy/huggingface/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY common ./common
COPY cloud ./cloud

RUN mkdir -p models \
    && python - <<'PY'
from pathlib import Path
from urllib.request import urlretrieve

url = "https://huggingface.co/spaces/anroiy/iot-ck-gesture-api/resolve/main/models/gesture-cnn-baseline-s05-partial.keras"
target = Path("models/gesture-cnn-baseline-s05-partial.keras")
urlretrieve(url, target)
if target.stat().st_size < 1_000_000:
    raise RuntimeError(f"Downloaded model is unexpectedly small: {target.stat().st_size} bytes")
PY

EXPOSE 7860

CMD ["sh", "-c", "uvicorn cloud.app:app --host 0.0.0.0 --port ${PORT}"]
