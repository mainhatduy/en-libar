#!/bin/bash

# Script thiết lập hotkey Super+T cho Hello World App trên Wayland/GNOME
echo "🔧 Thiết lập phím tắt Super+T cho Hello World App trên Wayland..."

# Kiểm tra môi trường
if [ "$XDG_SESSION_TYPE" != "wayland" ]; then
    echo "⚠️  Bạn không đang chạy Wayland session."
    echo "Script này chỉ dành cho Wayland. Trên X11, ứng dụng sẽ tự động hoạt động."
    exit 1
fi

# Tạo thư mục cho script
mkdir -p ~/.local/bin

# Tạo script để hiển thị ứng dụng
cat > ~/.local/bin/show_hello_world_app.sh << 'EOF'
#!/bin/bash
# Script để hiển thị Hello World App với logic focus/show window

PROJECT_DIR="$HOME/Learn/EN-Project"
PID_FILE="$HOME/.local/share/hello-world-app/app.pid"

# Function để kiểm tra process có đang chạy không
is_app_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE" 2>/dev/null)
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            # Kiểm tra xem process có đúng là hello_world_app không
            if ps -p "$pid" -o cmd= | grep -q "hello_world_app.main"; then
                echo "$pid"
                return 0
            fi
        fi
        # PID file không hợp lệ, xóa nó
        rm -f "$PID_FILE" 2>/dev/null
    fi
    return 1
}

# Kiểm tra xem ứng dụng có đang chạy không
if app_pid=$(is_app_running); then
    echo "Ứng dụng đang chạy (PID: $app_pid), đưa cửa sổ lên foreground..."
    
    # Thử các cách khác nhau để đưa cửa sổ lên
    success=false
    
    # Cách 1: Gửi SIGUSR1 signal để app tự hiển thị
    if kill -USR1 "$app_pid" 2>/dev/null; then
        echo "✅ Đã gửi signal hiển thị cửa sổ"
        success=true
    fi
    
    # Cách 2: Sử dụng wmctrl nếu có
    if command -v wmctrl >/dev/null 2>&1; then
        wmctrl -a "Hello World" 2>/dev/null && success=true
    fi
    
    # Cách 3: Sử dụng xdotool nếu có (cho X11)
    if [ "$XDG_SESSION_TYPE" = "x11" ] && command -v xdotool >/dev/null 2>&1; then
        window_id=$(xdotool search --name "Hello World" 2>/dev/null | head -1)
        if [ -n "$window_id" ]; then
            xdotool windowactivate "$window_id" 2>/dev/null && success=true
        fi
    fi
    
    if [ "$success" = false ]; then
        echo "⚠️  Không thể đưa cửa sổ lên, thử khởi động lại..."
        kill "$app_pid" 2>/dev/null
        sleep 1
        cd "$PROJECT_DIR"
        python3 -m src.hello_world_app.main &
    fi
else
    echo "Khởi động ứng dụng mới..."
    cd "$PROJECT_DIR"
    python3 -m src.hello_world_app.main &
fi
EOF

# Làm script có thể thực thi
chmod +x ~/.local/bin/show_hello_world_app.sh

# Thiết lập GNOME custom shortcut
echo "📝 Thiết lập GNOME custom shortcut..."

# Lấy shortcuts hiện tại
current_shortcuts=$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)

# Đường dẫn cho shortcut mới
shortcut_path="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/hello-world-app/"

# Thêm shortcut mới vào danh sách
if [ "$current_shortcuts" = "@as []" ]; then
    new_shortcuts="['$shortcut_path']"
else
    # Remove brackets và thêm shortcut mới
    trimmed=${current_shortcuts:1:-1}  # Remove [ ]
    new_shortcuts="[$trimmed, '$shortcut_path']"
fi

# Áp dụng cấu hình
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "$new_shortcuts"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$shortcut_path name "Show Hello World App"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$shortcut_path command "$HOME/.local/bin/show_hello_world_app.sh"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$shortcut_path binding "<Super>t"

echo "✅ Đã thiết lập thành công!"
echo ""
echo "🎯 Cách sử dụng:"
echo "   • Nhấn Super+T từ bất kỳ đâu để hiển thị ứng dụng"
echo "   • Nếu không hoạt động ngay, hãy logout và login lại"
echo ""
echo "🔍 Kiểm tra thủ công:"
echo "   Settings → Keyboard → Keyboard Shortcuts → Custom Shortcuts"
echo "   Bạn sẽ thấy 'Show Hello World App' với phím tắt Super+T"
echo ""
echo "⚡ Test ngay bây giờ:"
echo "   ~/.local/bin/show_hello_world_app.sh" 