# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Instala dependências básicas e o Poetry
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir poetry

# Copia os arquivos do Poetry
COPY pyproject.toml poetry.lock ./

# Instala dependências no sistema global (sem venv isolado)
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Copia o restante da aplicação
COPY . .

# Expõe a porta da API
EXPOSE 8000

# Comando para rodar a API
CMD ["bash", "-c", "python -m scripts.indexer && uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload"]
