import os
import sqlite3
from flask import Flask, abort, jsonify, request, send_from_directory
from dao import criar_conexao, CategoriaDAO, UsuarioDAO, LivroDAO, PedidoDAO
from models import Categoria, Usuario, Livro, Pedido

RAIZ = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
conexao = criar_conexao()


def registrar(nome, dao, modelo):
    """Cria as 5 rotas do CRUD de um recurso: GET, GET/<id>, POST, PUT/<id>, DELETE/<id>."""

    def listar():
        return jsonify([o.to_dict() for o in dao.listar()])

    def buscar(id):
        obj = dao.buscar_por_id(id)
        return (jsonify(obj.to_dict()), 200) if obj else (jsonify(erro="Não encontrado"), 404)

    def criar():
        novo = dao.inserir(modelo.from_dict(request.get_json()))
        return jsonify(novo.to_dict()), 201

    def atualizar(id):
        if not dao.atualizar(id, modelo.from_dict(request.get_json())):
            return jsonify(erro="Não encontrado"), 404
        return "", 204

    def excluir(id):
        return ("", 204) if dao.excluir(id) else (jsonify(erro="Não encontrado"), 404)

    app.add_url_rule(f"/{nome}", f"listar_{nome}", listar, methods=["GET"])
    app.add_url_rule(f"/{nome}", f"criar_{nome}", criar, methods=["POST"])
    app.add_url_rule(f"/{nome}/<int:id>", f"buscar_{nome}", buscar, methods=["GET"])
    app.add_url_rule(f"/{nome}/<int:id>", f"atualizar_{nome}", atualizar, methods=["PUT"])
    app.add_url_rule(f"/{nome}/<int:id>", f"excluir_{nome}", excluir, methods=["DELETE"])


registrar("categorias", CategoriaDAO(conexao), Categoria)
registrar("usuarios", UsuarioDAO(conexao), Usuario)
registrar("livros", LivroDAO(conexao), Livro)
registrar("pedidos", PedidoDAO(conexao), Pedido)


@app.errorhandler(KeyError)
def campo_ausente(e):
    return jsonify(erro=f"Campo obrigatório ausente: {e}"), 400


@app.errorhandler(ValueError)
@app.errorhandler(TypeError)
def dados_invalidos(e):
    return jsonify(erro=f"Dados inválidos: {e}"), 400


@app.errorhandler(sqlite3.IntegrityError)
def integridade(e):
    return jsonify(erro="Operação não permitida: dado duplicado, obrigatório ou registro em uso."), 400


# páginas do front-end
@app.get("/")
@app.get("/index.html")
def home():
    return send_from_directory(RAIZ, "index.html")


@app.get("/<pasta>/<path:arquivo>")
def estatico(pasta, arquivo):
    if pasta not in ("pages", "css", "js", "img"):
        abort(404)
    return send_from_directory(os.path.join(RAIZ, pasta), arquivo)


if __name__ == "__main__":
    app.run(debug=True)