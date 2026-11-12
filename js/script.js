// Endereço da API Flask. Local: vazio (o próprio Flask serve o site).
// No GitHub Pages: troque SEU_USUARIO pelo seu usuário do PythonAnywhere.
let API = location.hostname.endsWith("github.io") ? "https://SEU_USUARIO.pythonanywhere.com" : "";

let $ = id => document.getElementById(id);
let esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
let reais = v => "R$ " + Number(v).toFixed(2).replace(".", ",");
let slug = t => t.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  .replace(/ de /g, " ").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
let botoes = (id, extra = "") => `<div class="acoes-td" style="justify-content: center;">${extra}
  <button type="button" class="botao botao-warning" style="padding: 4px 10px; font-size: 0.85rem;" data-acao="editar" data-id="${id}">Editar</button>
  <button type="button" class="botao botao-danger" style="padding: 4px 10px; font-size: 0.85rem;" data-acao="excluir" data-id="${id}">Excluir</button></div>`;

// ---------- comunicação com a API Flask ----------
async function api(url, metodo = "GET", dados) {
  let resposta = await fetch(API + url, {
    method: metodo,
    headers: {"Content-Type": "application/json"},
    body: dados && JSON.stringify(dados)
  });
  if (resposta.status === 204) return null;
  let json = await resposta.json();
  if (!resposta.ok) throw new Error(json.erro || "Erro na requisição");
  return json;
}

function msg(texto, ok = true) {
  $("msg").textContent = texto;
  $("msg").style.color = ok ? "green" : "red";
}

async function excluir(recurso, id, recarregar) {
  if (!confirm("Excluir este registro?")) return;
  try {
    await api(`/${recurso}/${id}`, "DELETE");
    msg("Excluído com sucesso!");
    recarregar();
  } catch (erro) {
    msg(erro.message, false);
  }
}

// ---------- formulário que cria (POST) ou edita (PUT) ----------
function crud(recurso, form, recarregar, somenteCriacao = []) {
  let editando = null;
  let salvar = form.querySelector("[type=submit]");
  let rotulo = salvar.textContent;
  let cancelar = form.querySelector(".cancelar");

  let limpar = () => {
    form.reset();
    editando = null;
    salvar.textContent = rotulo;
    cancelar.style.display = "none";
    somenteCriacao.forEach(nome => form.elements[nome].disabled = false);
  };
  cancelar.onclick = limpar;

  form.onsubmit = async e => {
    e.preventDefault();
    let dados = Object.fromEntries(new FormData(form));
    try {
      await (editando ? api(`/${recurso}/${editando}`, "PUT", dados) : api(`/${recurso}`, "POST", dados));
      msg(editando ? "Atualizado com sucesso!" : "Cadastrado com sucesso!");
      limpar();
      recarregar();
    } catch (erro) {
      msg(erro.message, false);
    }
  };

  return {
    editar(item, id) {
      editando = id;
      [...form.elements].forEach(el => { if (el.name in item) el.value = item[el.name] ?? ""; });
      somenteCriacao.forEach(nome => form.elements[nome].disabled = true);
      salvar.textContent = "Salvar alterações";
      cancelar.style.display = "";
      form.scrollIntoView();
    }
  };
}

function ligarAcoes(lista, recurso, obter, controle, recarregar) {
  lista.onclick = e => {
    let botao = e.target.closest("button[data-acao]");
    if (!botao) return;
    let id = Number(botao.dataset.id);
    if (botao.dataset.acao === "editar") controle.editar(obter(id), id);
    else excluir(recurso, id, recarregar);
  };
}

// ---------- categorias e usuários (tabela + formulário) ----------
function paginaTabela(recurso, chave, linha, somenteCriacao) {
  let itens = [];
  let controle = crud(recurso, $("form"), carregar, somenteCriacao);
  async function carregar() {
    itens = await api("/" + recurso);
    $("lista").innerHTML = itens.map(i => `<tr>${linha(i)}<td>${botoes(i[chave])}</td></tr>`).join("");
  }
  ligarAcoes($("lista"), recurso, id => itens.find(i => i[chave] === id), controle, carregar);
  carregar().catch(e => msg(e.message, false));
}

// ---------- livros (catálogo + formulário) ----------
function paginaLivros() {
  let livros = [];
  let controle = crud("livros", $("form"), carregar);
  async function carregar() {
    let [lista, categorias] = await Promise.all([api("/livros"), api("/categorias")]);
    livros = lista;
    let nomes = Object.fromEntries(categorias.map(c => [c.id_categoria, c.nome]));
    $("id_categoria").innerHTML = categorias.map(c => `<option value="${c.id_categoria}">${esc(c.nome)}</option>`).join("");
    $("lista").innerHTML = livros.map(l => `
      <figure class="livro">
        <img src="../img/livros/${slug(l.titulo)}.webp" alt="${esc(l.titulo)}" onerror="if (this.src.endsWith('.webp')) this.src = this.src.replace('.webp', '.jpg'); else this.remove()">
        <figcaption><strong>${esc(l.titulo)}</strong><br><span>${esc(l.autor)} | ${esc(nomes[l.id_categoria])}</span></figcaption>
        <div class="preco">${reais(l.preco)}</div>
        ${botoes(l.id_livro)}
      </figure>`).join("");
  }
  ligarAcoes($("lista"), "livros", id => livros.find(l => l.id_livro === id), controle, carregar);
  $("busca").oninput = e => document.querySelectorAll("#lista .livro").forEach(f => {
    let titulo = f.querySelector("strong").textContent.toLowerCase();
    f.classList.toggle("escondido", !titulo.includes(e.target.value.toLowerCase()));
  });
  carregar().catch(e => msg(e.message, false));
}

