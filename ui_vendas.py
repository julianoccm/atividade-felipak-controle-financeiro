from PyQt5 import QtWidgets
from database import conectar
from datetime import datetime

class TelaVendas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Vendas")
        self.resize(400, 300)

        layout = QtWidgets.QVBoxLayout()

        self.combo_produto = QtWidgets.QComboBox()
        self.qtd = QtWidgets.QSpinBox()
        self.qtd.setRange(1, 100)
        self.btn_registrar = QtWidgets.QPushButton("Registrar Venda")
        self.btn_registrar.clicked.connect(self.registrar_venda)

        self.lista = QtWidgets.QListWidget()

        layout.addWidget(QtWidgets.QLabel("Produto:"))
        layout.addWidget(self.combo_produto)
        layout.addWidget(QtWidgets.QLabel("Quantidade:"))
        layout.addWidget(self.qtd)
        layout.addWidget(self.btn_registrar)
        layout.addWidget(QtWidgets.QLabel("Vendas registradas:"))
        layout.addWidget(self.lista)

        self.setLayout(layout)
        self.carregar_produtos()
        self.atualizar_vendas()

    def carregar_produtos(self):
        self.combo_produto.clear()
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, preco FROM produtos")
        self.produtos = cur.fetchall()
        for p in self.produtos:
            self.combo_produto.addItem(f"{p[1]} - R$ {p[2]:.2f}", p[0])
        conn.close()

    def registrar_venda(self):
        produto_id = self.combo_produto.currentData()
        qtd = self.qtd.value()
        preco = [p[2] for p in self.produtos if p[0] == produto_id][0]
        total = preco * qtd
        data = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO vendas (produto_id, quantidade, total, data) VALUES (?, ?, ?, ?)",
                    (produto_id, qtd, total, data))
        conn.commit()
        conn.close()
        self.atualizar_vendas()

    def atualizar_vendas(self):
        self.lista.clear()
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
                    SELECT v.id, p.nome, v.quantidade, v.total, v.data
                    FROM vendas v
                             JOIN produtos p ON v.produto_id = p.id
                    ORDER BY v.data DESC
                    """)
        for id_, nome, qtd, total, data in cur.fetchall():
            self.lista.addItem(f"{data} | {nome} x{qtd} - R$ {total:.2f}")
        conn.close()
