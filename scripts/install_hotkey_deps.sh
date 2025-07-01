#!/bin/bash

# Script cài đặt dependencies cho tính năng hotkey
echo "Cài đặt dependencies cho tính năng hotkey Super+T..."

# Cài đặt pynput qua pip
pip3 install --user pynput>=1.7.6

if [ $? -eq 0 ]; then
    echo "✅ Đã cài đặt thành công pynput"
    echo "🎯 Bây giờ bạn có thể sử dụng Super+T để hiển thị ứng dụng từ bất kỳ đâu!"
    echo ""
    echo "Cách sử dụng:"
    echo "- Chạy ứng dụng: python3 -m src.hello_world_app.main"
    echo "- Ẩn cửa sổ xuống system tray"
    echo "- Nhấn Super+T từ bất kỳ đâu để hiển thị lại cửa sổ"
else
    echo "❌ Có lỗi khi cài đặt pynput"
    echo "Thử chạy: pip3 install --user pynput"
fi 