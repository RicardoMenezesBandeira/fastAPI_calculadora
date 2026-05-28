from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import httpx

app = FastAPI(
    title="API Gateway - Calculadora de Microsserviços",
    description="Porta de entrada para gerenciar as operações matemáticas.",
    version="1.0.0"
)

# Mapeamento de onde cada microsserviço está rodando dentro da rede do Docker
# Usamos o nome do serviço definido no docker-compose.yml como "hostname"
SERVICOS_URL = {
    "soma": "http://soma:8001/soma",
    "subtracao": "http://subtracao:8002/subtracao",
    "multiplicacao": "http://multiplicacao:8003/multiplicacao",
    "divisao": "http://divisao:8004/divisao"
}

# Modelo de dados que o Gateway espera receber do usuário
class RequisicaoCalculo(BaseModel):
    num1: float
    num2: float
    operacao: str  # Deve ser: 'soma', 'subtracao', 'multiplicacao' ou 'divisao'

@app.post("/calcular")
async def calcular(dados: RequisicaoCalculo):
    # 1. Padroniza o nome da operação para evitar problemas com letras maiúsculas
    operacao_limpa = dados.operacao.lower().strip()
    
    # 2. Valida se a operação enviada é suportada pelo sistema
    if operacao_limpa not in SERVICOS_URL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operação '{dados.operacao}' inválida. Use: soma, subtracao, multiplicacao ou divisao."
        )
    
    # 3. Descobre a URL do microsserviço responsável
    url_microsservico = SERVICOS_URL[operacao_limpa]
    
    # Dados que serão repassados para o microsserviço
    payload = {
        "num1": dados.num1,
        "num2": dados.num2
    }
    
    # 4. Faz a chamada HTTP assíncrona para o microsserviço correspondente
    async with httpx.AsyncClient() as client:
        try:
            resposta = await client.post(url_microsservico, json=payload, timeout=5.0)
            
            # Se o microsserviço retornar um erro (ex: divisão por zero), o Gateway repassa o erro
            if resposta.status_code != 200:
                detalhe_erro = resposta.json().get("detail", "Erro no microsserviço.")
                raise HTTPException(status_code=resposta.status_code, detail=detalhe_erro)
                
            return resposta.json()
            
        except httpx.RequestError:
            # Caso o microsserviço esteja fora do ar ou inacessível
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"O serviço de {operacao_limpa} está indisponível no momento."
            )