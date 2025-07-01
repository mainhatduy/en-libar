"""
Main window GUI cho Hello World App
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ..core.config import AppConfig
from ..utils.helpers import format_system_info, log_message

class MainWindow:
    """Quản lý cửa sổ chính của ứng dụng"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.window = None
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        self.window = Gtk.Window()
        self.window.set_title(AppConfig.WINDOW_TITLE)
        self.window.set_default_size(
            AppConfig.WINDOW_DEFAULT_WIDTH, 
            AppConfig.WINDOW_DEFAULT_HEIGHT
        )
        self.window.set_position(Gtk.WindowPosition.CENTER)
        
        # Tạo layout chính
        vbox = self._create_main_layout()
        self.window.add(vbox)
        
        # Kết nối signal handlers
        self.window.connect("delete-event", self._on_window_delete)
    
    def _create_main_layout(self) -> Gtk.VBox:
        """Tạo layout chính của cửa sổ"""
        vbox = Gtk.VBox(spacing=20)
        vbox.set_margin_left(20)
        vbox.set_margin_right(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        
        # Thêm các widget
        vbox.pack_start(self._create_hello_label(), True, True, 0)
        vbox.pack_start(self._create_info_label(), True, True, 0)
        vbox.pack_start(self._create_hotkey_info_label(), False, False, 0)
        vbox.pack_start(self._create_hide_button(), False, False, 0)
        vbox.pack_start(self._create_quit_button(), False, False, 0)
        
        return vbox
    
    def _create_hello_label(self) -> Gtk.Label:
        """Tạo label chào mừng chính"""
        label = Gtk.Label()
        label.set_markup('<span size="xx-large" weight="bold">Hello World!</span>')
        label.set_halign(Gtk.Align.CENTER)
        return label
    
    def _create_info_label(self) -> Gtk.Label:
        """Tạo label thông tin hệ thống"""
        label = Gtk.Label()
        label.set_markup(format_system_info())
        label.set_halign(Gtk.Align.CENTER)
        return label
    
    def _create_hotkey_info_label(self) -> Gtk.Label:
        """Tạo label thông tin về hotkey"""
        label = Gtk.Label()
        label.set_markup('<span style="italic" color="blue">💡 Sử dụng Super+T để hiển thị cửa sổ từ bất kỳ đâu</span>')
        label.set_halign(Gtk.Align.CENTER)
        return label
    
    def _create_hide_button(self) -> Gtk.Button:
        """Tạo nút ẩn xuống system tray"""
        button = Gtk.Button(label="Ẩn xuống System Tray")
        button.connect("clicked", self._on_hide_clicked)
        return button
    
    def _create_quit_button(self) -> Gtk.Button:
        """Tạo nút thoát ứng dụng"""
        button = Gtk.Button(label="Thoát ứng dụng")
        button.connect("clicked", self._on_quit_clicked)
        return button
    
    def _on_hide_clicked(self, widget):
        """Xử lý khi click nút ẩn"""
        self.hide()
    
    def _on_quit_clicked(self, widget):
        """Xử lý khi click nút thoát"""
        self.app.quit()
    
    def _on_window_delete(self, widget, event):
        """Xử lý khi đóng cửa sổ"""
        self.hide()
        return True  # Ngăn destroy window
    
    def show(self):
        """Hiển thị cửa sổ"""
        if self.window:
            self.window.show_all()
            self.window.present()
            log_message("Hiển thị cửa sổ chính")
    
    def hide(self):
        """Ẩn cửa sổ"""
        if self.window:
            self.window.hide()
            log_message("Ẩn cửa sổ xuống system tray")
    
    def destroy(self):
        """Hủy cửa sổ"""
        if self.window:
            self.window.destroy()
            log_message("Đóng cửa sổ chính") 