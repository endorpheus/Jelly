import sys
import json
import os
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton, 
                               QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QColorDialog)
from PySide6.QtGui import QPixmap, QColor, QPainter, QFont, QImage
from PySide6.QtCore import Qt, QSize
import qrcode
from PIL.ImageQt import ImageQt
from PIL import Image
from Jelly import Jelly

class ColorSwatchButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(30, 30))
        self.setColor(color)

    def setColor(self, color):
        self.color = QColor(color) if isinstance(color, str) else color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawRect(self.rect())

    def sizeHint(self):
        return QSize(30, 30)

class QRJelly(QWidget):
    def __init__(self):
        super().__init__()

        self.jelly_dialog = Jelly()
        self.jelly_dialog.setWindowTitle("QRJelly")
        self.jelly_dialog.resize(400, 500)

        # Load color settings
        self.colors_file = "qr_jelly_colors.json"
        self.load_color_settings()

        # Main layout for the Jelly dialog
        main_layout = QVBoxLayout()

        # Add window title widget
        title_label = QLabel("QRJelly")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin: 10px 0;
            }
        """)
        main_layout.addWidget(title_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter text for QR code")
        main_layout.addWidget(self.input_field)

        self.generate_button = QPushButton("Generate QR Code")
        self.generate_button.clicked.connect(self.on_generate_qr_code)
        main_layout.addWidget(self.generate_button)

        self.save_button = QPushButton("Save QR Code")
        self.save_button.clicked.connect(self.on_save_qr_code)
        self.save_button.setEnabled(False)
        main_layout.addWidget(self.save_button)

        main_layout.addWidget(QWidget())  # Spacer

        # Color selection layout
        color_layout = QHBoxLayout()
        color_layout.addStretch()
        color_layout.addWidget(QLabel("QR Code Colors:"))
        self.fg_color_button = ColorSwatchButton(self.fg_color)
        self.fg_color_button.clicked.connect(self.on_fg_color_click)
        self.bg_color_button = ColorSwatchButton(self.bg_color)
        self.bg_color_button.clicked.connect(self.on_bg_color_click)
        color_layout.addWidget(self.fg_color_button)
        color_layout.addWidget(self.bg_color_button)
        
        # Add swap colors button
        self.swap_colors_button = QPushButton("↔")
        self.swap_colors_button.setFixedSize(30, 30)
        self.swap_colors_button.clicked.connect(self.swap_colors)
        color_layout.addWidget(self.swap_colors_button)
        
        color_layout.addStretch()
        main_layout.addLayout(color_layout)

        # QR code display
        qr_layout = QHBoxLayout()
        qr_layout.addStretch()
        self.qr_code_label = QLabel()
        self.qr_code_label.setAlignment(Qt.AlignCenter)
        self.qr_code_label.setFixedSize(300, 300)
        qr_layout.addWidget(self.qr_code_label)
        qr_layout.addStretch()
        main_layout.addLayout(qr_layout)

        main_layout.addStretch()  # This will push everything up

        # Set the main layout to the Jelly dialog
        self.jelly_dialog.setLayout(main_layout)

        self.qr_image = None
        self.jelly_dialog.show()

    def load_color_settings(self):
        if os.path.exists(self.colors_file):
            with open(self.colors_file, 'r') as f:
                colors = json.load(f)
            self.fg_color = QColor(colors.get('foreground_color', '#000000'))
            self.bg_color = QColor(colors.get('background_color', '#FFFFFF'))
        else:
            self.fg_color = QColor('#000000')
            self.bg_color = QColor('#FFFFFF')

    def save_color_settings(self):
        colors = {
            'foreground_color': self.fg_color.name(),
            'background_color': self.bg_color.name()
        }
        with open(self.colors_file, 'w') as f:
            json.dump(colors, f)

    def on_fg_color_click(self):
        color = QColorDialog.getColor(self.fg_color_button.color, self, "Select Foreground Color")
        if color.isValid():
            self.fg_color_button.setColor(color)
            self.fg_color = color
            self.save_color_settings()
            self.on_generate_qr_code()

    def on_bg_color_click(self):
        color = QColorDialog.getColor(self.bg_color_button.color, self, "Select Background Color")
        if color.isValid():
            self.bg_color_button.setColor(color)
            self.bg_color = color
            self.save_color_settings()
            self.on_generate_qr_code()

    def swap_colors(self):
        self.fg_color, self.bg_color = self.bg_color, self.fg_color
        self.fg_color_button.setColor(self.fg_color)
        self.bg_color_button.setColor(self.bg_color)
        self.save_color_settings()
        self.on_generate_qr_code()

    def on_generate_qr_code(self):
        text = self.input_field.text()
        self.qr_image = self.generate_qr_code(text)
        if self.qr_image:
            self.display_qr_code()
            self.save_button.setEnabled(True)

    def on_save_qr_code(self):
        if self.qr_image:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "PNG Files (*.png);;All Files (*)")
            if file_path:
                self.qr_image.save(file_path)

    def generate_qr_code(self, text):
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(text)
            qr.make(fit=True)
            fg_color = self.fg_color.name()
            bg_color = self.bg_color.name()
            img = qr.make_image(fill_color=fg_color, back_color=bg_color)
            return img
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None

    def display_qr_code(self):
        if self.qr_image:
            qt_img = ImageQt(self.qr_image)
            pixmap = QPixmap.fromImage(qt_img)
            scaled_pixmap = pixmap.scaled(self.qr_code_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.qr_code_label.setPixmap(scaled_pixmap)

def main():
    app = QApplication(sys.argv)
    qr_jelly = QRJelly()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()