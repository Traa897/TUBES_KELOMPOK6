import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QVBoxLayout, QHBoxLayout, QPushButton, 
                             QMessageBox, QComboBox, QTableWidget, 
                             QTableWidgetItem)
from PyQt5.QtCore import Qt

class TopUpDanaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDatabase()

    def initUI(self):
        self.setWindowTitle('Aplikasi Top Up Dana')
        self.setGeometry(100, 100, 600, 500)

        main_layout = QVBoxLayout()

        rekening_layout = QHBoxLayout()
        
        bank_label = QLabel('Pilih Bank:')
        self.bank_combo = QComboBox()
        bank_list = ['BCA', 'Mandiri', 'BNI', 'BRI', 'Permata']
        self.bank_combo.addItems(bank_list)
        rekening_layout.addWidget(bank_label)
        rekening_layout.addWidget(self.bank_combo)

        no_rekening_label = QLabel('Nomor Rekening:')
        self.no_rekening_input = QLineEdit()
        rekening_layout.addWidget(no_rekening_label)
        rekening_layout.addWidget(self.no_rekening_input)

        main_layout.addLayout(rekening_layout)

        jumlah_layout = QHBoxLayout()
        jumlah_label = QLabel('Jumlah Top Up (Rp):')
        self.jumlah_input = QLineEdit()
        jumlah_layout.addWidget(jumlah_label)
        jumlah_layout.addWidget(self.jumlah_input)

        main_layout.addLayout(jumlah_layout)

        self.topup_button = QPushButton('Top Up')
        self.topup_button.clicked.connect(self.proses_topup)
        main_layout.addWidget(self.topup_button)

        self.tabel_riwayat = QTableWidget()
        self.tabel_riwayat.setColumnCount(4)
        self.tabel_riwayat.setHorizontalHeaderLabels(['Bank', 'Nomor Rekening', 'Jumlah Top Up', 'Waktu'])
        main_layout.addWidget(self.tabel_riwayat)

        self.setLayout(main_layout)

    def initDatabase(self):
        self.conn = sqlite3.connect('topup_dana.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS riwayat_topup (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bank TEXT,
                nomor_rekening TEXT,
                jumlah REAL,
                waktu DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

        self.load_riwayat_topup()

    def proses_topup(self):
        bank = self.bank_combo.currentText()
        no_rekening = self.no_rekening_input.text()
        jumlah = self.jumlah_input.text()

        if not no_rekening or not jumlah:
            QMessageBox.warning(self, 'Peringatan', 'Harap isi semua field!')
            return

        try:
            jumlah = float(jumlah)
            if jumlah <= 0:
                raise ValueError('Jumlah harus lebih dari 0')
        except ValueError:
            QMessageBox.warning(self, 'Peringatan', 'Jumlah top up tidak valid!')
            return

        self.cursor.execute('''
            INSERT INTO riwayat_topup (bank, nomor_rekening, jumlah) 
            VALUES (?, ?, ?)
        ''', (bank, no_rekening, jumlah))
        self.conn.commit()

        QMessageBox.information(self, 'Berhasil', 'Top Up Dana Berhasil!')

        self.no_rekening_input.clear()
        self.jumlah_input.clear()
        self.load_riwayat_topup()

    def load_riwayat_topup(self):
        self.cursor.execute('SELECT bank, nomor_rekening, jumlah, waktu FROM riwayat_topup ORDER BY waktu DESC')
        riwayat = self.cursor.fetchall()

        self.tabel_riwayat.setRowCount(len(riwayat))

        for row, (bank, no_rekening, jumlah, waktu) in enumerate(riwayat):
            self.tabel_riwayat.setItem(row, 0, QTableWidgetItem(bank))
            self.tabel_riwayat.setItem(row, 1, QTableWidgetItem(no_rekening))
            self.tabel_riwayat.setItem(row, 2, QTableWidgetItem(f'Rp {jumlah:,.2f}'))
            self.tabel_riwayat.setItem(row, 3, QTableWidgetItem(waktu))

    def closeEvent(self, event):
        self.conn.close()

def main():
    app = QApplication(sys.argv)
    topup_app = TopUpDanaApp()
    topup_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
