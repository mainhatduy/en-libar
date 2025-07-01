"""
Main application logic cho Hello World App
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import signal
import os

from .config import AppConfig
from .hotkey_manager import HotkeyManager
from .dbus_service import HelloWorldDBusService
from ..gui.main_window import MainWindow
from ..gui.system_tray import SystemTray
from ..utils.helpers import setup_signal_handlers, log_message

class HelloWorldApp:
    """Class chính quản lý ứng dụng Hello World"""
    
    def __init__(self):
        self.main_window = None
        self.system_tray = None
        self.hotkey_manager = None
        self.dbus_service = None
        self.setup_application()
    
    def setup_application(self):
        """Khởi tạo các thành phần của ứng dụng"""
        log_message(f"Khởi động {AppConfig.APP_NAME} v{AppConfig.APP_VERSION}")
        
        # Khởi tạo GUI components
        self.main_window = MainWindow(self)
        self.system_tray = SystemTray(self)
        
        # Khởi tạo hotkey manager
        self.hotkey_manager = HotkeyManager(self)
        
        # Khởi tạo và đăng ký D-Bus service
        self.setup_dbus_service()
        
        # Thiết lập signal handlers
        setup_signal_handlers()
        self._setup_custom_signal_handlers()
        
        # Tạo file PID để track process
        self._create_pid_file()
        
        log_message("Ứng dụng đã được khởi tạo thành công")
    
    def setup_dbus_service(self):
        """Thiết lập D-Bus service"""
        try:
            self.dbus_service = HelloWorldDBusService(self)
            if self.dbus_service.register():
                log_message("D-Bus service đã sẵn sàng nhận kết nối")
            else:
                log_message("Không thể khởi tạo D-Bus service, hotkey có thể tạo thêm instance", "WARNING")
        except Exception as e:
            log_message(f"Lỗi khi khởi tạo D-Bus service: {e}", "ERROR")
    
    def _setup_custom_signal_handlers(self):
        """Thiết lập signal handlers tùy chỉnh"""
        # SIGUSR1 để hiển thị cửa sổ từ external script
        signal.signal(signal.SIGUSR1, self._on_show_signal)
        log_message("Đã thiết lập signal handlers (SIGUSR1 để hiển thị cửa sổ)")
    
    def _on_show_signal(self, signum, frame):
        """Xử lý signal SIGUSR1 để hiển thị cửa sổ"""
        log_message("Nhận signal SIGUSR1 - hiển thị cửa sổ")
        # Sử dụng GLib.idle_add để chạy trong main thread của GTK
        GLib.idle_add(self.show_window)
    
    def _create_pid_file(self):
        """Tạo file PID để track process"""
        pid_dir = os.path.expanduser('~/.local/share/hello-world-app')
        os.makedirs(pid_dir, exist_ok=True)
        
        pid_file = os.path.join(pid_dir, 'app.pid')
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
        
        log_message(f"PID file: {pid_file}")
    
    def _remove_pid_file(self):
        """Xóa file PID khi thoát"""
        pid_file = os.path.expanduser('~/.local/share/hello-world-app/app.pid')
        try:
            os.remove(pid_file)
        except FileNotFoundError:
            pass
    
    def show_window(self):
        """Hiển thị cửa sổ chính"""
        if self.main_window:
            self.main_window.show()
            # Đảm bảo cửa sổ lên foreground
            if hasattr(self.main_window, 'window') and self.main_window.window:
                self.main_window.window.present()
    
    def hide_window(self):
        """Ẩn cửa sổ chính"""
        if self.main_window:
            self.main_window.hide()
    
    def quit(self):
        """Thoát ứng dụng hoàn toàn"""
        log_message("Đang thoát ứng dụng...")
        
        # Xóa PID file
        self._remove_pid_file()
        
        # Dừng hotkey manager
        if self.hotkey_manager:
            self.hotkey_manager.stop()
        
        # Cleanup
        if self.main_window:
            self.main_window.destroy()
        
        # Thoát GTK main loop
        Gtk.main_quit()
    
    def run(self):
        """Chạy ứng dụng"""
        log_message("Ứng dụng có thể chạy nền và hiển thị trong system tray")
        log_message("Sử dụng Super+T để hiển thị cửa sổ từ bất kỳ đâu")
        
        # Bắt đầu hotkey manager
        if self.hotkey_manager:
            self.hotkey_manager.start()
        
        # Hiển thị cửa sổ ban đầu
        self.show_window()
        
        try:
            # Chạy vòng lặp chính của GTK
            Gtk.main()
        except KeyboardInterrupt:
            log_message("Ứng dụng bị dừng bởi người dùng", "INFO")
        except Exception as e:
            log_message(f"Lỗi không mong muốn: {e}", "ERROR")
        finally:
            self._remove_pid_file()
            log_message("Ứng dụng đã thoát") 