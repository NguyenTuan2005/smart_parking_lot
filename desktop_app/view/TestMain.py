import sys
from PyQt6.QtWidgets import QApplication
# Import Main Window
from MenuMain import MenuMain

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuMain()
    window.show()
    sys.exit(app.exec_())
