FROM python:3.10-slim

WORKDIR /app

# Copia e instala as dependências antes para aproveitar o cache de camadas do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# A porta varia de acordo com o serviço (8001 a 8004)
# Exemplo genérico: substituído dinamicamente pelo docker-compose
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]