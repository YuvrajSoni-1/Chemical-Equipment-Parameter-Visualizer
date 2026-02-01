import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.login import LoginDialog
from ui.dashboard import Dashboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(1000, 700)
        self.dashboard = Dashboard()
        self.setCentralWidget(self.dashboard)

def main():
    app = QApplication(sys.argv)
    
    # Login Flow
    login = LoginDialog()
    if login.exec_() == LoginDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
