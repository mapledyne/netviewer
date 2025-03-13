"""
Main application module for NetViewer
"""
import sys
print("Starting application...")  # Debug print
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
import diagnostics

class MainWindow(QMainWindow):
    """Main window of the NetViewer application"""
    
    def __init__(self):
        print("Creating main window...")  # Debug print
        super().__init__()
        self.setup_ui()
        self.setup_diagnostics()
        
    def setup_ui(self):
        """Initialize the user interface"""
        print("Setting up UI...")  # Debug print
        self.setWindowTitle("NetViewer")
        self.setMinimumSize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add placeholder widgets here
        
    def setup_diagnostics(self):
        """Setup diagnostics logging"""
        print("Setting up diagnostics...")  # Debug print
        diagnostics.info("NetViewer main window initialized")
        
def main():
    """Main entry point for the application"""
    print("Starting main function...")  # Debug print
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MainWindow()
    print("Showing window...")  # Debug print
    window.show()
    
    print("Starting event loop...")  # Debug print
    # Start the event loop
    sys.exit(app.exec()) 