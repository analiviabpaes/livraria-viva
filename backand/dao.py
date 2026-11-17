import os
import sqlite3
from werkzeug.security import generate_password_hash
from models import Categoria, Usuario, Livro, Pedido, ItemPedido

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
ARQUIVO_BD = os.path.join(PASTA, "livraria.db")


def ler(nome):
    with open(os.path.join(PASTA, nome), encoding="utf-8") as f:
        return f.read()


def criar_conexao():
    """Abre o banco; cria o arquivo, as tabelas e os dados iniciais se ainda não existirem."""
    novo = not os.path.exists(ARQUIVO_BD)
    conexao = sqlite3.connect(ARQUIVO_BD, check_same_thread=False)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.executescript(ler("modelo_fisico.sql"))
    if novo:
        conexao.executescript(ler("dados_iniciais.sql"))
    return conexao


class BaseDAO:
    tabela = pk = ""
    modelo = None
    campos = []               # colunas gravadas no INSERT
    campos_atualizar = None   # colunas gravadas no UPDATE (padrão: as mesmas)

    def __init__(self, conexao):
        self.conexao = conexao

    def listar(self):
        linhas = self.conexao.execute(f"SELECT * FROM {self.tabela} ORDER BY {self.pk}").fetchall()
        return [self.modelo.from_dict(dict(l)) for l in linhas]

    def buscar_por_id(self, id):
        linha = self.conexao.execute(
            f"SELECT * FROM {self.tabela} WHERE {self.pk} = ?", (id,)).fetchone()
        return self.modelo.from_dict(dict(linha)) if linha else None

    def inserir(self, obj):
        marcas = ", ".join("?" * len(self.campos))
        cursor = self.conexao.execute(
            f"INSERT INTO {self.tabela} ({', '.join(self.campos)}) VALUES ({marcas})",
            [getattr(obj, c) for c in self.campos])
        self.conexao.commit()
        setattr(obj, self.pk, cursor.lastrowid)
        return obj

    def atualizar(self, id, obj):
        campos = self.campos_atualizar or self.campos
        sets = ", ".join(f"{c} = ?" for c in campos)
        cursor = self.conexao.execute(
            f"UPDATE {self.tabela} SET {sets} WHERE {self.pk} = ?",
            [getattr(obj, c) for c in campos] + [id])
        self.conexao.commit()
        return cursor.rowcount > 0

    def excluir(self, id):
        cursor = self.conexao.execute(f"DELETE FROM {self.tabela} WHERE {self.pk} = ?", (id,))
        self.conexao.commit()
        return cursor.rowcount > 0


class CategoriaDAO(BaseDAO):
    tabela, pk, modelo = "categoria", "id_categoria", Categoria
    campos = ["nome", "descricao"]


class UsuarioDAO(BaseDAO):
    tabela, pk, modelo = "usuario", "id_usuario", Usuario
    campos = ["nome", "email", "senha", "telefone"]
    campos_atualizar = ["nome", "email", "telefone"]

    def inserir(self, usuario):
        if not usuario.senha:
            raise ValueError("A senha é obrigatória.")
        usuario.senha = generate_password_hash(usuario.senha)
        return super().inserir(usuario)


class LivroDAO(BaseDAO):
    tabela, pk, modelo = "livro", "id_livro", Livro
    campos = ["titulo", "autor", "descricao", "estoque", "preco", "isbn", "id_categoria"]


class PedidoDAO(BaseDAO):
    tabela, pk, modelo = "pedido", "id_pedido", Pedido
    campos_atualizar = ["status"]

    def inserir(self, pedido):
        if not pedido.itens:
            raise ValueError("O pedido precisa ter ao menos um item.")
        try:
            for item in pedido.itens:
                linha = self.conexao.execute(
                    "SELECT preco FROM livro WHERE id_livro = ?", (item.id_livro,)).fetchone()
                if not linha:
                    raise ValueError(f"O livro {item.id_livro} não existe.")
                item.preco_unitario = linha["preco"]
            pedido.valor_total = pedido.calcular_total()
            cursor = self.conexao.execute(
                "INSERT INTO pedido (id_usuario, valor_total, status) VALUES (?, ?, ?)",
                (pedido.id_usuario, pedido.valor_total, pedido.status))
            pedido.id_pedido = cursor.lastrowid
            for item in pedido.itens:
                self.conexao.execute(
                    "INSERT INTO item_pedido (id_pedido, id_livro, quantidade, preco_unitario) "
                    "VALUES (?, ?, ?, ?)",
                    (pedido.id_pedido, item.id_livro, item.quantidade, item.preco_unitario))
            self.conexao.commit()
            return pedido
        except Exception:
            self.conexao.rollback()
            raise

    def buscar_por_id(self, id):
        pedido = super().buscar_por_id(id)
        if pedido:
            linhas = self.conexao.execute(
                "SELECT * FROM item_pedido WHERE id_pedido = ?", (id,)).fetchall()
            pedido.itens = [ItemPedido.from_dict(dict(l)) for l in linhas]
        return pedido