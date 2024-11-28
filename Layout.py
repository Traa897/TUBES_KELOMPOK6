import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QTabWidget, 
    QGridLayout, QScrollArea, QLineEdit, QFrame, QDialog, QRadioButton, QButtonGroup
)
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QSize, QRect

class RoundedWidget(QWidget):
    def __init__(self, color=Qt.white, radius=10, parent=None):
        super().__init__(parent)
        self.color = color
        self.radius = radius
        self.setStyleSheet("background-color: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(self.color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)

class RestaurantItem(RoundedWidget):
    def __init__(self, restaurant_data, parent=None):
        super().__init__(parent=parent)
        self.restaurant_data = restaurant_data
        layout = QVBoxLayout()

        # Restaurant Image (Placeholder)
        self.image_label = QLabel()
        self.image_label.setFixedSize(250, 150)
        self.image_label.setStyleSheet("""
            background-color: #E0E0E0;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)

        # Restaurant Details
        name_label = QLabel(restaurant_data['name'])
        name_label.setStyleSheet("font-weight: bold; font-size: 16px;")

        details_label = QLabel(f"{restaurant_data['cuisine']} • {restaurant_data['distance']} km")
        details_label.setStyleSheet("color: gray;")

        rating_label = QLabel(f"★ {restaurant_data['rating']}")
        rating_label.setStyleSheet("color: orange;")

        layout.addWidget(self.image_label)
        layout.addWidget(name_label)
        layout.addWidget(details_label)
        layout.addWidget(rating_label)

        self.setLayout(layout)
        self.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        """)

class FoodDeliveryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kaciw FooD")
        self.setGeometry(100, 100, 1000, 800)
        
        # Sophisticated color palette
        self.setStyleSheet("""
            QMainWindow { background-color: #F5F5F5; }
            QPushButton { 
                background-color:#9932CC; 
                color: white; 
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { 
                background-color: #9932CC; 
            }
        """)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Search and Filter Section
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari restoran atau makanan...")
        self.search_input.setStyleSheet("""
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
        """)
        search_layout.addWidget(self.search_input)

        filter_btn = QPushButton("Filter")
        filter_btn.clicked.connect(self.show_filter_dialog)
        search_layout.addWidget(filter_btn)

        main_layout.addLayout(search_layout)

        # Restaurants Section
        restaurants_scroll = QScrollArea()
        restaurants_widget = QWidget()
        restaurants_grid = QGridLayout(restaurants_widget)
        restaurants_scroll.setWidget(restaurants_widget)
        restaurants_scroll.setWidgetResizable(True)

        # Sample Restaurant Data
        restaurants = [
            {"name": "Nasi Padang bulan", "cuisine": "kilo 50", "distance": 1.2, "rating": 4.5},
            {"name": "Eagan gado gado", "cuisine": "kampung baru", "distance": 2.5, "rating": 4.8},
            {"name": "Austin Kebab", "cuisine": "Bangun Reksa", "distance": 0.8, "rating": 4.2},
            {"name": "Mie Ayam", "cuisine": "Rapak", "distance": 3.0, "rating": 4.6},
        ]

        row, col = 0, 0
        for restaurant in restaurants:
            restaurant_item = RestaurantItem(restaurant)
            restaurants_grid.addWidget(restaurant_item, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        main_layout.addWidget(restaurants_scroll)

    def show_filter_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Filter Restoran")
        layout = QVBoxLayout()

        # Kategori Filter
        kategori_group = QButtonGroup()
        kategori_label = QLabel("Kategori Makanan:")
        kategori_options = ["Semua", "kilo 50", "", "Fast Food", "Vegetarian"]
        
        for option in kategori_options:
            radio = QRadioButton(option)
            kategori_group.addButton(radio)
            layout.addWidget(radio)

        # Jarak Filter
        jarak_group = QButtonGroup()
        jarak_label = QLabel("Jarak Maksimum:")
        jarak_options = ["< 5 km", "25 km", "> 50km"]
        
        for option in jarak_options:
            radio = QRadioButton(option)
            jarak_group.addButton(radio)
            layout.addWidget(radio)

        # Rating Filter
        rating_group = QButtonGroup()
        rating_label = QLabel("Rating Minimal:")
        rating_options = ["★ 3.5", "★ 4.0", "★ 4.5"]
        
        for option in rating_options:
            radio = QRadioButton(option)
            rating_group.addButton(radio)
            layout.addWidget(radio)

        apply_btn = QPushButton("Terapkan Filter")
        apply_btn.clicked.connect(dialog.accept)
        layout.addWidget(apply_btn)

        dialog.setLayout(layout)
        dialog.exec_()

def main():
    app = QApplication(sys.argv)
    window = FoodDeliveryApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
