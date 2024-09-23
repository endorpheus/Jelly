from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QSize, QMargins, QDir, QPoint
from PySide6.QtGui import QColor, QPainter, QBrush, QIcon, QMouseEvent

class Jelly(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set dialog properties
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Variables for dragging
        self.dragging = False
        self.drag_position = QPoint()

        # Button placement variables
        self.button_margin = 5
        self.button_spacing = 5
        self.button_size = QSize(14, 14)

        # Set size and appearance
        self.resize(400, 300)
        
        self.setStyleSheet("""
            QDialog {
                background-color: rgba(34, 9, 56, 217);
                border-radius: 15px;
            }
            QLabel, QPushButton {
                color: white;
            }
            QLineEdit {
                color: white;
                background-color: rgba(24, 6, 40, 217);
                border: 1px solid rgba(255, 255, 255, 100);
                border-radius: 5px;
                padding: 2px 5px;
            }
            QPushButton {
                background-color: rgba(24, 6, 40, 217);
                border: 1px solid rgba(255, 255, 255, 100);
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: rgba(44, 16, 70, 217);
            }
        """)

        # Set the window icon
        icon_path = QDir.current().filePath("./icons/jelly_icon.png")
        self.setWindowIcon(QIcon(icon_path))

        # Layout for the dialog
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(QMargins(20, 10, 20, 20))  # Reduced top margin
        self.main_layout.setSpacing(10)

        # Horizontal layout for the buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(self.button_margin, 0, self.button_margin, 0)  # Removed top margin
        self.button_layout.setSpacing(self.button_spacing)

        # Minimize button
        self.minimize_button = QPushButton()
        self.minimize_button.setFixedSize(self.button_size)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #FFB700;
                border: none;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #FFC800;
                border: 2px solid #FFD700;
            }
        """)
        self.minimize_button.clicked.connect(self.showMinimized)

        # Close button
        self.close_button = QPushButton()
        self.close_button.setFixedSize(self.button_size)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #FF5F57;
                border: none;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #FF6F69;
                border: 2px solid #FF8C8A;
            }
        """)
        self.close_button.clicked.connect(self.close)
        
        # Add the buttons to the button layout
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.minimize_button)
        self.button_layout.addWidget(self.close_button)

        # Add the button layout to the main layout
        self.main_layout.addLayout(self.button_layout)

        # Content Layout
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)
        self.content_layout.setContentsMargins(0, 5, 0, 0)  # Reduced top margin

        # Add the content layout to the main layout
        self.main_layout.addLayout(self.content_layout)

        # Ensure the dialog resizes based on content
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(34, 9, 56, 217)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 15, 15)

    def add_content_widget(self, widget):
        self.content_layout.addWidget(widget)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

    def setLayout(self, layout):
        self.content_layout = layout
        self.main_layout.addLayout(self.content_layout)