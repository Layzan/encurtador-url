# Use a imagem oficial do Python como base
FROM python:3.12-slim-bookworm

# Setando o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos de dependências para dentro do container
COPY requirements.txt .

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia a pasta 'static/' para o container
COPY static /app/static

# Copia o restante dos arquivos do projeto (incluindo o código do FastAPI)
COPY app /app/app

# Expõe a porta que o FastAPI vai usar (padrão: 8000)
EXPOSE 8000

# Comando para rodar a aplicação FastAPI com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
