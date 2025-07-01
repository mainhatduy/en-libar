#!/bin/bash

# Script để test và debug hotkey system
echo "🔍 Hello World App - Hotkey Debug Tool"
echo "===================================="

# Kiểm tra session type
echo "🖥️  Session Type: $XDG_SESSION_TYPE"
echo "🖱️  Desktop: $XDG_CURRENT_DESKTOP"
echo ""

# Kiểm tra dependencies
echo "📦 Kiểm tra Dependencies:"
echo "------------------------"

# Kiểm tra pynput
if python3 -c "import pynput" 2>/dev/null; then
    echo "✅ pynput: Đã cài đặt"
else
    echo "❌ pynput: Chưa cài đặt"
    echo "   Chạy: pip3 install --user pynput"
fi

# Kiểm tra GTK
if python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" 2>/dev/null; then
    echo "✅ GTK3: Đã cài đặt"
else
    echo "❌ GTK3: Chưa cài đặt"
    echo "   Chạy: sudo dnf install python3-gobject gtk3-devel"
fi

echo ""

# Kiểm tra hotkey setup dựa trên session type
if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    echo "🌊 Wayland Session - Kiểm tra GNOME Shortcuts:"
    echo "----------------------------------------------"
    
    # Kiểm tra xem có shortcut nào được thiết lập chưa
    shortcuts=$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)
    echo "📋 Custom shortcuts hiện tại: $shortcuts"
    
    # Kiểm tra script
    if [ -f "$HOME/.local/bin/show_hello_world_app.sh" ]; then
        echo "✅ Show script: Đã tồn tại"
        echo "   Đường dẫn: $HOME/.local/bin/show_hello_world_app.sh"
    else
        echo "❌ Show script: Chưa tồn tại"
        echo "   Chạy: ./scripts/setup_wayland_hotkey.sh"
    fi
    
    # Kiểm tra xem có shortcut Super+T không
    if echo "$shortcuts" | grep -q "hello-world-app"; then
        echo "✅ Hello World shortcut: Đã thiết lập"
        
        # Hiển thị chi tiết shortcut
        shortcut_path="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/hello-world-app/"
        name=$(gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$shortcut_path name 2>/dev/null)
        command=$(gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$shortcut_path command 2>/dev/null)
        binding=$(gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$shortcut_path binding 2>/dev/null)
        
        echo "   Name: $name"
        echo "   Command: $command"
        echo "   Binding: $binding"
    else
        echo "❌ Hello World shortcut: Chưa thiết lập"
        echo "   Chạy: ./scripts/setup_wayland_hotkey.sh"
    fi
    
else
    echo "🖥️  X11 Session - Sử dụng pynput:"
    echo "--------------------------------"
    echo "✅ Hotkey sẽ hoạt động tự động với pynput"
    echo "   Phím tắt: Super+T"
fi

echo ""

# Test chạy ứng dụng
echo "🚀 Test chạy ứng dụng:"
echo "---------------------"

if [ -f "src/hello_world_app/main.py" ]; then
    echo "✅ Main app: Tồn tại"
    echo "   Lệnh chạy: python3 -m src.hello_world_app.main"
else
    echo "❌ Main app: Không tìm thấy"
fi

echo ""

# Hướng dẫn khắc phục
echo "🔧 Khắc phục sự cố:"
echo "-------------------"

if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    echo "1️⃣  Thiết lập shortcut: ./scripts/setup_wayland_hotkey.sh"
    echo "2️⃣  Test script: ~/.local/bin/show_hello_world_app.sh"
    echo "3️⃣  Restart session nếu cần thiết"
    echo "4️⃣  Kiểm tra Settings → Keyboard → Custom Shortcuts"
else
    echo "1️⃣  Chuyển sang X11 session để sử dụng pynput"
    echo "2️⃣  Hoặc thiết lập GNOME shortcut: ./scripts/setup_wayland_hotkey.sh"
fi

echo ""
echo "🎯 Chạy ứng dụng để test:"
echo "python3 -m src.hello_world_app.main" 