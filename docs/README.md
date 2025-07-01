# Hello World Desktop App cho Fedora

Một ứng dụng desktop đơn giản được viết bằng Python với GTK, có khả năng chạy nền và hiển thị trong system tray trên Fedora Linux.

## Tính năng

- ✅ Giao diện GTK đẹp mắt và thân thiện
- ✅ Có thể ẩn xuống system tray
- ✅ Chạy nền trong background apps
- ✅ Menu context trong system tray
- ✅ Hiển thị thời gian thực
- ✅ Tương thích với GNOME desktop environment
- ✅ Cấu trúc code theo chuẩn Python package
- ✅ Hỗ trợ testing và development tools

## Yêu cầu hệ thống

- **Hệ điều hành:** Fedora Linux (phiên bản 35+)
- **Desktop Environment:** GNOME (hoặc bất kỳ DE nào hỗ trợ GTK)
- **Python:** 3.8+

## Cài đặt

### Phương pháp 1: Cài đặt qua setup.py

```bash
# Cài đặt dependencies hệ thống
sudo dnf install python3-gobject gtk3-devel libappindicator-gtk3-devel

# Clone repository
git clone <repository-url>
cd EN-Project

# Cài đặt package
pip install -e .

# Chạy ứng dụng
hello-world-app
```

### Phương pháp 2: Development setup

```bash
# Cài đặt dependencies hệ thống
sudo dnf install python3-gobject gtk3-devel libappindicator-gtk3-devel

# Clone repository
git clone <repository-url>
cd EN-Project

# Tạo virtual environment
python -m venv venv
source venv/bin/activate

# Cài đặt development dependencies
pip install -e ".[dev]"

# Chạy từ source
python -m hello_world_app.main
```

### Phương pháp 3: Sử dụng script tự động

```bash
# Chạy script cài đặt tự động
./scripts/install.sh
```

## Cấu trúc project

```
EN-Project/
├── src/
│   └── hello_world_app/          # Main package
│       ├── __init__.py
│       ├── main.py               # Entry point
│       ├── gui/                  # GUI components
│       │   ├── __init__.py
│       │   ├── main_window.py    # Main window
│       │   └── system_tray.py    # System tray
│       ├── core/                 # Core logic
│       │   ├── __init__.py
│       │   ├── app.py           # Main application
│       │   └── config.py        # Configuration
│       └── utils/               # Utilities
│           ├── __init__.py
│           └── helpers.py       # Helper functions
├── assets/
│   ├── icons/                   # App icons
│   └── desktop/                 # Desktop files
├── scripts/                     # Installation scripts
├── tests/                       # Test suite
├── docs/                        # Documentation
├── setup.py                     # Setup script
├── pyproject.toml              # Modern Python config
├── requirements.txt            # Dependencies
└── requirements-dev.txt        # Dev dependencies
```

## Sử dụng

### Giao diện chính
- Ứng dụng sẽ hiển thị cửa sổ với thông điệp "Hello World!"
- Hiển thị thời gian hiện tại
- Có 2 nút: "Ẩn xuống System Tray" và "Thoát ứng dụng"

### System Tray
- Click nút "Ẩn xuống System Tray" để ẩn cửa sổ
- Ứng dụng sẽ tiếp tục chạy nền và hiển thị icon trong system tray
- Right-click vào icon trong system tray để xem menu:
  - **Hiển thị cửa sổ:** Mở lại cửa sổ chính
  - **Thoát:** Đóng ứng dụng hoàn toàn

### Phím tắt
- **Ctrl+C:** Dừng ứng dụng khi chạy từ terminal
- **Đóng cửa sổ (X):** Ẩn xuống system tray thay vì thoát

## Development

### Chạy tests

```bash
# Chạy tất cả tests
pytest

# Chạy tests với coverage
pytest --cov=hello_world_app

# Chạy tests cụ thể
pytest tests/test_main.py
```

### Code quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Build package

```bash
# Build wheel
python -m build

# Install locally
pip install dist/hello_world_app-1.0.0-py3-none-any.whl
```

## Troubleshooting

### Lỗi "No module named 'gi'"
```bash
sudo dnf install python3-gobject
```

### System tray không hiển thị
```bash
# Đối với GNOME, cài extension
sudo dnf install gnome-shell-extension-appindicator
# Sau đó enable extension trong GNOME Extensions app
```

### Lỗi AppIndicator3
```bash
sudo dnf install libappindicator-gtk3-devel
```

### ImportError khi chạy từ source
```bash
# Đảm bảo PYTHONPATH được set đúng
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python -m hello_world_app.main
```

## Đóng góp

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

### Development workflow

```bash
# Setup development environment
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Make changes và test
pytest
black src/ tests/
flake8 src/ tests/

# Commit và push
git add .
git commit -m "Description of changes"
git push
```

## Giấy phép

Ứng dụng này được phát hành dưới giấy phép MIT. Bạn có thể tự do sử dụng, chỉnh sửa và phân phối.

## Tác giả

- Hello World Team (team@helloworld.app)

## Links

- [Repository](https://github.com/your-username/hello-world-app)
- [Issues](https://github.com/your-username/hello-world-app/issues)
- [Documentation](https://github.com/your-username/hello-world-app/blob/main/docs/README.md) 