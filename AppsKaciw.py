import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
data_file = "data_login.txt"


class UserManager:
    def __init__(self, data_file):
        self.data_file = data_file

    def load_users(self):
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, "r") as file:
            lines = file.readlines()
        return [{"username": line.split(",")[0], "password": line.split(",")[1].strip()} for line in lines]

    def save_user(self, username, password):
        with open(self.data_file, "a") as file:
            file.write(f"{username},{password}\n")

    def add_user(self, username, password):
        users = self.load_users()
        if any(user['username'] == username for user in users):
            return False
        self.save_user(username, password)
        return True

    def validate_login(self, username, password):
        users = self.load_users()
        return any(user['username'] == username and user['password'] == password for user in users)



class RegistrationDialog(QDialog):
    def __init__(self, user_manager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.setWindowTitle('Registrasi Akun Baru')
        self.setGeometry(300, 300, 400, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: ;
                color: white;
                border: none;
                padding: 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color:  rgb(68, 116, 120);
            }
        """)

        layout = QVBoxLayout()
        title_label = QLabel('Buat Akun Baru')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color:  rgb(68, 116, 120);
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        username_layout = QVBoxLayout()
        username_label = QLabel('Username')
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        password_layout = QVBoxLayout()
        password_label = QLabel('Password')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        confirm_password_layout = QVBoxLayout()
        confirm_password_label = QLabel('Konfirmasi Password')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        confirm_password_layout.addWidget(confirm_password_label)
        confirm_password_layout.addWidget(self.confirm_password_input)
        layout.addLayout(confirm_password_layout)

        register_btn = QPushButton('Daftar')
        register_btn.clicked.connect(self.register)
        layout.addWidget(register_btn)

        # login_link = QLabel('Sudah punya akun? <a href="#login">Login</a>')
        # login_link.setOpenExternalLinks(True)
        # login_link.setAlignment(Qt.AlignCenter)
        # layout.addWidget(login_link)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Registrasi Gagal', 'Semua field harus diisi')
            return

        if password != confirm_password:
            QMessageBox.warning(self, 'Registrasi Gagal', 'Password tidak cocok')
            return

        if self.user_manager.add_user(username, password):
            QMessageBox.information(self, 'Registrasi Berhasil', 'Akun berhasil dibuat')
            self.accept()
        else:
            QMessageBox.warning(self, 'Registrasi Gagal', 'Username sudah digunakan')


class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.user_manager = UserManager(data_file)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Kaciw Food Delivery')
        self.setGeometry(100, 100, 400, 500)
        self.setWindowIcon(QIcon('D:/Cool-Yeah/SEMESTER 1/Algoritma Pemrograman H/CODE/Ikon_Kaciw_Food_Delivery.png'))
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color:  rgb(68, 116, 120);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color:  rgb(68, 116, 120);
            }
        """)

        layout = QVBoxLayout()
        title_label = QLabel('Kaciw Food Delivery')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color:  rgb(68, 116, 120);
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        username_layout = QVBoxLayout()
        username_label = QLabel('Username')
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        password_layout = QVBoxLayout()
        password_label = QLabel('Password')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        register_btn = QPushButton('Daftar')
        register_btn.setStyleSheet("""
            background-color: white;
            color:  rgb(68, 116, 120);
            border: 2px solid  rgb(68, 116, 120);
        """)
        register_btn.clicked.connect(self.open_registration)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.user_manager.validate_login(username, password):
             QMessageBox.information(self, 'Login Berhasil', 'Selamat datang!')
             self.food_app = BestSellerRecommendationPage()
             self.food_app.show()
             self.hide()
        else:
            QMessageBox.warning(self, 'Login Gagal', 'Username atau password salah')


    def open_registration(self):
        registration_dialog = RegistrationDialog(self.user_manager, self)
        registration_dialog.exec_()


class BestSellerRecommendationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kaciw Food Delivery")
        self.setWindowIcon(QIcon('D:/Cool-Yeah/SEMESTER 1/Algoritma Pemrograman H/CODE/Ikon_Kaciw_Food_Delivery.png'))
        self.setGeometry(100, 100, 1200, 800)

        self.cart_items = []
        self.history_items = []
        
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari makanan...")
        self.search_input.textChanged.connect(self.filter_items)
        main_layout.addWidget(self.search_input)

        button_layout = QHBoxLayout()
        cart_btn = QPushButton("🛒 Keranjang")
        cart_btn.clicked.connect(self.show_cart)
        cart_btn.setStyleSheet("background-color: rgb(68, 116, 120); color: white; border-radius: 5px; padding: 5px;")
        
        history_btn = QPushButton("🧾 Riwayat")
        history_btn.clicked.connect(self.show_history)
        history_btn.setStyleSheet("background-color: rgb(68, 116, 120); color: white; border-radius: 5px; padding: 5px;")
        
        button_layout.addWidget(cart_btn)
        button_layout.addWidget(history_btn)
        main_layout.addLayout(button_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        
        main_layout.addWidget(scroll_area)
        
        self.setCentralWidget(main_container)

        self.original_categories = [
            {
                "category": "Makanan Tradisional",
                "items": [
                    {
                        "name": "Nasi Padang",
                        "restaurant": "Warung Mbah austin ",
                        "rating": 3.9,
                        "price": "Rp 25.000",
                        "description": "Nasgor gacor dengan sentuhan mbah"
                    },
                    {
                        "name": "Sate Ayam Maduro",
                        "restaurant": "Sate Raja Madura",
                        "rating": 4.8,
                        "price": "Rp 35.000",
                        "description": "Sate ayam dengan bumbu kacang khas Madura enaknyoooo"
                    },
                    {
                        "name": "Mie Ayam Guacorrr",
                        "restaurant": "Mie Ayam Kusman",
                        "rating": 4.6,
                        "price": "Rp 55.000",
                        "description": "Mie Ayam dengan kuah yang sangat enak dan gurih"
                    },
                ]
            },
            {
                "category": "Makanan Modern",
                "items": [
                    {
                        "name": "Austin Kebab",
                        "restaurant": "Austin Kebab gacor",
                        "rating": 4.7,
                        "price": "Rp 85.000",
                        "description": "Kebab asli Turkey Paling enak"
                    },
                    {
                        "name": "Salad Buah Mama Vaness",
                        "restaurant": "Benedict's Restaurant",
                        "rating": 5.0,
                        "price": "Rp 65.000",
                        "description": "Salad buah untuk menjaga kesehatanmu!"
                    },
                    {
                        "name": "Toast",
                        "restaurant": "Restaurant Vera's",
                        "rating": 4.6,
                        "price": "Rp 80.000",
                        "description": "Dengan rasa yang asli dan enak"
                    },
                ]
            }
        ]

        self.categories = self.original_categories.copy()
        self.display_categories()

    def create_best_seller_item(self, item):
        item_widget = QFrame()
        item_widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                border: 1px solid #E0E0E0;
                min-width: 250px;
                max-width: 300px;
            }
        """)

        layout = QVBoxLayout()

        name_label = QLabel(item['name'])
        name_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
        """)
        layout.addWidget(name_label)

        restaurant_label = QLabel(f"Dari: {item['restaurant']}")
        restaurant_label.setStyleSheet("color: gray;")
        layout.addWidget(restaurant_label)

        description_label = QLabel(item['description'])
        description_label.setStyleSheet("""
            font-style: italic;
            color: #666;
        """)
        layout.addWidget(description_label)

        rating_price_layout = QHBoxLayout()

        rating_label = QLabel(f"★ {item['rating']}")
        rating_label.setStyleSheet("""
            color: gold;
            font-weight: bold;
        """)
        rating_price_layout.addWidget(rating_label)

        price_label = QLabel(item['price'])
        price_label.setStyleSheet("""
            color:  rgb(68, 116, 120);
            font-weight: bold;
        """)
        rating_price_layout.addWidget(price_label)

        layout.addLayout(rating_price_layout)

        order_btn = QPushButton("Pesan")
        order_btn.setStyleSheet("""
            background-color:  rgb(68, 116, 120);
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
        """)
        order_btn.clicked.connect(lambda checked, i=item: self.customize_item(i))
        layout.addWidget(order_btn)

        item_widget.setLayout(layout)
        return item_widget

    def customize_item(self, item):
        dialog = MenuCustomizationDialog(item, self)
        quantity = dialog.exec_()

        if quantity > 0:
            cart_item = CartItem(item['name'], item['price'], quantity)
            existing_item = next((x for x in self.cart_items if x.name == item['name']), None)

            if existing_item:
                existing_item.quantity += quantity
                existing_item.total_price = existing_item.calculate_total_price()
            else:
                self.cart_items.append(cart_item)

    def show_cart(self):
        dialog = CartDialog(self.cart_items, self)
        dialog.exec_()

    def show_history(self):
        dialog = HistoryDialog(self.history_items, self)
        dialog.exec_()

    def filter_items(self):
        query = self.search_input.text().lower()
        self.categories = [
            {
                "category": cat["category"],
                "items": [
                    item for item in cat["items"] if query in item["name"].lower()
                ]
            }
            for cat in self.original_categories
        ]
        self.display_categories()

    def display_categories(self):
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().deleteLater()

        row, col = 0, 0
        for category in self.categories:
            if not category['items']:
                continue

            category_label = QLabel(category['category'])
            category_label.setStyleSheet("font-weight: bold; font-size: 20px;")
            self.scroll_layout.addWidget(category_label, row, 0, 1, 3)
            row += 1

            for item in category['items']:
                item_widget = self.create_best_seller_item(item)
                self.scroll_layout.addWidget(item_widget, row, col)
                col += 1
                if col > 2:
                    col = 0
                    row += 1
            row += 1

