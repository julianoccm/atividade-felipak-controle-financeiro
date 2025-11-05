from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from ui_produtos import TelaProdutos
from ui_relatorio import TelaRelatorioFinanceiro
from ui_vendas import TelaVendas


class TelaPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controle Financeiro")
        self.resize(300, 350)

        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 10)

        image_label = QLabel()
        pixmap = QPixmap("image.png")
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        titulo = QtWidgets.QLabel("Bem-vinda, Dona Maria!")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        titulo.setAlignment(Qt.AlignCenter)

        btn_produtos = QtWidgets.QPushButton("\nGerenciar Produtos\n")
        btn_produtos.clicked.connect(self.abrir_produtos)

        btn_vendas = QtWidgets.QPushButton("\nRegistrar Vendas\n")
        btn_vendas.clicked.connect(self.abrir_vendas)

        btn_relatorio = QtWidgets.QPushButton("\nRelatório Financeiro\n")
        btn_relatorio.clicked.connect(self.abrir_relatorio)

        layout.addWidget(image_label, alignment=Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(titulo)
        layout.addWidget(btn_produtos)
        layout.addWidget(btn_vendas)
        layout.addWidget(btn_relatorio)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def abrir_produtos(self):
        self.janela_produtos = TelaProdutos()
        self.janela_produtos.show()

    def abrir_vendas(self):
        self.janela_vendas = TelaVendas()
        self.janela_vendas.show()

    def abrir_relatorio(self):
        self.janela_relatorio = TelaRelatorioFinanceiro()
        self.janela_relatorio.show()
