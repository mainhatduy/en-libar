#!/bin/bash

# Script gỡ bỏ Hello World Desktop App
# Author: Hello World Team
# Description: Gỡ bỏ hoàn toàn ứng dụng và các file liên quan

echo "🗑️  Hello World Desktop App - Uninstaller"
echo "=========================================="

# Kiểm tra xem ứng dụng có được cài đặt không
if ! command -v hello-world-app &> /dev/null; then
    echo "ℹ️  Hello World App chưa được cài đặt hoặc đã được gỡ bỏ"
    exit 0
fi

echo "🔍 Tìm thấy Hello World App đã được cài đặt"

# Hỏi xác nhận
read -p "❓ Bạn có chắc chắn muốn gỡ bỏ Hello World App? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Hủy bỏ quá trình gỡ cài đặt"
    exit 0
fi

echo "🗑️  Đang gỡ bỏ Hello World App..."

# Gỗ bỏ package
echo "📦 Gỡ bỏ package Python..."
pip3 uninstall -y hello-world-app

# Gỡ bỏ desktop file
echo "🖥️  Gỡ bỏ desktop entry..."
if [ -f ~/.local/share/applications/hello-world-app.desktop ]; then
    rm ~/.local/share/applications/hello-world-app.desktop
    echo "   ✅ Đã xóa desktop file cá nhân"
fi

if [ -f /usr/share/applications/hello-world-app.desktop ]; then
    sudo rm /usr/share/applications/hello-world-app.desktop
    echo "   ✅ Đã xóa desktop file hệ thống"
fi

# Cập nhật desktop database
update-desktop-database ~/.local/share/applications/ 2>/dev/null || true

# Gỡ bỏ config files (nếu có)
if [ -d ~/.config/hello-world-app ]; then
    read -p "❓ Bạn có muốn xóa config files không? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf ~/.config/hello-world-app
        echo "   ✅ Đã xóa config files"
    fi
fi

echo ""
echo "✅ Gỡ bỏ hoàn tất!"
echo ""
echo "ℹ️  Lưu ý: Dependencies hệ thống (GTK, python3-gobject) vẫn được giữ lại"
echo "   Bạn có thể gỡ bỏ chúng thủ công nếu cần:"
echo "   sudo dnf remove python3-gobject gtk3-devel libappindicator-gtk3-devel"
echo ""
echo "🙏 Cảm ơn bạn đã sử dụng Hello World App!" 