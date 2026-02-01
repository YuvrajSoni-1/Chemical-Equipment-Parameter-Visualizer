from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Chemical Visualizer")
        self.resize(300, 150)
        self.layout = QVBoxLayout()
        
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.layout.addWidget(self.username)
        
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password)
        
        self.btn_login = QPushButton("Login", self)
        self.btn_login.clicked.connect(self.check_login)
        self.layout.addWidget(self.btn_login)
        
        self.setLayout(self.layout)
        
    def check_login(self):
        # Strict validation
        if self.username.text() == 'admin' and self.password.text() == 'admin123':
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid Username or Password!")
