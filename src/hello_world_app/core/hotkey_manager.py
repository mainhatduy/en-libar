"""
Global hotkey manager cho Hello World App
Hỗ trợ cả X11 và Wayland sessions
"""

import os
import subprocess
from pynput import keyboard
from threading import Thread
import gi
from gi.repository import GLib

from ..utils.helpers import log_message

class HotkeyManager:
    """Quản lý global hotkeys cho ứng dụng"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.listener = None
        self.hotkey_thread = None
        self.running = False
        self.session_type = os.environ.get('XDG_SESSION_TYPE', 'unknown')
        
    def start(self):
        """Bắt đầu lắng nghe global hotkeys"""
        if self.running:
            return
            
        self.running = True
        
        if self.session_type == 'wayland':
            log_message("Phát hiện Wayland session - sử dụng GNOME shortcuts")
            self._setup_gnome_shortcut()
        else:
            log_message("Phát hiện X11 session - sử dụng pynput")
            self._setup_pynput_hotkey()
        
    def _setup_pynput_hotkey(self):
        """Thiết lập hotkey bằng pynput (cho X11)"""
        # Tạo hotkey combination: Super+T (phím Windows + T)
        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse('<cmd>+t'),
            self._on_hotkey_pressed
        )
        
        # Tạo listener
        self.listener = keyboard.Listener(
            on_press=lambda key: self._for_canonical(hotkey, key, True),
            on_release=lambda key: self._for_canonical(hotkey, key, False)
        )
        
        # Chạy listener trong thread riêng
        self.hotkey_thread = Thread(target=self._run_listener, daemon=True)
        self.hotkey_thread.start()
        
        log_message("Hotkey manager đã được khởi động (Super+T để hiển thị)")
    
    def _setup_gnome_shortcut(self):
        """Thiết lập GNOME custom shortcut (cho Wayland)"""
        try:
            # Tạo script để hiển thị ứng dụng
            script_path = self._create_show_window_script()
            
            # Thiết lập GNOME custom shortcut
            self._set_gnome_custom_shortcut(script_path)
            
            log_message("GNOME shortcut đã được thiết lập (Super+T để hiển thị)")
            log_message("Lưu ý: Bạn có thể cần restart session để shortcut hoạt động")
            
        except Exception as e:
            log_message(f"Không thể thiết lập GNOME shortcut: {e}", "ERROR")
            log_message("Vui lòng thiết lập manual: Settings → Keyboard → Custom Shortcuts", "INFO")
    
    def _create_show_window_script(self):
        """Tạo script để hiển thị cửa sổ"""
        script_content = f'''#!/bin/bash
# Script để hiển thị Hello World App
python3 -c "
import dbus
import sys
import os
import time
import subprocess

def find_window_id():
    try:
        output = subprocess.check_output(['xdotool', 'search', '--name', 'Hello World App']).decode().strip()
        if output:
            return output.split('\\n')[0]
    except:
        pass
    return None

try:
    # Thử kết nối qua D-Bus
    bus = dbus.SessionBus()
    proxy = bus.get_object('org.hello_world_app.Service', '/org/hello_world_app')
    interface = dbus.Interface(proxy, 'org.hello_world_app.Interface')
    interface.ShowWindow()
    print('Successfully showed window via D-Bus')
except Exception as e:
    print(f'D-Bus connection failed: {{e}}')
    
    # Thử tìm cửa sổ bằng xdotool (nếu có X11)
    window_id = find_window_id()
    if window_id:
        try:
            # Kích hoạt cửa sổ hiện có
            subprocess.run(['xdotool', 'windowactivate', window_id])
            print(f'Activated existing window with ID: {{window_id}}')
            sys.exit(0)
        except Exception as e:
            print(f'Failed to activate window: {{e}}')
    
    # Kiểm tra process đang chạy
    try:
        ps_output = subprocess.check_output(['pgrep', '-f', 'python.*hello_world_app']).decode().strip()
        if ps_output:
            print('App is already running, but window not found. Sending signal to show window...')
            # Gửi SIGUSR1 đến process để báo hiệu hiển thị cửa sổ
            for pid in ps_output.split('\\n'):
                try:
                    os.kill(int(pid), 10)  # SIGUSR1 = 10
                    print(f'Sent signal to PID {{pid}}')
                    time.sleep(0.5)  # Đợi chút để ứng dụng hiển thị
                except:
                    pass
            sys.exit(0)
    except subprocess.CalledProcessError:
        # Process không tìm thấy, chạy mới
        pass
        
    # Fallback: Chạy ứng dụng mới nếu chưa có
    print('Starting new instance of the app')
    subprocess.Popen(['python3', '-m', 'src.hello_world_app.main'], 
                    cwd='{os.getcwd()}')
"
'''
        
        script_path = os.path.expanduser('~/.local/bin/show_hello_world_app.sh')
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        os.chmod(script_path, 0o755)
        return script_path
    
    def _set_gnome_custom_shortcut(self, script_path):
        """Thiết lập GNOME custom shortcut"""
        try:
            # Tạo path cho shortcut
            shortcut_name = 'hello-world-app'
            
            # Lấy danh sách shortcuts hiện tại
            result = subprocess.run([
                'gsettings', 'get', 'org.gnome.settings-daemon.plugins.media-keys', 'custom-keybindings'
            ], capture_output=True, text=True)
            
            current_shortcuts = result.stdout.strip()
            
            # Đường dẫn đến custom keybinding
            binding_path = f'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/{shortcut_name}/'
            
            # Cập nhật danh sách shortcuts
            if current_shortcuts == '@as []':
                new_shortcuts = f"['{binding_path}']"
            else:
                # Parse current shortcuts và thêm mới nếu chưa có
                shortcuts_list = current_shortcuts.strip('[]').replace("'", '').split(', ')
                if binding_path not in shortcuts_list:
                    shortcuts_list.append(binding_path)
                new_shortcuts = f"[{', '.join(f"'{path}'" for path in shortcuts_list)}]"
            
            # Cập nhật danh sách shortcuts
            subprocess.run([
                'gsettings', 'set', 'org.gnome.settings-daemon.plugins.media-keys', 
                'custom-keybindings', new_shortcuts
            ], check=True)
            
            # Thiết lập từng thuộc tính của shortcut
            schema_base = 'org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:'
            schema_path = f'{schema_base}{binding_path}'
            
            subprocess.run(['gsettings', 'set', schema_path, 'name', 'Show Hello World App'], check=True)
            subprocess.run(['gsettings', 'set', schema_path, 'command', script_path], check=True)
            subprocess.run(['gsettings', 'set', schema_path, 'binding', '<Super>t'], check=True)
            
            log_message("GNOME shortcut đã được thiết lập (Super+T để hiển thị)")
            
        except Exception as e:
            log_message(f"Không thể thiết lập GNOME shortcut: {e}", "ERROR")
            log_message("Vui lòng thiết lập manual: Settings → Keyboard → Custom Shortcuts", "INFO")
    
    def stop(self):
        """Dừng lắng nghe global hotkeys"""
        self.running = False
        
        if self.listener:
            self.listener.stop()
            
        log_message("Hotkey manager đã được dừng")
    
    def _run_listener(self):
        """Chạy listener trong thread riêng"""
        try:
            self.listener.start()
            self.listener.join()
        except Exception as e:
            log_message(f"Lỗi khi chạy hotkey listener: {e}", "ERROR")
    
    def _for_canonical(self, hotkey, key, is_pressed):
        """Xử lý key events cho hotkey"""
        try:
            if is_pressed:
                hotkey.press(self.listener.canonical(key))
            else:
                hotkey.release(self.listener.canonical(key))
        except AttributeError:
            # Ignore special keys that don't have canonical representation
            pass
    
    def _on_hotkey_pressed(self):
        """Xử lý khi hotkey Super+T được nhấn"""
        log_message("Phát hiện hotkey Super+T")
        
        # Sử dụng GLib.idle_add để chạy trong main thread của GTK
        GLib.idle_add(self._show_window_main_thread)
    
    def _show_window_main_thread(self):
        """Hiển thị window trong main thread của GTK"""
        try:
            if self.app and hasattr(self.app, 'show_window'):
                self.app.show_window()
                log_message("Hiển thị cửa sổ từ hotkey")
        except Exception as e:
            log_message(f"Lỗi khi hiển thị cửa sổ từ hotkey: {e}", "ERROR")
        
        return False  # Chỉ chạy một lần 