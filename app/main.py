from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from .database import urls_collection, is_db_connected
from .models import URL
from .schemas import URLResponse
from pathlib import Path

description = """
Este é um serviço simples de encurtamento de URL desenvolvido com FastAPI.\n\r
O sistema permite que você envie uma URL original e receba uma URL encurtada.

## URLs

Você será capaz de:

- **Shorten Url** (_Gera uma URL mais curta a partir de uma URL longa._)
- **Redirect Url** (_Redireciona para a URL original a partir de uma URL curta._)

**Fluxo:**
1. Envie uma URL original para o endpoint `/shorten/`.
2. Receba uma URL curta gerada automaticamente.
3. Use a URL curta no endpoint `/short_url` para redirecionar à URL original.

## Banco

**Você poderá consultar o status do banco de dados.**

- O endpoint `/healthcheck/db` retorna o estado de conexão com o banco de dados MongoDB.
- Em caso de falha na conexão, a API irá retornar um erro detalhado.

### Página Estática

Para acessar a página estática do encurtador de URL (frontend), você pode consultar o seguinte link: 

[Página Estática do Encurtador de URL](http://127.0.0.1:8000/front/index.html)

"""

app = FastAPI(
    title="Encurtador de URL",
    version="0.0.1",
    description=description
)

# Função para criar uma URL curta
def generate_short_url() -> str:
    return str(uuid4())[:8]  # Gerar uma string curta de 8 caracteres

# Rota para encurtar uma URL
@app.post("/shorten/", tags=["URL"], response_model=URLResponse)
async def shorten_url(url: URL):
    # Verificar se a URL já foi encurtada
    existing_url = urls_collection.find_one({"original_url": url.original_url})
    if existing_url:
        return URLResponse(original_url=existing_url["original_url"], short_url=existing_url["short_url"])
    
    # Gerar uma URL curta e salvar no MongoDB
    short_url = generate_short_url()
    urls_collection.insert_one({"original_url": url.original_url, "short_url": short_url})
    
    return URLResponse(original_url=url.original_url, short_url=short_url)

# Rota para redirecionar para a URL original
@app.get("/{short_url}", tags=["URL"])
async def redirect_url(short_url: str):
    # Procurar no banco pela URL curta
    url_data = urls_collection.find_one({"short_url": short_url})
    
    if not url_data:
        raise HTTPException(status_code=404, detail="URL não encontrada")
    
    # Redirecionar para a URL original
    return {"redirect_url": url_data["original_url"]}

# Rota para verificar a conexão com o banco de dados
@app.get("/healthcheck/db", tags=["Banco"])
async def healthcheck_db():
    if is_db_connected():
        return {"status": "OK", "message": "Banco de dados conectado com sucesso."}
    else:
        raise HTTPException(status_code=500, detail="Falha na conexão com o banco de dados.")
    
# Servindo arquivos estáticos da pasta 'static'
app.mount("/front", StaticFiles(directory=Path(__file__).parent.parent / "static"), name="static")

