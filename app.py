from flask import Flask, redirect, request, make_response, jsonify
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Treino
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

app.run(port=5000, host='localhost', debug=True)

