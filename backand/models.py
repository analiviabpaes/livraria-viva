class Categoria:
    def __init__(self, nome, descricao=None, id_categoria=None):
        self.id_categoria = id_categoria
        self.nome = nome
        self.descricao = descricao

    def to_dict(self):
        return {"id_categoria": self.id_categoria, "nome": self.nome,
                "descricao": self.descricao}

    @staticmethod
    def from_dict(d):
        return Categoria(d["nome"], d.get("descricao") or None, d.get("id_categoria"))


class Usuario:
    def __init__(self, nome, email, senha=None, telefone=None, id_usuario=None):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone

    def to_dict(self):  # a senha nunca sai da API
        return {"id_usuario": self.id_usuario, "nome": self.nome,
                "email": self.email, "telefone": self.telefone}

    @staticmethod
    def from_dict(d):
        return Usuario(d["nome"], d["email"], d.get("senha"),
                       d.get("telefone") or None, d.get("id_usuario"))


class Livro:
    def __init__(self, titulo, autor, preco, id_categoria, estoque=0,
                 descricao=None, isbn=None, id_livro=None):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.preco = preco
        self.id_categoria = id_categoria
        self.estoque = estoque
        self.descricao = descricao
        self.isbn = isbn

    def to_dict(self):
        return {"id_livro": self.id_livro, "titulo": self.titulo, "autor": self.autor,
                "preco": self.preco, "id_categoria": self.id_categoria,
                "estoque": self.estoque, "descricao": self.descricao, "isbn": self.isbn}

    @staticmethod
    def from_dict(d):
        return Livro(d["titulo"], d["autor"], float(d["preco"]), int(d["id_categoria"]),
                     int(d.get("estoque") or 0), d.get("descricao") or None,
                     d.get("isbn") or None, d.get("id_livro"))


class ItemPedido:
    def __init__(self, id_livro, quantidade, preco_unitario=None, id_pedido=None, id_item=None):
        if quantidade < 1:
            raise ValueError("A quantidade deve ser pelo menos 1.")
        self.id_item = id_item
        self.id_livro = id_livro
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.id_pedido = id_pedido

    def to_dict(self):
        return {"id_item": self.id_item, "id_livro": self.id_livro,
                "quantidade": self.quantidade, "preco_unitario": self.preco_unitario,
                "id_pedido": self.id_pedido}

    @staticmethod
    def from_dict(d):
        return ItemPedido(int(d["id_livro"]), int(d["quantidade"]),
                          d.get("preco_unitario"), d.get("id_pedido"), d.get("id_item"))


class Pedido:
    STATUS = ("pendente", "pago", "enviado", "cancelado")

    def __init__(self, id_usuario=None, status="pendente", itens=None,
                 valor_total=0, data_pedido=None, id_pedido=None):
        if status not in Pedido.STATUS:
            raise ValueError("Status inválido: " + str(status))
        self.id_pedido = id_pedido
        self.id_usuario = id_usuario
        self.status = status
        self.itens = itens or []
        self.valor_total = valor_total
        self.data_pedido = data_pedido

    def calcular_total(self):
        return round(sum(i.quantidade * i.preco_unitario for i in self.itens), 2)

    def to_dict(self):
        return {"id_pedido": self.id_pedido, "id_usuario": self.id_usuario,
                "status": self.status, "valor_total": self.valor_total,
                "data_pedido": self.data_pedido,
                "itens": [i.to_dict() for i in self.itens]}

    @staticmethod
    def from_dict(d):
        id_usuario = d.get("id_usuario")
        return Pedido(int(id_usuario) if id_usuario is not None else None,
                      d.get("status", "pendente"),
                      [ItemPedido.from_dict(i) for i in d.get("itens", [])],
                      d.get("valor_total", 0), d.get("data_pedido"), d.get("id_pedido"))