from pydantic import BaseModel
from typing import Optional, List
from model.treino import Treino



class TreinoSchema(BaseModel):
    """ Define como um novo treino a ser inserido deve ser representado
    """
    nome: str = "Agachamento"
    quantidade: Optional[int] = 10


class TreinoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do treino.
    """
    produto_id: int = 1


class ListagemTreinosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    treinos:List[TreinoSchema]


def apresenta_treinos(treinos: List[Treino]):
    """ Retorna uma representação do treino seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for treino in treinos:
        result.append({
            "nome": treino.nome,
            "quantidade": treino.quantidade,
            "valor": treino.valor,
        })

    return {"treinos": result}


class TreinoViewSchema(BaseModel):
    """ Define como um treino será retornado: treino + quantidade.
    """
    id: int = 1
    nome: str = "Agachamento2"
    quantidade: Optional[int] = 15


class TreinoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_treino(treino: Treino):
    """ Retorna uma representação do treino seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": treino.id,
        "nome": treino.nome,
        "quantidade": treino.quantidade,
    }
