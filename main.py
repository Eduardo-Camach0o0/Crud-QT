# import sys
# # Asegúrate de importar QtWidgets y QMainWindow
# from PyQt5 import QtWidgets, uic
# from PyQt5.QtWidgets import QMainWindow, QApplication

# # Cambia esta línea para que herede de QMainWindow
# class VentanaProductos(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi('ui/menu.ui', self)

# # El resto de tu función main()...
# def main():
#     app = QApplication(sys.argv)
#     window = VentanaProductos()
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()




from PyQt5 import QtWidgets
import sys
from load.load_iu_login import Login

def main():
    app = QtWidgets.QApplication(sys.argv)
    # window = Load_ui_productos()
    window = Login()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()