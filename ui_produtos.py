from PyQt5 import QtWidgets
from database import conectar


class TelaProdutos(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Produtos")
        self.resize(600, 700)

        layout = QtWidgets.QVBoxLayout()
        self.nome = QtWidgets.QLineEdit()
        self.nome.setPlaceholderText("Nome do produto")

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.container_ingredientes = QtWidgets.QWidget()
        self.layout_ingredientes = QtWidgets.QVBoxLayout(self.container_ingredientes)
        self.layout_ingredientes.setSpacing(5)
        self.scroll_area.setWidget(self.container_ingredientes)

        self.btn_add_ingrediente = QtWidgets.QPushButton("Adicionar Ingrediente")
        self.btn_add_ingrediente.clicked.connect(self.adicionar_ingrediente)

        self.ingredientes = []
        self.adicionar_ingrediente()

        self.margem = QtWidgets.QLineEdit()
        self.margem.setPlaceholderText("Margem de lucro (%) — Padrão 30")

        self.btn_calcular = QtWidgets.QPushButton("Calcular Preço Justo")
        self.btn_calcular.clicked.connect(self.calcular_preco_justo)

        self.label_resultado = QtWidgets.QLabel("")
        self.label_resultado.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")

        self.btn_salvar = QtWidgets.QPushButton("Salvar Produto")
        self.btn_salvar.clicked.connect(self.salvar_produto)
        self.btn_salvar.setEnabled(False)

        self.lista = QtWidgets.QListWidget()
        self.atualizar_lista()

        layout.addWidget(self.nome)
        layout.addWidget(self.btn_add_ingrediente)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.margem)
        layout.addWidget(self.btn_calcular)
        layout.addWidget(self.label_resultado)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(QtWidgets.QLabel("Produtos cadastrados:"))
        layout.addWidget(self.lista)

        self.setLayout(layout)

    def adicionar_ingrediente(self):
        ingr = QtWidgets.QLineEdit()
        ingr.setPlaceholderText("Ingrediente (nome)")

        qtd = QtWidgets.QLineEdit()
        qtd.setPlaceholderText("Quantidade em % (ex: 0.5)")

        custo = QtWidgets.QLineEdit()
        custo.setPlaceholderText("Custo unitário (ex: 2.50)")

        linha = QtWidgets.QHBoxLayout()
        linha.addWidget(ingr)
        linha.addWidget(qtd)
        linha.addWidget(custo)

        self.ingredientes.append((ingr, qtd, custo))

        linha_widget = QtWidgets.QWidget()
        linha_widget.setLayout(linha)
        self.layout_ingredientes.addWidget(linha_widget)

    def calcular_preco_justo(self):
        total_custo = 0.0
        for ingr, qtd, custo in self.ingredientes:
            try:
                q = float(qtd.text()) if qtd.text() else 0
                c = float(custo.text()) if custo.text() else 0
                total_custo += q * c
            except ValueError:
                pass

        margem = float(self.margem.text()) / 100 if self.margem.text() else 0.30
        preco_sugerido = total_custo * (1 + margem)

        self.label_resultado.setText(f"Preço custo por produto: R$ {total_custo:.2f}\nPreço sugerido: R$ {preco_sugerido:.2f}")
        self.btn_salvar.setEnabled(True)
        self.preco_final = preco_sugerido

    def salvar_produto(self):
        nome = self.nome.text()
        preco = getattr(self, "preco_final", None)

        if nome and preco:
            conn = conectar()
            cur = conn.cursor()

            cur.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
            produto_id = cur.lastrowid  # pega o ID recém criado

            for ingr, qtd, custo in self.ingredientes:
                nome_ingr = ingr.text()
                try:
                    quantidade = float(qtd.text()) if qtd.text() else 0
                    custo_unit = float(custo.text()) if custo.text() else 0
                except ValueError:
                    quantidade = 0
                    custo_unit = 0

                if nome_ingr:
                    cur.execute("""
                                INSERT INTO ingredientes (produto_id, nome, quantidade, custo_unitario)
                                VALUES (?, ?, ?, ?)
                                """, (produto_id, nome_ingr, quantidade, custo_unit))

            conn.commit()
            conn.close()

            self.nome.clear()
            for ingr, qtd, custo in self.ingredientes:
                ingr.clear()
                qtd.clear()
                custo.clear()
            self.margem.clear()
            self.label_resultado.clear()
            self.btn_salvar.setEnabled(False)
            self.atualizar_lista()

    def atualizar_lista(self):
        self.lista.clear()
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT nome, preco FROM produtos")
        for nome, preco in cur.fetchall():
            self.lista.addItem(f"{nome} - R$ {preco:.2f}")
        conn.close()
