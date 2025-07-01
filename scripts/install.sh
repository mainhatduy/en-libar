#!/bin/bash

# Script cài đặt và chạy Hello World Desktop App cho Fedora
# Author: Hello World Team
# Description: Tự động cài đặt dependencies và chạy ứng dụng

echo "🚀 Hello World Desktop App - Fedora Installer"
echo "=============================================="

# Kiểm tra OS
if ! grep -q "Fedora" /etc/os-release; then
    echo "❌ Script này được thiết kế cho Fedora Linux"
    echo "Vui lòng cài đặt dependencies thủ công theo hướng dẫn trong docs/README.md"
    exit 1
fi

echo "✅ Phát hiện Fedora Linux - Tiếp tục cài đặt..."

# Cập nhật package cache
echo "📦 Cập nhật package cache..."
sudo dnf check-update

# Cài đặt dependencies chính
echo "🔧 Cài đặt GTK và Python dependencies..."
sudo dnf install -y python3-gobject gtk3-devel libappindicator-gtk3-devel python3-pip python3-venv

# Cài đặt D-Bus dependencies
echo "🔄 Cài đặt D-Bus và window management tools..."
sudo dnf install -y dbus-python python3-dbus-devel xdotool

# Cài đặt extension cho GNOME (nếu đang dùng GNOME)
if [ "$XDG_CURRENT_DESKTOP" = "GNOME" ]; then
    echo "🖥️  Phát hiện GNOME desktop - Cài đặt AppIndicator extension..."
    sudo dnf install -y gnome-shell-extension-appindicator
    
    echo "ℹ️  Lưu ý: Bạn có thể cần enable extension AppIndicator trong GNOME Extensions"
    echo "   Mở 'Extensions' app và bật 'AppIndicator and KStatusNotifierItem Support'"
fi

# Kiểm tra Python version
echo "🐍 Kiểm tra Python version..."
python3 --version

# Quay về thư mục project root
cd "$(dirname "$0")/.."

# Cài đặt package
echo "📦 Cài đặt Hello World App package..."
pip3 install --user -e .

# Cài đặt desktop file (tùy chọn)
echo "🖥️  Cài đặt desktop entry..."
mkdir -p ~/.local/share/applications/
cp assets/desktop/hello-world-app.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/

# Đảm bảo script hotkey có quyền thực thi
echo "🔑 Thiết lập script hotkey..."
mkdir -p ~/.local/bin/
touch ~/.local/bin/show_hello_world_app.sh
chmod +x ~/.local/bin/show_hello_world_app.sh

echo ""
echo "✅ Cài đặt hoàn tất!"
echo ""
echo "🎯 Để chạy ứng dụng:"
echo "   hello-world-app"
echo "   hoặc từ menu ứng dụng: 'Hello World App'"
echo "   hoặc sử dụng phím tắt Super+T (Windows+T)"
echo ""
echo "📖 Đọc docs/README.md để biết thêm thông tin chi tiết"
echo ""

# Hỏi người dùng có muốn chạy luôn không
read -p "🚀 Bạn có muốn chạy ứng dụng ngay bây giờ? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🎉 Đang khởi động Hello World App..."
    hello-world-app
fi 