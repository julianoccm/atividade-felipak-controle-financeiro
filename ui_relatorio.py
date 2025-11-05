from PyQt5 import QtWidgets, QtCore
from database import conectar

class TelaRelatorioFinanceiro(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Relatório Financeiro Mensal")
        self.resize(600, 400)

        layout = QtWidgets.QVBoxLayout()

        titulo = QtWidgets.QLabel("Relatório Financeiro - Vendas x Custos x Lucro")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        titulo.setAlignment(QtCore.Qt.AlignCenter)

        self.tabela = QtWidgets.QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Mês", "Vendas (R$)", "Custos (R$)", "Lucro (R$)"])
        self.tabela.horizontalHeader().setStretchLastSection(True)
        self.tabela.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        btn_atualizar = QtWidgets.QPushButton("🔄 Atualizar Relatório")
        btn_atualizar.clicked.connect(self.atualizar_relatorio)

        layout.addWidget(titulo)
        layout.addWidget(self.tabela)
        layout.addWidget(btn_atualizar)

        self.setLayout(layout)
        self.atualizar_relatorio()

    def atualizar_relatorio(self):
        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                strftime('%Y-%m', v.data) AS mes,
                SUM(v.quantidade * p.preco) AS total_vendas,
                SUM(v.quantidade * (
                    SELECT SUM(i.quantidade * i.custo_unitario)
                    FROM ingredientes i
                    WHERE i.produto_id = v.produto_id
                )) AS total_custos
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            GROUP BY mes
            ORDER BY mes;
        """)

        resultados = cur.fetchall()
        conn.close()

        self.tabela.setRowCount(len(resultados))

        for row, (mes, total_vendas, total_custos) in enumerate(resultados):
            lucro = (total_vendas or 0) - (total_custos or 0)
            self.tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(mes))
            self.tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f"R$ {total_vendas:.2f}" if total_vendas else "R$ 0.00"))
            self.tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f"R$ {total_custos:.2f}" if total_custos else "R$ 0.00"))
            self.tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f"R$ {lucro:.2f}"))

        self.tabela.resizeRowsToContents()