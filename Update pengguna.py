import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QScrollArea, QGridLayout, QFrame,
    QDialog, QRadioButton, QButtonGroup, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class ShoppingCart:
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
        
    def remove_item(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)
        
    def get_total(self):
        total = 0
        for item in self.items:
            price = int(item['price'].replace('Rp ', '').replace('.', ''))
            total += price
        return total
    
    def clear(self):
        self.items = []

class CartDialog(QDialog):
    def __init__(self, cart, parent=None):
        super().__init__(parent)
        self.cart = cart
        self.parent = parent
        self.setWindowTitle("Keranjang Belanja")
        self.setGeometry(200, 200, 400, 500)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Display cart items
        for index, item in enumerate(self.cart.items):
            item_widget = QFrame()
            item_layout = QHBoxLayout()
            
            # Item details
            details_layout = QVBoxLayout()
            name_label = QLabel(f"{item['name']}")
            restaurant_label = QLabel(f"Dari: {item['restaurant']}")
            price_label = QLabel(item['price'])
            
            details_layout.addWidget(name_label)
            details_layout.addWidget(restaurant_label)
            details_layout.addWidget(price_label)
            
            # Delete button
            delete_btn = QPushButton("Hapus")
            delete_btn.setStyleSheet("""
                background-color: #FF4444;
                color: white;
                padding: 5px;
                border-radius: 3px;
            """)
            delete_btn.clicked.connect(lambda checked, idx=index: self.delete_item(idx))
            
            item_layout.addLayout(details_layout)
            item_layout.addWidget(delete_btn)
            
            item_widget.setLayout(item_layout)
            item_widget.setStyleSheet("border: 1px solid #E0E0E0; padding: 10px; margin: 5px;")
            layout.addWidget(item_widget)
        
        # Display total
        total = self.cart.get_total()
        total_label = QLabel(f"Total: Rp {total:,}")
        total_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(total_label)
        
        # Payment options
        payment_group = QButtonGroup(self)
        transfer_radio = QRadioButton("Transfer Bank")
        cod_radio = QRadioButton("Cash on Delivery (COD)")
        payment_group.addButton(transfer_radio)
        payment_group.addButton(cod_radio)
        
        layout.addWidget(QLabel("Pilih Metode Pembayaran:"))
        layout.addWidget(transfer_radio)
        layout.addWidget(cod_radio)
        
        # Checkout button
        checkout_btn = QPushButton("Bayar Sekarang")
        checkout_btn.setStyleSheet("""
            background-color: #9932CC;
            color: white;
            padding: 10px;
            border-radius: 5px;
        """)
        checkout_btn.clicked.connect(lambda: self.process_payment(payment_group))
        layout.addWidget(checkout_btn)
        
        self.setLayout(layout)
    
    def delete_item(self, index):
        self.cart.remove_item(index)
        self.parent.cart_btn.setText(f"Lihat Keranjang ({len(self.cart.items)})")
        self.close()
        if self.cart.items:
            CartDialog(self.cart, self.parent).exec_()
    
    def process_payment(self, payment_group):
        selected_button = payment_group.checkedButton()
        if not selected_button:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih metode pembayaran!")
            return
            
        payment_method = selected_button.text()
        msg = QMessageBox()
        msg.setWindowTitle("Pembayaran Berhasil")
        msg.setText(f"Pembayaran via {payment_method} berhasil!\nTerima kasih telah berbelanja.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        
        self.cart.clear()
        self.accept()

class BestSellerRecommendationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cart = ShoppingCart()
        self.setWindowTitle("Rekomendasi Best Seller Makanan")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main Container
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Scroll Area for Best Seller Recommendations
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        # Best Seller Categories
        categories = [
            {
                "category": "Makanan Tradisional",
                "items": [
                    {
                        "name": "Nasi Goreng Kampung",
                        "restaurant": "Warung Mbah Marijan",
                        "rating": 4.9,
                        "price": "Rp 25.000",
                        "description": "Nasi goreng autentik dengan bumbu tradisional"
                    },
                    {
                        "name": "Sate Ayam Madura",
                        "restaurant": "Sate Raja Madura",
                        "rating": 4.8,
                        "price": "Rp 35.000",
                        "description": "Sate ayam dengan bumbu kacang khas Madura"
                    }
                ]
            },
            {
                "category": "Makanan Modern",
                "items": [
                    {
                        "name": "Burger Truffle Wagyu",
                        "restaurant": "Burger Artisan",
                        "rating": 4.7,
                        "price": "Rp 85.000",
                        "description": "Burger premium dengan daging wagyu dan truffle"
                    },
                    {
                        "name": "Sushi Salmon Roll",
                        "restaurant": "Sushi Master",
                        "rating": 4.6,
                        "price": "Rp 65.000",
                        "description": "Sushi roll dengan salmon premium"
                    }
                ]
            },
            {
                "category": "Street Food",
                "items": [
                    {
                        "name": "Bakso Jumbo Pedas",
                        "restaurant": "Bakso Bang Jago",
                        "rating": 4.8,
                        "price": "Rp 20.000",
                        "description": "Bakso berukuran jumbo dengan bumbu pedas"
                    },
                    {
                        "name": "Martabak Manis Special",
                        "restaurant": "Martabak 88",
                        "rating": 4.7,
                        "price": "Rp 35.000",
                        "description": "Martabak manis dengan topping berlimpah"
                    }
                ]
            }
        ]
        
        # Add Categories and Items to Layout
        for category_index, category in enumerate(categories):
            category_label = QLabel(category['category'])
            category_label.setStyleSheet("""
                font-size: 20px;
                font-weight: bold;
                color: #9932CC;
                padding: 15px 0;
            """)
            scroll_layout.addWidget(category_label, category_index * 3, 0, 1, 2)
            
            for item_index, item in enumerate(category['items']):
                item_widget = self.create_best_seller_item(item)
                scroll_layout.addWidget(item_widget, category_index * 3 + 1, item_index)
        
        main_layout.addWidget(scroll_area)
        
        # Cart Button
        self.cart_btn = QPushButton("Lihat Keranjang (0)")
        self.cart_btn.setStyleSheet("""
            background-color: #9932CC;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin: 10px;
        """)
        self.cart_btn.clicked.connect(self.show_cart)
        main_layout.addWidget(self.cart_btn)
        
        self.setCentralWidget(main_container)
    
    def create_header(self):
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #9932CC;
                padding: 20px;
            }
        """)
        
        header_layout = QHBoxLayout()
        
        title = QLabel("Rekomendasi Best Seller")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        
        search_btn = QPushButton("Cari Makanan")
        search_btn.setStyleSheet("""
            background-color: white;
            color: #9932CC;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        """)
        header_layout.addWidget(search_btn)
        
        header.setLayout(header_layout)
        return header
    
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
            QFrame:hover {
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transform: scale(1.02);
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
            color: #9932CC;
            font-weight: bold;
        """)
        rating_price_layout.addWidget(price_label)
        
        layout.addLayout(rating_price_layout)
        
        order_btn = QPushButton("Pesan Sekarang")
        order_btn.setStyleSheet("""
            background-color: #9932CC;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
        """)
        order_btn.clicked.connect(lambda: self.add_to_cart(item))
        layout.addWidget(order_btn)
        
        item_widget.setLayout(layout)
        return item_widget
    
    def add_to_cart(self, item):
        self.cart.add_item(item)
        self.cart_btn.setText(f"Lihat Keranjang ({len(self.cart.items)})")
        QMessageBox.information(self, "Sukses", f"{item['name']} ditambahkan ke keranjang!")
    
    def show_cart(self):
        if not self.cart.items:
            QMessageBox.information(self, "Keranjang Kosong", "Silakan pilih makanan terlebih dahulu!")
            return
            
        cart_dialog = CartDialog(self.cart, self)
        if cart_dialog.exec_() == QDialog.Accepted:
            self.cart_btn.setText("Lihat Keranjang (0)")

def main():
    app = QApplication(sys.argv)
    window = BestSellerRecommendationPage()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
