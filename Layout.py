import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QMessageBox, QTableWidget, QTableWidgetItem, QTabWidget, QGridLayout, QScrollArea
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class FoodDeliveryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.cart = {}
        self.menu_items = [
            {"name": "Nasi Goreng", "price": 25000, "desc": "Nasi goreng dengan telur spesial", "category": "Makanan Utama"},
            {"name": "Mie Ayam", "price": 20000, "desc": "Mie ayam kuah spesial", "category": "Makanan Utama"},
            {"name": "Sate Ayam", "price": 30000, "desc": "Sate ayam dengan bumbu kacang", "category": "Makanan Pendamping"},
            {"name": "Rendang", "price": 35000, "desc": "Rendang daging sapi empuk", "category": "Makanan Utama"},
            {"name": "Burger", "price": 40000, "desc": "Burger dengan daging premium", "category": "Fast Food"},
            {"name": "Es Teh", "price": 5000, "desc": "Es teh manis segar", "category": "Minuman"},
            {"name": "Jus Jeruk", "price": 15000, "desc": "Jus jeruk segar tanpa gula tambahan", "category": "Minuman"}
        ]

        self.setWindowTitle("Kaciw Food Delivery")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QWidget { background-color: #f4f4f4; }
            QPushButton { 
                background-color: #9932CC; 
                color: white; 
                padding: 7px; 
                border-radius: 5px; 
            }
            QPushButton:hover { 
                background-color: #9932CC; 
            }
        """)

        # Layout Utama
        main_layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # Tab Menu
        menu_tab = QWidget()
        menu_layout = QVBoxLayout()

        # Tombol Kategori
        category_layout = QHBoxLayout()
        categories = ["Semua", "Makanan Utama", "Makanan Pendamping", "Fast Food", "Minuman"]
        self.category_buttons = {}
        
        for category in categories:
            btn = QPushButton(category)
            btn.setFixedHeight(30)
            btn.clicked.connect(lambda checked, cat=category: self.filter_menu(cat))
            category_layout.addWidget(btn)
            self.category_buttons[category] = btn

        menu_layout.addLayout(category_layout)

        # Scroll Area untuk Grid Makanan
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.food_grid_widget = QWidget()
        self.food_grid = QGridLayout(self.food_grid_widget)
        self.scroll_area.setWidget(self.food_grid_widget)
        self.populate_food_grid()
        menu_layout.addWidget(self.scroll_area)
        menu_tab.setLayout(menu_layout)

        # Tab Keranjang
        cart_tab = QWidget()
        cart_layout = QVBoxLayout()
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(4)
        self.cart_table.setHorizontalHeaderLabels(["Nama", "Harga", "Jumlah", "Total"])
        cart_layout.addWidget(self.cart_table)
        self.cart_total_label = QLabel("Total: Rp 0")
        self.cart_total_label.setFont(QFont("Arial", 14, QFont.Bold))
        cart_layout.addWidget(self.cart_total_label)
        clear_cart_btn = QPushButton("Kosongkan Keranjang")
        clear_cart_btn.clicked.connect(self.clear_cart)
        cart_layout.addWidget(clear_cart_btn)
        cart_tab.setLayout(cart_layout)

        # Tambahkan Tab
        self.tab_widget.addTab(menu_tab, "Menu")
        self.tab_widget.addTab(cart_tab, "Keranjang")
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def populate_food_grid(self, filtered_indices=None):
        # Bersihkan grid sebelumnya
        for i in reversed(range(self.food_grid.count())): 
            self.food_grid.itemAt(i).widget().setParent(None)

        # Gunakan semua indeks jika tidak ada filter
        if filtered_indices is None:
            filtered_indices = range(len(self.menu_items))

        row, col = 0, 0
        for idx in filtered_indices:
            # Widget untuk setiap item makanan
            food_widget = QWidget()
            food_layout = QVBoxLayout()
            food_layout.setSpacing(5)

            # Label nama
            name_label = QLabel(self.menu_items[idx]["name"])
            name_label.setFont(QFont("Arial", 12, QFont.Bold))
            food_layout.addWidget(name_label)

            # Label harga
            price_label = QLabel(f"Rp {self.menu_items[idx]['price']:,}")
            price_label.setFont(QFont("Arial", 10))
            food_layout.addWidget(price_label)

            # Label deskripsi
            desc_label = QLabel(self.menu_items[idx]["desc"])
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: gray; font-size: 10pt;")
            food_layout.addWidget(desc_label)

            # Tombol tambah ke keranjang
            add_btn = QPushButton("Tambah")
            add_btn.clicked.connect(lambda checked, i=idx: self.add_to_cart(i))
            food_layout.addWidget(add_btn)

            food_widget.setLayout(food_layout)
            food_widget.setStyleSheet("""
                QWidget { 
                    background-color: white; 
                    border: 1px solid #ddd; 
                    border-radius: 5px; 
                    padding: 10px; 
                }
            """)

            self.food_grid.addWidget(food_widget, row, col)
            
            col += 1
            if col > 2:  # 3 kolom
                col = 0
                row += 1

    def filter_menu(self, category):
        # Sorot tombol kategori yang dipilih
        for btn in self.category_buttons.values():
            btn.setStyleSheet("background-color: #9932CC; color: white;")
        if category in self.category_buttons:
            self.category_buttons[category].setStyleSheet("background-color:#9932CC; color: white;")

        # Filter menu
        if category == "Semua":
            filtered_indices = range(len(self.menu_items))
        else:
            filtered_indices = [i for i, item in enumerate(self.menu_items) if item["category"] == category]

        # Perbarui grid dengan menu terfilter
        self.populate_food_grid(filtered_indices)

    def add_to_cart(self, index):
        item = self.menu_items[index]
        if item["name"] in self.cart:
            self.cart[item["name"]]["quantity"] += 1
        else:
            self.cart[item["name"]] = {"price": item["price"], "quantity": 1}
        self.update_cart_table()
        QMessageBox.information(self, "Keranjang", f"{item['name']} ditambahkan ke keranjang!")

    def update_cart_table(self):
        self.cart_table.setRowCount(0)
        total = 0
        for name, data in self.cart.items():
            row = self.cart_table.rowCount()
            self.cart_table.insertRow(row)
            self.cart_table.setItem(row, 0, QTableWidgetItem(name))
            self.cart_table.setItem(row, 1, QTableWidgetItem(f"Rp {data['price']:,}"))
            self.cart_table.setItem(row, 2, QTableWidgetItem(str(data["quantity"])))
            total_item = data["price"] * data["quantity"]
            self.cart_table.setItem(row, 3, QTableWidgetItem(f"Rp {total_item:,}"))
            total += total_item
        self.cart_total_label.setText(f"Total: Rp {total:,}")

    def clear_cart(self):
        self.cart.clear()
        self.update_cart_table()
        QMessageBox.information(self, "Keranjang", "Keranjang telah dikosongkan!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FoodDeliveryApp()
    window.show()
    sys.exit(app.exec_())
