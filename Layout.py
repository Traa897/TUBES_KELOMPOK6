import sys
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

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
    def __init__(self, restaurant_data, favorite_meals_list, parent=None):
        super().__init__(parent=parent)
        self.restaurant_data = restaurant_data
        self.favorite_meals_list = favorite_meals_list
        self.comments = []

        layout = QVBoxLayout()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(4)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 80)) 
        self.setGraphicsEffect(shadow)

        self.image_label = QLabel("Image Placeholder")
        self.image_label.setFixedSize(250, 150)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            background-color: #E0E0E0;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)

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

        rating_layout = QVBoxLayout()
        rating_title = QLabel("Rating Makanan Favorit")
        rating_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        rating_layout.addWidget(rating_title)

        meal_layout = QHBoxLayout()
        self.meal_dropdown = QComboBox()
        self.meal_dropdown.addItems([
            "Pilih Makanan", 
            "Nasi Goreng", 
            "Sate", 
            "Bakso", 
            "Gado-gado", 
            "Mie Ayam"
        ])
        meal_layout.addWidget(self.meal_dropdown)

        self.rating_dropdown = QComboBox()
        self.rating_dropdown.addItems([
            "Rating", 
            "★", 
            "★★", 
            "★★★", 
            "★★★★", 
            "★★★★★"
        ])
        meal_layout.addWidget(self.rating_dropdown)

        self.add_favorite_btn = QPushButton("Tambah Favorit")
        self.add_favorite_btn.setStyleSheet("""
            background-color: #9932CC;
            color: white;
            border-radius: 5px;
            padding: 5px;
        """)
        self.add_favorite_btn.clicked.connect(self.add_to_favorites)
        meal_layout.addWidget(self.add_favorite_btn)

        rating_layout.addLayout(meal_layout)

        layout.addLayout(rating_layout)

        comment_layout = QVBoxLayout()
        comment_title = QLabel("Komentar")
        comment_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        comment_layout.addWidget(comment_title)

        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Tambahkan komentar...")
        self.comment_input.setStyleSheet("""
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
        """)

        self.comment_button = QPushButton("Kirim")
        self.comment_button.setStyleSheet("""
            background-color: #9932CC;
            color: white;
            border-radius: 5px;
            padding: 5px;
        """)
        self.comment_button.clicked.connect(self.add_comment)

        comment_layout.addWidget(self.comment_input)
        comment_layout.addWidget(self.comment_button)

        self.comments_display = QLabel()
        self.comments_display.setWordWrap(True)
        self.comments_display.setStyleSheet("""
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #F9F9F9;
            padding: 5px;
            font-size: 12px;
        """)
        comment_layout.addWidget(self.comments_display)

        layout.addLayout(comment_layout)
        self.setLayout(layout)
        self.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            /* Removed the box-shadow property here */
        """)

    def add_to_favorites(self):
        meal = self.meal_dropdown.currentText()
        rating = self.rating_dropdown.currentText()
        
        if meal != "Pilih Makanan" and rating != "Rating":
            favorite_entry = f"{self.restaurant_data['name']} - {meal} ({rating})"
            
            existing_items = [self.favorite_meals_list.item(i).text() for i in range(self.favorite_meals_list.count())]
            if favorite_entry not in existing_items:
                item = QListWidgetItem(favorite_entry)
                self.favorite_meals_list.addItem(item)

            self.meal_dropdown.setCurrentIndex(0)
            self.rating_dropdown.setCurrentIndex(0)

    def add_comment(self):
        comment_text = self.comment_input.text().strip()
        if comment_text:
            self.comments.append(comment_text)
            self.update_comments_display()
            self.comment_input.clear()

    def update_comments_display(self):
        self.comments_display.setText("\n".join(f"- {comment}" for comment in self.comments))


class FoodDeliveryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kaciw FooD")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #F5F5F5; }
            QPushButton { 
                background-color:#9932CC; 
                color: white; 
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { 
                background-color: #BA55D3; 
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        restaurants_container = QWidget()
        restaurants_layout = QVBoxLayout(restaurants_container)

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

        restaurants_layout.addLayout(search_layout)

        restaurants_scroll = QScrollArea()
        restaurants_widget = QWidget()
        restaurants_grid = QGridLayout(restaurants_widget)
        restaurants_scroll.setWidget(restaurants_widget)
        restaurants_scroll.setWidgetResizable(True)

        favorite_meals_container = QWidget()
        favorite_meals_layout = QVBoxLayout(favorite_meals_container)
        favorite_meals_title = QLabel("Makanan Favorit")
        favorite_meals_title.setStyleSheet("font-weight: bold; font-size: 16px;")
        favorite_meals_layout.addWidget(favorite_meals_title)

        self.favorite_meals_list = QListWidget()
        self.favorite_meals_list.setStyleSheet("""
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 5px;
        """)
        favorite_meals_layout.addWidget(self.favorite_meals_list)

        restaurants = [
            {"name": "Nasi Padang Ondemande", "cuisine": "kilo 50", "distance": 1.2, "rating": 4.5},
            {"name": "Gado Gado Pak Gundul", "cuisine": "kampung baru", "distance": 2.5, "rating": 4.8},
            {"name": "Austin Kebab", "cuisine": "Bangun Reksa", "distance": 0.8, "rating": 4.2},
            {"name": "Mie Ayam Plat KT", "cuisine": "Rapak", "distance": 3.0, "rating": 4.6},
        ]

        row, col = 0, 0
        for restaurant in restaurants:
            restaurant_item = RestaurantItem(restaurant, self.favorite_meals_list)
            restaurants_grid.addWidget(restaurant_item, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        restaurants_layout.addWidget(restaurants_scroll)

        main_layout.addWidget(restaurants_container, 3)
        main_layout.addWidget(favorite_meals_container, 1)

    def show_filter_dialog(self):
        dialog = QDialog(self)  
        dialog.setWindowTitle("Filter Restoran")
        layout = QVBoxLayout()

    
        kategori_group = QButtonGroup()
        kategori_label = QLabel("Kategori Makanan:")
        kategori_options = ["Semua", "kilo 50", "Fast Food", "Vegetarian"]
        layout.addWidget(kategori_label)
        
        for option in kategori_options:
            radio = QRadioButton(option)
            kategori_group.addButton(radio)
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
