from PyQt5 import QtWidgets
from database import criar_tabelas
from ui_main import TelaPrincipal
import sys

if __name__ == "__main__":
    criar_tabelas()
    app = QtWidgets.QApplication(sys.argv)
    janela = TelaPrincipal()
    janela.show()
    sys.exit(app.exec_())
