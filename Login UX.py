import sys
from PyQt5.QtWidgets import*

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login Aplikasi')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Contoh validasi sederhana
        if username == 'admin' and password == 'password':
            QMessageBox.information(self, 'Login Berhasil', 'Selamat datang!')
            # Tambahkan kode untuk buka halaman selanjutnya
        else:
            QMessageBox.warning(self, 'Login Gagal', 'Username atau password salah')

def main():
    app = QApplication(sys.argv)
    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
