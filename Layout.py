import sys
import json
import os
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QMessageBox, QTableWidget, QTableWidgetItem, QTabWidget, QGridLayout, QScrollArea,
    QTextEdit, QDialog, QLineEdit, QRadioButton, QButtonGroup, QInputDialog, 
    QMenu, QAction, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class MembershipDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Daftar Membership")
        self.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout()
        
        # Header Membership
        header_label = QLabel("Program Membership Kaciw Food")
        header_label.setFont(QFont("Arial", 14, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)
        
        # Penjelasan Membership
        desc_label = QLabel("""
        Keuntungan Membership:
        • Diskon 10% setiap pembelian
        • Gratis ongkos kirim
        • Akumulasi poin reward
        • Akses promo eksklusif
        """)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Form Pendaftaran
        form_layout = QVBoxLayout()
        
        # Input Nama
        nama_layout = QHBoxLayout()
        nama_label = QLabel("Nama Lengkap:")
        self.nama_input = QLineEdit()
        nama_layout.addWidget(nama_label)
        nama_layout.addWidget(self.nama_input)
        form_layout.addLayout(nama_layout)
        
        # Input Nomor HP
        hp_layout = QHBoxLayout()
        hp_label = QLabel("Nomor HP:")
        self.hp_input = QLineEdit()
        hp_layout.addWidget(hp_label)
        hp_layout.addWidget(self.hp_input)
        form_layout.addLayout(hp_layout)
        
        layout.addLayout(form_layout)
        
        # Tombol Daftar
        daftar_btn = QPushButton("Daftar Sekarang")
        daftar_btn.clicked.connect(self.accept)
        layout.addWidget(daftar_btn)
        
        self.setLayout(layout)
    
    def get_membership_data(self):
        return {
            "nama": self.nama_input.text(),
            "nomor_hp": self.hp_input.text(),
            "tanggal_daftar": datetime.now().strftime("%d-%m-%Y"),
            "poin": 0
        }

class FoodDeliveryApp(QWidget):
    def __init__(self):
        super().__init__()

        # Inisialisasi data tambahan
        self.membership_file = "membership_data.json"
        self.membership_data = self.load_membership()
        self.order_history_file = "order_history.json"
        self.order_history = self.load_order_history()

        # ... [kode sebelumnya]

        # Tambahkan Tab Membership
        membership_tab = QWidget()
        membership_layout = QVBoxLayout()
        
        # Status Membership
        self.membership_status_label = QLabel("Status Membership: Belum Terdaftar")
        self.membership_status_label.setFont(QFont("Arial", 12, QFont.Bold))
        membership_layout.addWidget(self.membership_status_label)
        
        # Tombol Daftar Membership
        daftar_membership_btn = QPushButton("Daftar Membership")
        daftar_membership_btn.clicked.connect(self.daftar_membership)
        membership_layout.addWidget(daftar_membership_btn)
        
        # Area Poin dan Riwayat
        poin_layout = QHBoxLayout()
        
        # Label Poin
        self.poin_label = QLabel("Poin: 0")
        self.poin_label.setFont(QFont("Arial", 10))
        poin_layout.addWidget(self.poin_label)
        
        # Tombol Tukar Poin
        tukar_poin_btn = QPushButton("Tukar Poin")
        tukar_poin_btn.clicked.connect(self.tukar_poin)
        poin_layout.addWidget(tukar_poin_btn)
        
        membership_layout.addLayout(poin_layout)
        
        # Riwayat Pesanan
        riwayat_label = QLabel("Riwayat Pesanan:")
        membership_layout.addWidget(riwayat_label)
        
        self.riwayat_table = QTableWidget()
        self.riwayat_table.setColumnCount(4)
        self.riwayat_table.setHorizontalHeaderLabels(["Tanggal", "Total Pesanan", "Poin Didapat", "Detail"])
        membership_layout.addWidget(self.riwayat_table)
        
        membership_tab.setLayout(membership_layout)
        
        # Tambahkan Tab Membership ke Tab Widget
        self.tab_widget.addTab(membership_tab, "Membership")
        
        # Update status membership
        self.update_membership_status()

    def update_order_total(self, total):
        # Tambahkan logika poin dan riwayat pesanan
        if self.membership_data:
            # Hitung poin (1 poin per 10.000)
            poin_didapat = total // 10000
            
            # Update data membership
            self.membership_data['poin'] += poin_didapat
            
            # Simpan riwayat pesanan
            order_entry = {
                "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "total": total,
                "poin_didapat": poin_didapat
            }
            self.order_history.append(order_entry)
            
            # Simpan perubahan
            self.save_membership()
            self.save_order_history()
            
            # Update tampilan
            self.update_membership_status()
            self.load_order_history_table()

    def daftar_membership(self):
        # Tampilkan dialog pendaftaran
        dialog = MembershipDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            membership_data = dialog.get_membership_data()
            
            # Validasi input
            if not membership_data["nama"] or not membership_data["nomor_hp"]:
                QMessageBox.warning(self, "Peringatan", "Nama dan Nomor HP tidak boleh kosong!")
                return
            
            # Simpan data membership
            self.membership_data = membership_data
            self.save_membership()
            
            # Update status
            self.update_membership_status()
    
    def update_membership_status(self):
        # Update label status membership
        if self.membership_data:
            status_text = f"Status Membership: Aktif\n"
            status_text += f"Nama: {self.membership_data['nama']}\n"
            status_text += f"Poin: {self.membership_data.get('poin', 0)}"
            
            self.membership_status_label.setText(status_text)
            self.poin_label.setText(f"Poin: {self.membership_data.get('poin', 0)}")
        else:
            self.membership_status_label.setText("Status Membership: Belum Terdaftar")
            self.poin_label.setText("Poin: 0")
        
        # Muat riwayat pesanan
        self.load_order_history_table()
    
    def tukar_poin(self):
        # Cek apakah sudah ada membership
        if not self.membership_data:
            QMessageBox.warning(self, "Peringatan", "Silakan daftar membership terlebih dahulu!")
            return
        
        # Ambil poin saat ini
        current_poin = self.membership_data.get('poin', 0)
        
        # Dialog pilihan hadiah
        hadiah_options = [
            ("Diskon 20% (50 Poin)", 50),
            ("Gratis Ongkir (100 Poin)", 100),
            ("Voucher Rp 25.000 (150 Poin)", 150)
        ]
        
        # Buat menu pilihan
        hadiah_menu = QMenu(self)
        for hadiah, poin_dibutuhkan in hadiah_options:
            action = QAction(f"{hadiah} (Butuh {poin_dibutuhkan} Poin)", self)
            action.triggered.connect(lambda checked, h=hadiah, p=poin_dibutuhkan: self.proses_tukar_poin(h, p))
            hadiah_menu.addAction(action)
        
        # Tampilkan menu
        hadiah_menu.exec_(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))
    
    def proses_tukar_poin(self, hadiah, poin_dibutuhkan):
        # Cek apakah poin mencukupi
        current_poin = self.membership_data.get('poin', 0)
        if current_poin < poin_dibutuhkan:
            QMessageBox.warning(self, "Peringatan", "Poin tidak mencukupi!")
            return
        
        # Konfirmasi penukaran
        konfirmasi = QMessageBox.question(
            self, "Konfirmasi", 
            f"Tukar {poin_dibutuhkan} poin untuk {hadiah}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if konfirmasi == QMessageBox.Yes:
            # Kurangi poin
            self.membership_data['poin'] -= poin_dibutuhkan
            self.save_membership()
            
            # Tampilkan pesan berhasil
            QMessageBox.information(
                self, "Berhasil", 
                f"Selamat! Anda berhasil menukarkan {hadiah}"
            )
            
            # Update status
            self.update_membership_status()
    
    def load_order_history_table(self):
        # Bersihkan tabel
        self.riwayat_table.setRowCount(0)
        
        # Tampilkan riwayat pesanan
        for order in reversed(self.order_history):
            row = self.riwayat_table.rowCount()
            self.riwayat_table.insertRow(row)
            
            # Kolom Tanggal
            self.riwayat_table.setItem(row, 0, QTableWidgetItem(order['tanggal']))
            
            # Kolom Total Pesanan
            self.riwayat_table.setItem(row, 1, QTableWidgetItem(f"Rp {order['total']:,}"))
            
            # Kolom Poin Didapat
            self.riwayat_table.setItem(row, 2, QTableWidgetItem(str(order['poin_didapat'])))
            
            # Kolom Detail (bisa ditambahkan detail pesanan di masa mendatang)
            detail_btn = QPushButton("Lihat Detail")
            self.riwayat_table.setCellWidget(row, 3, detail_btn)
    
    def save_membership(self):
        # Simpan data membership ke file JSON
        try:
            with open(self.membership_file, 'w') as f:
                json.dump(self.membership_data, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan data membership: {str(e)}")
    
    def load_membership(self):
        # Muat data membership dari file JSON
        try:
            if os.path.exists(self.membership_file):
                with open(self.membership_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data membership: {str(e)}")
        return None
    
    def save_order_history(self):
        # Simpan riwayat pesanan ke file JSON
        try:
            with open(self.order_history_file, 'w') as f:
                json.dump(self.order_history, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan riwayat pesanan: {str(e)}")
    
    def load_order_history(self):
        # Muat riwayat pesanan dari file JSON
        try:
            if os.path.exists(self.order_history_file):
                with open(self.order_history_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat riwayat pesanan: {str(e)}")
        return []
    
    def update_cart_table(self):
        # Override metode sebelumnya untuk menambahkan perhitungan poin
        super().update_cart_table()
        
        # Hitung total pesanan
        total = sum(data['price'] * data['quantity'] for data in self.cart.values())
        
        # Update poin untuk membership
        if self.membership_data:
            # Terapkan diskon 10% untuk member
            total *= 0.9
        
        # Panggil metode update total order (untuk membership)
        self.update_order_total(total)

# ... [sisa kode sama seperti sebelumnya] ...
