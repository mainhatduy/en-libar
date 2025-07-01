#!/usr/bin/env python3
"""
Entry point cho Hello World Desktop App
"""

import os
import sys
import dbus
import subprocess
import time

from .core.app import HelloWorldApp
from .utils.helpers import log_message

def is_app_running():
    """Kiểm tra xem ứng dụng đã chạy chưa"""
    # Kiểm tra qua D-Bus
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object('org.hello_world_app.Service', '/org/hello_world_app')
        return True
    except:
        # Không tìm thấy dịch vụ D-Bus
        return False

def show_existing_window():
    """Hiển thị cửa sổ của ứng dụng đang chạy"""
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object('org.hello_world_app.Service', '/org/hello_world_app')
        interface = dbus.Interface(proxy, 'org.hello_world_app.Interface')
        interface.ShowWindow()
        log_message("Đã gửi lệnh hiển thị cửa sổ cho instance đang chạy")
        return True
    except Exception as e:
        log_message(f"Không thể kết nối với instance đang chạy: {e}", "ERROR")
        return False

def main():
    """Hàm main entry point"""
    # Kiểm tra nếu ứng dụng đã chạy
    if is_app_running():
        log_message("Phát hiện instance đang chạy - hiển thị cửa sổ")
        if show_existing_window():
            sys.exit(0)
        else:
            log_message("Không thể kết nối với instance đang chạy - tạo instance mới", "WARNING")
    
    # Tạo và chạy ứng dụng mới
    log_message("Khởi động instance mới")
    app = HelloWorldApp()
    app.run()

if __name__ == "__main__":
    main() 