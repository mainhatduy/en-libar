# Hello World Desktop App

Một ứng dụng desktop đơn giản được viết bằng Python với GTK cho Fedora Linux.

## Cài đặt nhanh

```bash
# Cài đặt tự động (khuyến nghị)
./scripts/install.sh

# Cài đặt dependencies cho tính năng hotkey
./scripts/install_hotkey_deps.sh

# Hoặc cài đặt thủ công
sudo dnf install python3-gobject gtk3-devel libappindicator-gtk3-devel
pip install -e .
pip install --user pynput>=1.7.6  # Cho tính năng hotkey
```

## Chạy ứng dụng

```bash
hello-world-app
```

## Tính năng nổi bật

🎯 **Global Hotkey**: Nhấn **Super+T** từ bất kỳ đâu để hiển thị ứng dụng nhanh chóng!  
🔧 **System Tray**: Ứng dụng có thể chạy nền và hiển thị trong system tray  
💼 **Modern GUI**: Giao diện đẹp mắt với GTK3  

## Cách sử dụng

1. Chạy ứng dụng: `hello-world-app`
2. Sử dụng nút "Ẩn xuống System Tray" để ẩn cửa sổ
3. Nhấn **Super+T** từ bất kỳ ứng dụng nào để hiển thị lại cửa sổ
4. Hoặc click chuột phải vào icon trong system tray để hiển thị menu

## Cấu trúc project

Đây là một Python package được cấu trúc theo chuẩn hiện đại:

- **`src/hello_world_app/`** - Main package code
- **`tests/`** - Test suite  
- **`docs/`** - Documentation chi tiết
- **`assets/`** - Icons và desktop files
- **`scripts/`** - Installation scripts

## Documentation

Xem documentation chi tiết tại [docs/README.md](docs/README.md)

## Features

✅ Modern Python package structure  
✅ GTK GUI với system tray support  
✅ **Global hotkey Super+T support**  
✅ Proper testing setup  
✅ Development tools (black, flake8, pytest)  
✅ Easy installation với setup.py  
✅ Desktop integration  

## Development

```bash
# Setup development environment
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/
```

## License

MIT License - xem [LICENSE](LICENSE) để biết thêm chi tiết. 