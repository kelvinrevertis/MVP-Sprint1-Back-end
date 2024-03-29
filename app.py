from flask import Flask, redirect, request, make_response, jsonify
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Treino, BMIData
from logger import logger
from schemas import *

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
treino_tag = Tag(name="Treino", description="Adição, visualização e remoção de produtos à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.route('/treinos', methods=['POST'])
def post_treinos():

    data = request.get_json()
    nome = data.get("nome")
    quantidade = data.get("quantidade")

    try:
        session = Session()

        treino = session.query(Treino).filter_by(nome=nome).first()

        if treino:
            treino.quantidade += quantidade
        else:
            treino = Treino(nome=nome, quantidade=quantidade)
            session.add(treino)

        session.commit()

        treino_dict = {"nome": treino.nome, "quantidade": treino.quantidade}
        response_json = jsonify(treino_dict)

        response = make_response(response_json, 200)

        print("Salvo treino:", treino_dict)

    except Exception as e:

        error = {"msg": "Não foi possível salvar novo item :/"}

        response_json = jsonify(error)

        response = make_response(response_json, 400,)

    # retornando resposta
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/treinos', methods=['GET'])
def get_treinos():

    session = Session()
    treinos = session.query(Treino).all()

    if not treinos:
        treinos_list = []
    else:
        treinos_list = [{"id":treino.id,"nome": treino.nome, "quantidade": treino.quantidade} for treino in treinos]

    return jsonify(treinos_list)


@app.route('/treinos/<int:id>', methods=['PUT'])
def edit_treinos(id):
    session = Session()
    treino = session.query(Treino).filter_by(id=id).first()

    if not treino:
        return make_response(jsonify({'msg': 'Treino não encontrado.'}), 404)

    try:
        edited_treino = request.get_json()
        treino.nome = edited_treino.get('nome', treino.nome)
        treino.quantidade = edited_treino.get('quantidade', treino.quantidade)

        session.add(treino)
        session.commit()

        treino_dict = {"id": treino.id, "nome": treino.nome, "quantidade": treino.quantidade}
        response_json = jsonify(treino_dict)

        response = make_response(response_json, 200)

        print("Editado treino:", treino_dict)

    except Exception as e:

        error = {"msg": "Não foi possível editar o item."}

        response_json = jsonify(error)

        response = make_response(response_json, 400)

    # retornando resposta
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/treinos/<int:id>', methods=['DELETE'])
def delete_treinos(id):
    try:
        session = Session()
        treino = session.query(Treino).filter_by(id=id).one()
        session.delete(treino)
        session.commit()
        response_json = {"msg": "Treino excluído com sucesso!"}
        status_code = 200
    except Exception as e:
        response_json = {"msg": "Não foi possível excluir o treino."}
        status_code = 400

    response = make_response(jsonify(response_json), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/treino/<int:id>', methods=['PATCH'])
def patch_treinos(id):
    session = Session()
    treino = session.query(Treino).filter_by(id=id).first()

    if not treino:
        return make_response(jsonify({'msg': 'Treino não encontrado.'}), 404)

    try:
        patch_data = request.get_json()
        quantidade = patch_data.get('quantidade')
        if quantidade is None:
            return make_response(jsonify({'msg': 'A quantidade não foi fornecida.'}), 400)

        treino.quantidade -= quantidade

        session.add(treino)
        session.commit()

        treino_dict = {"id": treino.id, "nome": treino.nome, "quantidade": treino.quantidade}
        response_json = jsonify(treino_dict)

        response = make_response(response_json, 200)

        print("Patch no treino:", treino_dict)

    except Exception as e:

        error = {"msg": "Não foi possível editar o item."}

        response_json = jsonify(error)

        response = make_response(response_json, 400)

    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/bmi', methods=['PUT'])
def update_bmi_data():
    data = request.get_json()
    bmi = data.get("bmi")
    health = data.get("health")
    healthy_bmi_range = data.get("healthy_bmi_range")

    if bmi is None:
        return make_response(jsonify({'msg': 'Valor de IMC vazio na solicitação.'}), 400)

    try:
        session = Session()
        bmi_data = session.query(BMIData).first()

        if bmi_data:
            # Se já existirem valores de BMI na base de dados, atualize-os.
            bmi_data.bmi = bmi
            bmi_data.health = health
            bmi_data.healthy_bmi_range = healthy_bmi_range
        else:
            # Se não existirem valores na base de dados, crie um novo registro.
            bmi_data = BMIData(bmi=bmi, health=health, healthy_bmi_range=healthy_bmi_range)
            session.add(bmi_data)

        session.commit()

        response_json = {
            "msg": "Valores do IMC, saúde e faixa saudável atualizados com sucesso.",
            "bmi": bmi,
            "health": health,
            "healthy_bmi_range": healthy_bmi_range
        }
        response = make_response(jsonify(response_json), 200)

    except Exception as e:
        error = {"msg": "Não foi possível atualizar os valores do IMC e saúde."}
        response_json = jsonify(error)
        response = make_response(response_json, 400)

    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/bmi', methods=['GET'])
def get_bmi_data():
    session = Session()
    bmi_data = session.query(BMIData).first()

    if bmi_data:
        # Se os valores de BMI existirem na base de dados, retorna esses valores.
        bmi = bmi_data.bmi
        health = bmi_data.health
        healthy_bmi_range = bmi_data.healthy_bmi_range
    else:
        # Se não existirem valores na base de dados, retorna valores zerados ou vazios.
        bmi = 0
        health = ""
        healthy_bmi_range = ""

    response_json = {
        "bmi": bmi,
        "health": health,
        "healthy_bmi_range": healthy_bmi_range
    }
    print("BMI Data:", bmi_data)
    return jsonify(response_json)


app.run(port=5000, host='0.0.0.0', debug=True)



