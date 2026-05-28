from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Serviço de Multiplicação")

class OperacaoRequest(BaseModel):
    num1: float
    num2: float

@app.post("/multiplicacao")
def multiplicar(dados: OperacaoRequest):
    resultado = dados.num1 * dados.num2
    return {"resultado": resultado, "servico": "multiplicacao"}