"""
Configuration management for Hello World App
"""

import os
from pathlib import Path

class AppConfig:
    """Quản lý cấu hình ứng dụng"""
    
    # Application info
    APP_NAME = "Hello World App"
    APP_ID = "hello-world-app"
    APP_VERSION = "1.0.0"
    
    # Window settings
    WINDOW_TITLE = "Hello World - Fedora App"
    WINDOW_DEFAULT_WIDTH = 400
    WINDOW_DEFAULT_HEIGHT = 300
    
    # System tray settings
    INDICATOR_ID = "hello-world-app"
    INDICATOR_ICON = "applications-system"
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
    ASSETS_DIR = PROJECT_ROOT / "assets"
    ICONS_DIR = ASSETS_DIR / "icons"
    
    @classmethod
    def get_asset_path(cls, asset_name: str) -> str:
        """Lấy đường dẫn đến asset file"""
        return str(cls.ASSETS_DIR / asset_name)
    
    @classmethod
    def get_icon_path(cls, icon_name: str) -> str:
        """Lấy đường dẫn đến icon file"""
        return str(cls.ICONS_DIR / icon_name) 