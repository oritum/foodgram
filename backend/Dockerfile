FROM python:3.9-slim

WORKDIR /app

COPY requirements/requirements*.txt .

ARG ENV=production

RUN pip install --upgrade pip 

RUN pip install -r requirements_${ENV}.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "foodgram_backend.wsgi"]