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


