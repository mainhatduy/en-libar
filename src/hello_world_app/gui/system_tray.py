"""
System tray management cho Hello World App
"""

import gi
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3

from ..core.config import AppConfig
from ..utils.helpers import log_message

class SystemTray:
    """Quản lý system tray indicator"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.indicator = None
        self.setup_indicator()
    
    def setup_indicator(self):
        """Thiết lập system tray indicator"""
        try:
            self.indicator = AppIndicator3.Indicator.new(
                AppConfig.INDICATOR_ID,
                AppConfig.INDICATOR_ICON,
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
            )
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self.indicator.set_title(AppConfig.APP_NAME)
            
            # Tạo menu cho system tray
            menu = self._create_tray_menu()
            self.indicator.set_menu(menu)
            
            log_message("System tray indicator đã được khởi tạo")
            
        except Exception as e:
            log_message(f"Không thể tạo system tray indicator: {e}", "ERROR")
            log_message("Ứng dụng sẽ chạy ở chế độ cửa sổ thông thường", "INFO")
    
    def _create_tray_menu(self) -> Gtk.Menu:
        """Tạo menu cho system tray"""
        menu = Gtk.Menu()
        
        # Menu item hiển thị cửa sổ
        show_item = Gtk.MenuItem(label="Hiển thị cửa sổ")
        show_item.connect("activate", self._on_show_clicked)
        menu.append(show_item)
        
        # Menu item thông tin hotkey
        hotkey_info = Gtk.MenuItem(label="Super+T: Hiển thị nhanh")
        hotkey_info.set_sensitive(False)  # Chỉ để hiển thị thông tin
        menu.append(hotkey_info)
        
        # Separator
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        
        # Menu item thoát
        quit_item = Gtk.MenuItem(label="Thoát")
        quit_item.connect("activate", self._on_quit_clicked)
        menu.append(quit_item)
        
        menu.show_all()
        return menu
    
    def _on_show_clicked(self, widget):
        """Xử lý khi click menu hiển thị"""
        self.app.show_window()
    
    def _on_quit_clicked(self, widget):
        """Xử lý khi click menu thoát"""
        self.app.quit()
    
    def is_available(self) -> bool:
        """Kiểm tra xem system tray có sẵn hay không"""
        return self.indicator is not None
    
    def show(self):
        """Hiển thị system tray icon"""
        if self.indicator:
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    
    def hide(self):
        """Ẩn system tray icon"""
        if self.indicator:
            self.indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE) 