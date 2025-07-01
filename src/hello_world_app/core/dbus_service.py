"""
D-Bus service cho Hello World App
Cho phép điều khiển ứng dụng qua D-Bus
"""

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

from ..utils.helpers import log_message

# Thiết lập main loop mặc định cho D-Bus
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

class HelloWorldDBusService(dbus.service.Object):
    """Triển khai D-Bus service cho Hello World App"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.bus_name = None
        self.initialized = False
        
    def register(self):
        """Đăng ký D-Bus service"""
        try:
            # Kết nối với session bus
            session_bus = dbus.SessionBus()
            
            # Đăng ký tên dịch vụ
            bus_name = dbus.service.BusName(
                "org.hello_world_app.Service", 
                bus=session_bus
            )
            
            # Khởi tạo đối tượng dịch vụ
            dbus.service.Object.__init__(
                self, 
                bus_name, 
                "/org/hello_world_app"
            )
            
            self.bus_name = bus_name
            self.initialized = True
            
            log_message("Đăng ký D-Bus service thành công: org.hello_world_app.Service")
            return True
            
        except Exception as e:
            log_message(f"Không thể đăng ký D-Bus service: {e}", "ERROR")
            return False
    
    @dbus.service.method(
        dbus_interface="org.hello_world_app.Interface",
        in_signature="", 
        out_signature=""
    )
    def ShowWindow(self):
        """Hiển thị cửa sổ chính"""
        log_message("Yêu cầu hiển thị cửa sổ qua D-Bus")
        if self.app:
            # Sử dụng GLib.idle_add để chạy trong main thread của GTK
            GLib.idle_add(self.app.show_window)
            return True
        return False
    
    @dbus.service.method(
        dbus_interface="org.hello_world_app.Interface",
        in_signature="", 
        out_signature=""
    )
    def HideWindow(self):
        """Ẩn cửa sổ chính"""
        log_message("Yêu cầu ẩn cửa sổ qua D-Bus")
        if self.app:
            GLib.idle_add(self.app.hide_window)
            return True
        return False
    
    @dbus.service.method(
        dbus_interface="org.hello_world_app.Interface",
        in_signature="", 
        out_signature=""
    )
    def Quit(self):
        """Thoát ứng dụng"""
        log_message("Yêu cầu thoát ứng dụng qua D-Bus")
        if self.app:
            GLib.idle_add(self.app.quit)
            return True
        return False 