// ---------- pedidos ----------
function paginaPedidos() {
  let STATUS = ["pendente", "pago", "enviado", "cancelado"];
  let livros = [], usuarios = [];

  let novaLinha = () => {
    let d = document.createElement("div");
    d.className = "linha";
    d.style.cssText = "display: flex; gap: 8px;";
    d.innerHTML = `<select style="flex: 1;">${livros.map(l => `<option value="${l.id_livro}">${esc(l.titulo)} - ${reais(l.preco)}</option>`).join("")}</select>
      <input type="number" min="1" value="1" style="width: 80px;" required>`;
    $("itens").appendChild(d);
  };

  async function carregar() {
    [usuarios, livros] = await Promise.all([api("/usuarios"), api("/livros")]);
    $("usuario").innerHTML = usuarios.map(u => `<option value="${u.id_usuario}">${esc(u.nome)}</option>`).join("");
    $("itens").innerHTML = "";
    novaLinha();
    let pedidos = await api("/pedidos");
    let nome = id => (usuarios.find(u => u.id_usuario === id) || {}).nome;
    $("lista").innerHTML = pedidos.map(p => `
      <tr>
        <td>${p.id_pedido}</td>
        <td>${esc(nome(p.id_usuario))}</td>
        <td>${new Date(p.data_pedido.replace(" ", "T")).toLocaleString("pt-BR")}</td>
        <td>${reais(p.valor_total)}</td>
        <td><select data-id="${p.id_pedido}">${STATUS.map(s => `<option${s === p.status ? " selected" : ""}>${s}</option>`).join("")}</select></td>
        <td><div class="acoes-td">
          <button type="button" class="botao" style="padding: 4px 10px; font-size: 0.85rem;" data-acao="itens" data-id="${p.id_pedido}">Itens</button>
          <button type="button" class="botao botao-danger" style="padding: 4px 10px; font-size: 0.85rem;" data-acao="excluir" data-id="${p.id_pedido}">Excluir</button>
        </div></td>
      </tr>`).join("");
  }

  $("add-item").onclick = novaLinha;

  $("form").onsubmit = async e => {
    e.preventDefault();
    let itens = [...document.querySelectorAll("#itens .linha")].map(d => ({
      id_livro: Number(d.children[0].value), quantidade: Number(d.children[1].value)
    }));
    try {
      await api("/pedidos", "POST", {id_usuario: Number($("usuario").value), itens});
      msg("Pedido realizado com sucesso!");
      carregar();
    } catch (erro) {
      msg(erro.message, false);
    }
  };

  $("lista").onchange = async e => {
    try {
      await api(`/pedidos/${e.target.dataset.id}`, "PUT", {status: e.target.value});
      msg("Status atualizado!");
    } catch (erro) {
      msg(erro.message, false);
    }
  };

  $("lista").onclick = async e => {
    let botao = e.target.closest("button[data-acao]");
    if (!botao) return;
    let id = Number(botao.dataset.id);
    if (botao.dataset.acao === "excluir") return excluir("pedidos", id, carregar);
    let pedido = await api("/pedidos/" + id);
    let titulo = i => (livros.find(l => l.id_livro === i) || {}).titulo;
    $("detalhe").innerHTML = `<h4>Itens do pedido ${id}</h4>` + pedido.itens.map(i =>
      `<p>${esc(titulo(i.id_livro))} - ${i.quantidade} x ${reais(i.preco_unitario)}</p>`).join("");
  };

  carregar().catch(e => msg(e.message, false));
}

// ---------- qual página está aberta ----------
let paginas = {
  livros: paginaLivros,
  pedidos: paginaPedidos,
  categorias: () => paginaTabela("categorias", "id_categoria",
    c => `<td>${c.id_categoria}</td><td>${esc(c.nome)}</td><td>${esc(c.descricao)}</td>`),
  usuarios: () => paginaTabela("usuarios", "id_usuario",
    u => `<td>${u.id_usuario}</td><td>${esc(u.nome)}</td><td>${esc(u.email)}</td><td>${esc(u.telefone)}</td>`, ["senha"])
};
let pagina = document.body.dataset.pagina;
if (paginas[pagina]) paginas[pagina]();