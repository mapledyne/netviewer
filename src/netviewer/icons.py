"""
Icon management for NetViewer
"""
from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
import os

# Icon sizes
ICON_SIZE = QSize(24, 24)
SMALL_ICON_SIZE = QSize(16, 16)

def get_icon_path(name):
    """Get the path to an icon file"""
    module_dir = Path(__file__).parent
    return str(module_dir / 'icons' / f'{name}.svg')

# Create icons for our tools
def create_dns_icon():
    """Create DNS icon"""
    icon = QIcon()
    icon.addFile(
        os.path.join(os.path.dirname(__file__), "icons", "format-list-bulleted.svg")
    )
    return icon

def create_ssl_icon():
    """Create SSL icon"""
    icon = QIcon()
    icon.addFile(
        os.path.join(os.path.dirname(__file__), "icons", "certificate-outline.svg")
    )
    return icon

def create_ip_icon():
    """Create IP icon"""
    icon = QIcon()
    icon.addFile(
        os.path.join(os.path.dirname(__file__), "icons", "server-network-outline.svg")
    )
    return icon 