class CartItem:
    def __init__(self, name, price, quantity=1):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.total_price = self.calculate_total_price()

    def calculate_total_price(self):
        try:
            price_value = int(self.price.replace("Rp ", "").replace(".", ""))
            return price_value * self.quantity
        except (ValueError, TypeError):
            return 0


class CartDialog(QDialog):
    def __init__(self, cart_items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keranjang Pesanan")
        self.setGeometry(300, 300, 400, 500)
        self.cart_items = cart_items

        layout = QVBoxLayout()
        self.order_list = QListWidget()
        layout.addWidget(self.order_list)

        self.total_label = QLabel("Total: Rp 0")
        self.total_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(self.total_label)

        btn_layout = QHBoxLayout()

        remove_btn = QPushButton("Hapus Item")
        remove_btn.clicked.connect(self.remove_item)
        btn_layout.addWidget(remove_btn)

        edit_quantity_btn = QPushButton("Perbarui jumlah item")
        edit_quantity_btn.clicked.connect(self.edit_item_quantity)
        btn_layout.addWidget(edit_quantity_btn)

        layout.addLayout(btn_layout)

        payment_group = QButtonGroup(self)
        self.transfer_radio = QRadioButton("Transfer Bank")
        self.cod_radio = QRadioButton("Cash on Delivery (COD)")
        payment_group.addButton(self.transfer_radio)
        payment_group.addButton(self.cod_radio)

        layout.addWidget(QLabel("Pilih Metode Pembayaran:"))
        layout.addWidget(self.transfer_radio)
        layout.addWidget(self.cod_radio)

        order_btn = QPushButton("Check Out")
        order_btn.clicked.connect(self.process_order)
        layout.addWidget(order_btn)

        self.setLayout(layout)
        self.update_cart()

    def update_cart(self):
        self.order_list.clear()
        total = 0
        for item in self.cart_items:
            item_text = f"{item.name} x{item.quantity} - Rp {item.total_price:,}"
            list_item = QListWidgetItem(item_text)
            self.order_list.addItem(list_item)
            total += item.total_price

        self.total_label.setText(f"Total: Rp {total:,}")

    def remove_item(self):
        current_item = self.order_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "Hapus Item", "Pilih Item yang akan Dihapus")
            return

        index = self.order_list.row(current_item)

        del self.cart_items[index]
    
        self.update_cart()

    def reset_cart(self):
        reply = QMessageBox.question(
            self,
            "Reset Isi Keranjang"
            "Apakah Anda yakin ingin mengosongkan keranjang?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.cart_items.clear()
            self.update_cart()

    def edit_item_quantity(self):
        
        current_item = self.order_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(
                self,
                "Perbarui jumlah pesanan",
                "Pilih item yang ingin diperbarui!"    
            )
            return
        
        index = self.order_list.row(current_item)
        cart_item = self.cart_items[index]

        quantity, ok = QInputDialog.getInt(
            self,
            "Ubah Jumlah",
            "Masukkan jumlah baru: ",
            cart_item.quantity,
            1,
            100
            )

        if ok:
            cart_item.quantity = quantity
            cart_item.total_price = cart_item.calculate_total_price()

            self.update_cart()

    def process_order(self):
        if not self.cart_items:
            QMessageBox.warning(self, "Keranjang Kosong", "Tambahkan item ke keranjang terlebih dahulu.")
            return

        if not self.transfer_radio.isChecked() and not self.cod_radio.isChecked():
            QMessageBox.warning(self, "Error", "Pilih metode pembayaran!")
            return

        else:
            reply = QMessageBox.question(
            self,
            "Konfirmasi Pesanan",
            "Apakah Anda yakin ingin memproses pesanan?",
            QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                
                for item in self.cart_items:
                    item_checkout =     (f"{item.name} x{item.quantity} - Rp {item.total_price:,}")
                    self.parent().history_items.append(item_checkout)

                QMessageBox.information(self, "Pesanan Berhasil", "Terima kasih telah memesan!")
                
                self.cart_items.clear()
                self.update_cart()
                self.accept()


class RatingDialog(QDialog):
    def __init__(self, item_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Rating untuk {item_name}")
        self.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout()
        
        item_label = QLabel(f"Item: {item_name}")
        item_label.setFont(QFont('Arial', 12))
        layout.addWidget(item_label)
        
        rating_layout = QHBoxLayout()
        self.rating_buttons = []
        rating_label = QLabel("Rating Makanan:")
        rating_layout.addWidget(rating_label)
        
        for i in range(5, 0, -1):
            radio_btn = QRadioButton(str(i))
            radio_btn.setStyleSheet("""
                QRadioButton { 
                    color: blue; 
                    margin-right: 10px;
                }
                QRadioButton::indicator { 
                    width: 20px; 
                    height: 20px; 
                }
                QRadioButton:checked { 
                    font-weight: bold; 
                }
            """)
            rating_layout.addWidget(radio_btn)
            self.rating_buttons.append(radio_btn)
        
        layout.addLayout(rating_layout)
        
        order_comment_label = QLabel("Komentar Pesanan:")
        layout.addWidget(order_comment_label)
        
        self.order_comment_edit = QTextEdit()
        self.order_comment_edit.setPlaceholderText("Tulis komentar tentang pesanan Anda...")
        layout.addWidget(self.order_comment_edit)
        
        submit_btn = QPushButton("Kirim Ulasan")
        submit_btn.setStyleSheet("background-color: rgb(68, 116, 120); color: white; border-radius: 5px; padding: 5px;")
        submit_btn.clicked.connect(self.submit_rating)
        layout.addWidget(submit_btn)
        
        self.setLayout(layout)
        self.rating = None
        self.order_comment = ""
    
    def submit_rating(self):
        selected_rating = None
        for btn in self.rating_buttons:
            if btn.isChecked():
                selected_rating = int(btn.text())
                break
        
        if selected_rating is None:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih rating makanan!")
            return
        
        self.rating = selected_rating
        self.order_comment = self.order_comment_edit.toPlainText()
        
        if not self.order_comment:
            reply = QMessageBox.question(
                self, 
                "Konfirmasi", 
                "Anda belum menulis komentar. Lanjutkan?", 
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        self.accept()

class HistoryDialog(QDialog):
    def __init__(self, history_items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Riwayat Pesanan")
        self.setGeometry(300, 300, 500, 600)
        
        layout = QVBoxLayout()
        
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        
        add_rating_btn = QPushButton("Tambahkan Ulasan")
        add_rating_btn.setStyleSheet("background-color: rgb(68, 116, 120); color: white; border-radius: 5px; padding: 5px;")
        add_rating_btn.clicked.connect(self.add_rating)
        layout.addWidget(add_rating_btn)
        
        self.setLayout(layout)
        
        self.history_items = history_items

        self.update_history()
    
    def update_history(self):
        self.history_list.clear()
        for item in self.history_items:
            list_item = QListWidgetItem(item)
            
            self.history_list.addItem(list_item)
    
    def add_rating(self):
        current_item = self.history_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Peringatan", "Pilih item yang ingin diberi rating")
            return
        
        item_name = current_item.text()
    
        rating_dialog = RatingDialog(item_name, self)
        
        if rating_dialog.exec_() == QDialog.Accepted:
            rating_text = (
                f"{item_name}\n"
                f"Rating: {'★' * rating_dialog.rating} ({rating_dialog.rating}/5)\n"
                f"Komentar: {rating_dialog.order_comment}"
            )
            
            current_item.setText(rating_text)
            
            QMessageBox.information(
                self, 
                "Berhasil", 
                f"Ulasan untuk {item_name} telah disimpan!"
            )

class MenuCustomizationDialog(QDialog):
    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Pesan {item['name']}")
        self.setGeometry(300, 300, 400, 500)
        self.item = item
        self.quantity = 1

        layout = QVBoxLayout()

        name_label = QLabel(item['name'])
        name_label.setStyleSheet("font-weight: bold; font-size: 20px;")
        layout.addWidget(name_label)

        desc_label = QLabel(item['description'])
        layout.addWidget(desc_label)

        price_label = QLabel(f"Harga: {item['price']}")
        layout.addWidget(price_label)

        quantity_layout = QHBoxLayout()
        minus_btn = QPushButton("-")
        minus_btn.clicked.connect(self.decrease_quantity)
        plus_btn = QPushButton("+")
        plus_btn.clicked.connect(self.increase_quantity)

        self.quantity_label = QLabel(str(self.quantity))
        self.quantity_label.setAlignment(Qt.AlignCenter)

        quantity_layout.addWidget(minus_btn)
        quantity_layout.addWidget(self.quantity_label)
        quantity_layout.addWidget(plus_btn)

        layout.addLayout(quantity_layout)

        add_to_cart_btn = QPushButton("Tambah ke Keranjang")
        add_to_cart_btn.clicked.connect(self.add_to_cart)
        layout.addWidget(add_to_cart_btn)

        self.setLayout(layout)

    def increase_quantity(self):
        self.quantity += 1
        self.quantity_label.setText(str(self.quantity))

    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.quantity_label.setText(str(self.quantity))

    def add_to_cart(self):
        self.done(self.quantity)

def main():
    app = QApplication(sys.argv) 
    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
