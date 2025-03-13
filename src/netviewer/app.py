"""
Main application window for NetViewer
"""
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QSize

from .icons import create_dns_icon, create_ssl_icon, create_ip_icon
from .tools.ssl_cert import SSLCertWidget


class ToolButton(QPushButton):
    """Custom button for tool selection with consistent styling"""
    def __init__(self, text, icon=None, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 10))
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(24, 24))
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                background-color: transparent;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #0078d4;
                color: white;
            }
        """)


class MainWindow(QMainWindow):
    """Main window of the NetViewer application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetViewer")
        self.setMinimumSize(1024, 768)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-right: 1px solid #e0e0e0;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(8)
        
        # Add logo/title
        title = QLabel("NetViewer")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #333333; margin-bottom: 16px;")
        sidebar_layout.addWidget(title)
        
        # Create tool buttons with icons
        self.dns_button = ToolButton("DNS Information", create_dns_icon())
        self.ssl_button = ToolButton("SSL Certificate", create_ssl_icon())
        self.ip_button = ToolButton("IP Address Info", create_ip_icon())
        
        # Add buttons to sidebar
        sidebar_layout.addWidget(self.dns_button)
        sidebar_layout.addWidget(self.ssl_button)
        sidebar_layout.addWidget(self.ip_button)
        sidebar_layout.addStretch()
        
        # Create stacked widget for different tools
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: white;
            }
        """)
        
        # Add placeholder pages for each tool
        self.dns_page = QWidget()
        self.ssl_page = SSLCertWidget()
        self.ip_page = QWidget()
        
        # Add pages to stack
        self.content_stack.addWidget(self.dns_page)
        self.content_stack.addWidget(self.ssl_page)
        self.content_stack.addWidget(self.ip_page)
        
        # Add widgets to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack)
        
        # Connect signals
        self.dns_button.clicked.connect(lambda: self.switch_tool(0))
        self.ssl_button.clicked.connect(lambda: self.switch_tool(1))
        self.ip_button.clicked.connect(lambda: self.switch_tool(2))
        
        # Set initial tool
        self.current_tool = 0
        self.switch_tool(0)
        
    def switch_tool(self, index):
        """Switch to the selected tool"""
        self.current_tool = index
        self.content_stack.setCurrentIndex(index)
        
        # Update button styles to show current selection
        buttons = [self.dns_button, self.ssl_button, self.ip_button]
        for i, button in enumerate(buttons):
            if i == index:
                button.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 8px 16px;
                        border: none;
                        border-radius: 4px;
                        background-color: #0078d4;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #0078d4;
                        color: white;
                    }
                    QPushButton:pressed {
                        background-color: #006cbd;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 8px 16px;
                        border: none;
                        border-radius: 4px;
                        background-color: transparent;
                        color: #333333;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                    QPushButton:pressed {
                        background-color: #0078d4;
                        color: white;
                    }
                """)


def main():
    """Main entry point for the application"""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec()) 