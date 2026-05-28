from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Serviço de Soma")

class OperacaoRequest(BaseModel):
    num1: float
    num2: float

@app.post("/soma")
def somar(dados: OperacaoRequest):
    resultado = dados.num1 + dados.num2
    return {"resultado": resultado, "servico": "soma"}