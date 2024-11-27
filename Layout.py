import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox, QHBoxLayout, QTextEdit
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class FoodDeliveryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kaciw Food Delivery")
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("background-color: #f0f0f0;")  

        self.layout = QVBoxLayout()             
        self.layout.setAlignment(Qt.AlignTop)

        self.title_label = QLabel("Kaciw Food Delivery")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.label = QLabel("Pilih Makanan:")
        self.label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.label)

        self.food_list = QListWidget()
        self.food_list.addItems(["Nasi Goreng", "Mie Ayam", "Sate Ayam", "Rendang", "Burger"])
        self.layout.addWidget(self.food_list)

        self.order_button = QPushButton("Pesan Sekarang")
        self.order_button.setFont(QFont("Arial", 12))
        self.order_button.setStyleSheet("background-color: ; color : white; padding: 10px; border: none; border-radius: 5px;")
        self.order_button.clicked.connect(self.place_order)
        self.layout.addWidget(self.order_button)

        self.order_summary_label = QLabel("Pesanan Anda:")
        self.order_summary_label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.order_summary_label)

        self.order_summary = QTextEdit()
        self.order_summary.setReadOnly(True)
        self.order_summary.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        self.layout.addWidget(self.order_summary)

        self.setLayout(self.layout)

    def place_order(self):
        selected_food = self.food_list.currentItem()
        if selected_food is None:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih makanan terlebih dahulu!")
        else:
            order_text = f"Anda telah memesan: {selected_food.text()}\n"
            self.order_summary.append(order_text)
            QMessageBox.information(self, "Pesanan Diterima", f"Anda telah memesan: {selected_food.text()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FoodDeliveryApp()
    window.show()
    sys.exit(app.exec_())