"""
SSL Certificate lookup tool
"""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QFrame,
    QGridLayout,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap, QImage
from datetime import datetime, timedelta
import os
import sys
import tempfile
import subprocess
import requests
from urllib.parse import urlparse
from icalendar import Calendar, Event

from diagnostics.network import SSLCertMonitor


class SSLCertWidget(QWidget):
    """Widget for SSL certificate lookup"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cert_monitor = SSLCertMonitor()
        self.setup_ui()
        
    def get_favicon(self, domain):
        """Get favicon for the domain using Google's favicon service"""
        try:
            # Use Google's favicon service
            url = f'https://www.google.com/s2/favicons?domain={domain}&sz=64'
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                # Convert response content to QPixmap
                image = QImage()
                image.loadFromData(response.content)
                if not image.isNull():
                    pixmap = QPixmap.fromImage(image)
                    
                    # Scale to 32x32 while maintaining aspect ratio
                    return pixmap.scaled(
                        QSize(32, 32),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
            return None
        except Exception:
            return None
        
    def update_favicon(self, domain):
        """Update the favicon display"""
        if not domain:
            self.favicon_label.setPixmap(QPixmap())
            self.favicon_label.setVisible(False)
            return
            
        favicon = self.get_favicon(domain)
        if favicon:
            self.favicon_label.setPixmap(favicon)
            self.favicon_label.setVisible(True)
        else:
            self.favicon_label.setPixmap(QPixmap())
            self.favicon_label.setVisible(False)
            
    def format_date(self, date_str):
        """Format ISO date string into a friendly format"""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%B %d, %Y %H:%M UTC")
        except (ValueError, AttributeError):
            return date_str
            
    def create_calendar_event(self, domain, expiry_date):
        """Create a calendar event for certificate renewal reminder"""
        try:
            # Calculate reminder date (14 days before expiry)
            reminder_date = expiry_date - timedelta(days=14)
            
            # Create calendar
            cal = Calendar()
            cal.add('prodid', '-//NetViewer SSL Certificate Renewal//mxm.dk//')
            cal.add('version', '2.0')
            
            # Create event
            event = Event()
            event.add('summary', f'SSL Certificate Renewal - {domain}')
            event.add('description', 
                     f'SSL certificate for {domain} expires on '
                     f'{expiry_date.strftime("%B %d, %Y")}. '
                     f'Please renew the certificate before expiration.')
            event.add('dtstart', reminder_date)
            event.add('dtend', reminder_date)
            event.add('dtstamp', datetime.utcnow())
            event.add('class', 'public')  # Make the event public
            event.add('transp', 'TRANSPARENT')  # Show as free time
            
            # Add event to calendar
            cal.add_component(event)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.ics') as f:
                f.write(cal.to_ical())
                temp_file = f.name
                
            # Open the calendar file with the default application
            if os.name == 'nt':  # Windows
                os.startfile(temp_file)
            elif os.name == 'posix':  # macOS and Linux
                if sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', temp_file])
                else:  # Linux
                    subprocess.run(['xdg-open', temp_file])
                    
            return temp_file
                
        except Exception as e:
            print(f"Error creating calendar event: {e}")
            return None
            
    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Search section
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(12, 8, 12, 8)  # Increased left/right margins
        search_layout.setSpacing(12)  # Increased spacing between elements
        
        # Favicon label
        self.favicon_label = QLabel()
        self.favicon_label.setFixedSize(32, 32)
        self.favicon_label.setMinimumSize(32, 32)
        self.favicon_label.setAlignment(Qt.AlignCenter)
        self.favicon_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
                margin: 0;
                padding: 0;
            }
        """)
        self.favicon_label.setVisible(False)  # Initially hidden
        
        # Domain input
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("Enter domain (e.g., example.com)")
        self.domain_input.returnPressed.connect(self.lookup_certificate)
        self.domain_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 10px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: white;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
            QLineEdit::placeholder {
                color: #999999;
            }
        """)
        
        # Search button
        self.search_button = QPushButton("Lookup")
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #006cbd;
            }
            QPushButton:pressed {
                background-color: #005ba1;
            }
        """)
        self.search_button.clicked.connect(self.lookup_certificate)
        
        search_layout.addWidget(self.favicon_label)
        search_layout.addWidget(self.domain_input)
        search_layout.addWidget(self.search_button)
        
        # Results section
        self.results_frame = QFrame()
        self.results_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        self.results_layout = QVBoxLayout(self.results_frame)
        self.results_layout.setContentsMargins(16, 16, 16, 16)
        self.results_layout.setSpacing(16)
        
        # Add widgets to main layout
        layout.addWidget(search_frame)
        layout.addWidget(self.results_frame, 1)  # Add stretch factor of 1 to make it expand
        
        # Initially hide results
        self.results_frame.hide()
        
    def clear_results(self):
        """Clear all results from the results frame"""
        # Remove all widgets from the layout
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # If it's a layout, remove all its widgets
                while item.layout().count():
                    subitem = item.layout().takeAt(0)
                    if subitem.widget():
                        subitem.widget().deleteLater()
                item.layout().deleteLater()
        
    def lookup_certificate(self):
        """Lookup SSL certificate for the given domain"""
        domain = self.domain_input.text().strip()
        if not domain:
            return
            
        try:
            # Clear previous results first
            self.clear_results()
            
            # Update favicon when searching
            self.update_favicon(domain)
            
            # Get SSL info from certificate monitor
            cert_info = self.cert_monitor.check_certificate(domain)
            if not cert_info:
                raise Exception("Failed to retrieve certificate information")
            
            # Create grid for certificate info
            grid = QGridLayout()
            grid.setSpacing(12)
            
            # Add certificate information
            info = [
                ("Subject", cert_info.get('subject', 'Unknown')),
                ("Issuer", cert_info.get('issuer', 'Unknown')),
                ("Valid From", self.format_date(cert_info.get('not_before', 'Unknown'))),
                ("Valid Until", self.format_date(cert_info.get('not_after', 'Unknown'))),
                ("Days Until Expiry", str(cert_info.get('days_until_expiry', 'Unknown'))),
                ("Version", cert_info.get('version', 'Unknown')),
                ("Serial Number", str(cert_info.get('serial_number', 'Unknown'))),
            ]
            
            for i, (label, value) in enumerate(info):
                # Label
                label_widget = QLabel(label)
                label_widget.setStyleSheet("""
                    QLabel {
                        color: #666666;
                        font-size: 14px;
                    }
                """)
                
                # Value
                value_widget = QLabel(value)
                value_widget.setWordWrap(True)
                value_widget.setStyleSheet("""
                    QLabel {
                        color: #333333;
                        font-size: 14px;
                        font-weight: bold;
                    }
                """)
                
                grid.addWidget(label_widget, i, 0)
                grid.addWidget(value_widget, i, 1)
            
            self.results_layout.addLayout(grid)
            
            # Add calendar button
            try:
                expiry_date = datetime.fromisoformat(
                    cert_info.get('not_after', '').replace('Z', '+00:00')
                )
                calendar_button = QPushButton("Add Renewal Reminder")
                calendar_button.setStyleSheet("""
                    QPushButton {
                        background-color: #28a745;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 6px 12px;
                        font-size: 14px;
                        font-weight: bold;
                        margin-top: 8px;
                    }
                    QPushButton:hover {
                        background-color: #218838;
                    }
                    QPushButton:pressed {
                        background-color: #1e7e34;
                    }
                """)
                calendar_button.clicked.connect(
                    lambda: self.create_calendar_event(domain, expiry_date)
                )
                self.results_layout.addWidget(calendar_button)
            except (ValueError, TypeError):
                pass  # Skip calendar button if date parsing fails
            
            self.results_frame.show()
            
        except Exception as e:
            # Show error message
            error_label = QLabel(f"Error: {str(e)}")
            error_label.setStyleSheet("""
                QLabel {
                    color: #d13438;
                    font-size: 14px;
                }
            """)
            self.results_layout.addWidget(error_label)
            self.results_frame.show() 