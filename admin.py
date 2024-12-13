import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QMessageBox, QTabWidget, QComboBox, QDialog)
from PyQt5.QtCore import Qt

class AdminPemesananMakanan(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initDatabase()
        self.initUI()

    def initDatabase(self):
        # Koneksi database SQLite
        self.conn = sqlite3.connect('pemesanan_makanan.db')
        self.cursor = self.conn.cursor()

        # Tabel yang sudah ada sebelumnya
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS makanan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                harga REAL NOT NULL,
                kategori TEXT NOT NULL,
                stok INTEGER NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pesanan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_pelanggan TEXT NOT NULL,
                total_harga REAL NOT NULL,
                status TEXT NOT NULL,
                tanggal DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS detail_pesanan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pesanan_id INTEGER,
                makanan_id INTEGER,
                jumlah INTEGER,
                FOREIGN KEY(pesanan_id) REFERENCES pesanan(id),
                FOREIGN KEY(makanan_id) REFERENCES makanan(id)
            )
        ''')

        # Tambah tabel rating
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rating (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                makanan_id INTEGER,
                rating INTEGER NOT NULL,
                ulasan TEXT,
                nama_pelanggan TEXT,
                tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(makanan_id) REFERENCES makanan(id)
            )
        ''')
        
        self.conn.commit()

    def initUI(self):
        self.setWindowTitle('Admin Pemesanan Makanan')
        self.setGeometry(100, 100, 900, 700)

        # Widget utama
        widget_utama = QWidget()
        layout_utama = QVBoxLayout()

        # Tab Widget
        tab_widget = QTabWidget()
        
        # Tab Makanan
        tab_makanan = QWidget()
        layout_makanan = QVBoxLayout()

        # Formulir Tambah Makanan
        form_makanan = QWidget()
        layout_form_makanan = QHBoxLayout()
        
        nama_label = QLabel('Nama Makanan:')
        self.nama_input = QLineEdit()
        
        harga_label = QLabel('Harga:')
        self.harga_input = QLineEdit()
        
        kategori_label = QLabel('Kategori:')
        self.kategori_combo = QComboBox()
        self.kategori_combo.addItems(['Makanan Pembuka', 'Makanan Utama', 'Dessert', 'Minuman'])
        
        stok_label = QLabel('Stok:')
        self.stok_input = QLineEdit()
        
        tambah_makanan_btn = QPushButton('Tambah Makanan')
        tambah_makanan_btn.clicked.connect(self.tambah_makanan)

        # Layout form makanan
        layout_form_makanan.addWidget(nama_label)
        layout_form_makanan.addWidget(self.nama_input)
        layout_form_makanan.addWidget(harga_label)
        layout_form_makanan.addWidget(self.harga_input)
        layout_form_makanan.addWidget(kategori_label)
        layout_form_makanan.addWidget(self.kategori_combo)
        layout_form_makanan.addWidget(stok_label)
        layout_form_makanan.addWidget(self.stok_input)
        layout_form_makanan.addWidget(tambah_makanan_btn)

        form_makanan.setLayout(layout_form_makanan)
        layout_makanan.addWidget(form_makanan)

        # Tabel Daftar Makanan
        self.tabel_makanan = QTableWidget()
        self.tabel_makanan.setColumnCount(6)
        self.tabel_makanan.setHorizontalHeaderLabels(['ID', 'Nama', 'Harga', 'Kategori', 'Stok', 'Rating Rata-rata'])
        layout_makanan.addWidget(self.tabel_makanan)

        # Tombol Lihat Rating
        btn_lihat_rating = QPushButton('Lihat Detail Rating')
        btn_lihat_rating.clicked.connect(self.lihat_detail_rating)
        layout_makanan.addWidget(btn_lihat_rating)

        tab_makanan.setLayout(layout_makanan)

        # Tab Pesanan
        tab_pesanan = QWidget()
        layout_pesanan = QVBoxLayout()

        # Tabel Daftar Pesanan
        self.tabel_pesanan = QTableWidget()
        self.tabel_pesanan.setColumnCount(5)
        self.tabel_pesanan.setHorizontalHeaderLabels(['ID', 'Nama Pelanggan', 'Total Harga', 'Status', 'Tanggal'])
        layout_pesanan.addWidget(self.tabel_pesanan)

        # Tombol Update Status Pesanan
        self.status_pesanan = QComboBox()
        self.status_pesanan.addItems(['Pending', 'Dikirim', 'Selesai'])
        btn_update_status = QPushButton('Update Status Pesanan')
        btn_update_status.clicked.connect(self.update_status_pesanan)
        layout_pesanan.addWidget(self.status_pesanan)
        layout_pesanan.addWidget(btn_update_status)

        tab_pesanan.setLayout(layout_pesanan)

        # Tab Rating Baru
        tab_rating = QWidget()
        layout_rating = QVBoxLayout()

        # Tabel Daftar Rating
        self.tabel_rating = QTableWidget()
        self.tabel_rating.setColumnCount(6)
        self.tabel_rating.setHorizontalHeaderLabels(['ID', 'Nama Makanan', 'Rating', 'Ulasan', 'Nama Pelanggan', 'Tanggal'])
        layout_rating.addWidget(self.tabel_rating)

        tab_rating.setLayout(layout_rating)

        # Tambahkan tab ke tab widget
        tab_widget.addTab(tab_makanan, 'Manajemen Makanan')
        tab_widget.addTab(tab_pesanan, 'Pesanan')
        tab_widget.addTab(tab_rating, 'Rating')

        layout_utama.addWidget(tab_widget)
        widget_utama.setLayout(layout_utama)
        self.setCentralWidget(widget_utama)

        # Muat data awal
        self.load_makanan()
        self.load_pesanan()
        self.load_rating()

    def lihat_detail_rating(self):
        # Ambil baris terpilih
        selected_row = self.tabel_makanan.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Peringatan', 'Pilih makanan untuk melihat rating!')
            return

        # Ambil ID makanan
        makanan_id = self.tabel_makanan.item(selected_row, 0).text()
        nama_makanan = self.tabel_makanan.item(selected_row, 1).text()

        # Dialog detail rating
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Detail Rating - {nama_makanan}')
        layout = QVBoxLayout()

        # Tabel detail rating
        tabel_detail_rating = QTableWidget()
        tabel_detail_rating.setColumnCount(4)
        tabel_detail_rating.setHorizontalHeaderLabels(['Rating', 'Ulasan', 'Nama Pelanggan', 'Tanggal'])

        # Ambil rating untuk makanan ini
        self.cursor.execute('''
            SELECT rating, ulasan, nama_pelanggan, tanggal 
            FROM rating 
            WHERE makanan_id = ?
        ''', (makanan_id,))
        ratings = self.cursor.fetchall()

        # Isi tabel
        tabel_detail_rating.setRowCount(len(ratings))
        for row, (rating, ulasan, nama_pelanggan, tanggal) in enumerate(ratings):
            tabel_detail_rating.setItem(row, 0, QTableWidgetItem(str(rating)))
            tabel_detail_rating.setItem(row, 1, QTableWidgetItem(str(ulasan)))
            tabel_detail_rating.setItem(row, 2, QTableWidgetItem(str(nama_pelanggan)))
            tabel_detail_rating.setItem(row, 3, QTableWidgetItem(str(tanggal)))

        layout.addWidget(tabel_detail_rating)

        # Hitung rata-rata rating
        if ratings:
            avg_rating = sum(r[0] for r in ratings) / len(ratings)
            label_avg = QLabel(f'Rating Rata-rata: {avg_rating:.2f}')
            layout.addWidget(label_avg)

        dialog.setLayout(layout)
        dialog.resize(600, 400)
        dialog.exec_()

    def tambah_makanan(self):
        # Validasi input
        nama = self.nama_input.text()
        harga = self.harga_input.text()
        kategori = self.kategori_combo.currentText()
        stok = self.stok_input.text()

        if not nama or not harga or not stok:
            QMessageBox.warning(self, 'Peringatan', 'Harap isi semua field!')
            return

        try:
            harga = float(harga)
            stok = int(stok)
        except ValueError:
            QMessageBox.warning(self, 'Peringatan', 'Harga dan stok harus angka!')
            return

        # Simpan ke database
        self.cursor.execute('''
            INSERT INTO makanan (nama, harga, kategori, stok) 
            VALUES (?, ?, ?, ?)
        ''', (nama, harga, kategori, stok))
        self.conn.commit()

        # Reset input
        self.nama_input.clear()
        self.harga_input.clear()
        self.stok_input.clear()

        # Muat ulang tabel
        self.load_makanan()

    def load_makanan(self):
        # Ambil data makanan dengan rating rata-rata
        self.cursor.execute('''
            SELECT 
                m.id, 
                m.nama, 
                m.harga, 
                m.kategori, 
                m.stok, 
                COALESCE(AVG(r.rating), 0) as rata_rating 
            FROM makanan m
            LEFT JOIN rating r ON m.id = r.makanan_id
            GROUP BY m.id
        ''')
        makanan = self.cursor.fetchall()

        # Set jumlah baris tabel
        self.tabel_makanan.setRowCount(len(makanan))

        # Isi tabel dengan data
        for row, (id, nama, harga, kategori, stok, rata_rating) in enumerate(makanan):
            self.tabel_makanan.setItem(row, 0, QTableWidgetItem(str(id)))
            self.tabel_makanan.setItem(row, 1, QTableWidgetItem(nama))
            self.tabel_makanan.setItem(row, 2, QTableWidgetItem(f'Rp {harga:,.2f}'))
            self.tabel_makanan.setItem(row, 3, QTableWidgetItem(kategori))
            self.tabel_makanan.setItem(row, 4, QTableWidgetItem(str(stok)))
            self.tabel_makanan.setItem(row, 5, QTableWidgetItem(f'{rata_rating:.2f}'))

    def load_rating(self):
        # Ambil semua rating dengan nama makanan
        self.cursor.execute('''
            SELECT 
                r.id, 
                m.nama, 
                r.rating, 
                r.ulasan, 
                r.nama_pelanggan, 
                r.tanggal 
            FROM rating r
            JOIN makanan m ON r.makanan_id = m.id
            ORDER BY r.tanggal DESC
        ''')
        ratings = self.cursor.fetchall()

        # Set jumlah baris tabel
        self.tabel_rating.setRowCount(len(ratings))

        # Isi tabel dengan data
        for row, (id, nama_makanan, rating, ulasan, nama_pelanggan, tanggal) in enumerate(ratings):
            self.tabel_rating.setItem(row, 0, QTableWidgetItem(str(id)))
            self.tabel_rating.setItem(row, 1, QTableWidgetItem(nama_makanan))
            self.tabel_rating.setItem(row, 2, QTableWidgetItem(str(rating)))
            self.tabel_rating.setItem(row, 3, QTableWidgetItem(str(ulasan)))
            self.tabel_rating.setItem(row, 4, QTableWidgetItem(str(nama_pelanggan)))
            self.tabel_rating.setItem(row, 5, QTableWidgetItem(str(tanggal)))

    def load_pesanan(self):
        # Ambil data pesanan
        self.cursor.execute('SELECT * FROM pesanan')
        pesanan = self.cursor.fetchall()

        # Set jumlah baris tabel
        self.tabel_pesanan.setRowCount(len(pesanan))

        # Isi tabel dengan data
        for row, (id, nama_pelanggan, total_harga, status, tanggal) in enumerate(pesanan):
            self.tabel_pesanan.setItem(row, 0, QTableWidgetItem(str(id)))
            self.tabel_pesanan.setItem(row, 1, QTableWidgetItem(nama_pelanggan))
            self.tabel_pesanan.setItem(row, 2, QTableWidgetItem(f'Rp {total_harga:,.2f}'))
            self.tabel_pesanan.setItem(row, 3, QTableWidgetItem(status))
            self.tabel_pesanan.setItem(row, 4, QTableWidgetItem(tanggal))

    def update_status_pesanan(self):
        # Ambil baris terpilih
        selected_row = self.tabel_pesanan.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Peringatan', 'Pilih pesanan yang ingin diupdate!')
            return

        # Ambil ID pesanan
        pesanan_id = self.tabel_pesanan.item(selected_row, 0).text()
        # Ambil status pesanan
        status = self.status_pesanan.currentText()
        # Update status pesanan
        self.cursor.execute('UPDATE pesanan SET status = ? WHERE id = ?', (status, pesanan_id))
        self.conn.commit()
        # Tampilkan pesan
        QMessageBox.information(self, 'Sukses', 'Status pesanan berhasil diupdate!')
        # Tampilkan data pesanan
        self.load_pesanan()
        # Tampilkan data rating
        self.load_rating()  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminPemesananMakanan()
    window.show()
    sys.exit(app.exec_())
