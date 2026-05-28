from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Serviço de Divisão")

class OperacaoRequest(BaseModel):
    num1: float
    num2: float

@app.post("/divisao")
def dividir(dados: OperacaoRequest):
    if dados.num2 == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro matemático: Não é possível dividir por zero."
        )
    resultado = dados.num1 / dados.num2
    return {"resultado": resultado, "servico": "divisao"}