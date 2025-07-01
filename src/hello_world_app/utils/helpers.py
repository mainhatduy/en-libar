"""
Utility functions và helpers cho Hello World App
"""

from datetime import datetime
import signal
import sys

def get_current_time_string() -> str:
    """Lấy thời gian hiện tại dưới dạng string định dạng"""
    return datetime.now().strftime("%H:%M:%S - %d/%m/%Y")

def setup_signal_handlers():
    """Thiết lập xử lý tín hiệu Ctrl+C"""
    signal.signal(signal.SIGINT, signal.SIG_DFL)

def format_system_info() -> str:
    """Tạo thông tin hệ thống để hiển thị"""
    time_str = get_current_time_string()
    return f'<span size="medium">Ứng dụng chạy trên Fedora\nThời gian: {time_str}</span>'

def log_message(message: str, level: str = "INFO"):
    """In log message với format đẹp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def is_fedora_system() -> bool:
    """Kiểm tra xem có phải hệ thống Fedora không"""
    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read()
            return 'Fedora' in content
    except:
        return False 