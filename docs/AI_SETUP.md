# Hướng dẫn thiết lập AI sinh nghĩa

## Tổng quan

Ứng dụng Hello World App hỗ trợ tính năng AI tự động sinh nghĩa cho từ vựng sử dụng Google Gemini API. Tính năng này giúp bạn nhanh chóng có được nghĩa tiếng Việt của từ tiếng Anh mà không cần tra cứu thủ công.

## Cài đặt

### 1. Cài đặt Dependencies

```bash
pip install google-genai
```

Hoặc chạy script cài đặt:

```bash
./scripts/install.sh
```

### 2. Lấy Gemini API Key

1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập bằng tài khoản Google
3. Tạo API key mới
4. Sao chép API key

### 3. Thiết lập Environment Variable

#### Cách 1: Thêm vào .bashrc (khuyến nghị)

```bash
echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

#### Cách 2: Thiết lập tạm thời

```bash
export GEMINI_API_KEY="your_api_key_here"
```

#### Cách 3: Tạo file .env (nâng cao)

Tạo file `.env` trong thư mục root của project:

```bash
GEMINI_API_KEY=your_api_key_here
```

## Sử dụng

### Trong giao diện chính

1. Nhập từ vựng vào ô "Từ vựng"
2. Nhấn nút "🤖 AI sinh nghĩa"
3. Chờ AI sinh nghĩa (thường mất 1-3 giây)
4. Nghĩa sẽ tự động điền vào ô "Nghĩa"
5. Bạn có thể chỉnh sửa nghĩa trước khi thêm vào từ điển

### Trạng thái AI

- **✅ AI đã sẵn sàng**: AI hoạt động bình thường
- **⚠️ AI chưa sẵn sàng**: Cần thiết lập API key hoặc cài đặt dependencies

## Troubleshooting

### Lỗi "AI chưa sẵn sàng"

**Nguyên nhân**: Chưa cài đặt `google-genai` hoặc chưa thiết lập API key

**Giải pháp**:
1. Cài đặt: `pip install google-genai`
2. Thiết lập GEMINI_API_KEY theo hướng dẫn trên

### Lỗi "Không thể sinh nghĩa"

**Nguyên nhân**: API key không hợp lệ, mạng có vấn đề, hoặc từ không được AI nhận diện

**Giải pháp**:
1. Kiểm tra kết nối mạng
2. Kiểm tra API key còn hạn sử dụng
3. Thử lại với từ khác
4. Nhập nghĩa thủ công

### API Rate Limit

Google Gemini có giới hạn số request miễn phí. Nếu vượt quá:
- Chờ ít phút rồi thử lại
- Xem xét nâng cấp gói API nếu cần sử dụng nhiều

## Tính năng nâng cao

### Tùy chỉnh prompt

Bạn có thể tùy chỉnh cách AI sinh nghĩa bằng cách chỉnh sửa file `src/hello_world_app/utils/ai_helper.py`, method `_create_definition_prompt()`.

### Sử dụng model khác

Mặc định sử dụng `gemini-2.0-flash-exp`. Bạn có thể thay đổi trong `ai_helper.py`:

```python
self.model = "gemini-1.5-pro"  # Hoặc model khác
```

## Bảo mật

- **Không chia sẻ API key**: Giữ API key bí mật
- **Không commit API key**: Không đưa API key vào git
- **Sử dụng environment variables**: Luôn sử dụng biến môi trường

## Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra log trong terminal khi chạy ứng dụng
2. Đọc thông báo lỗi trong giao diện
3. Tham khảo documentation của Google Gemini API

## Giới hạn

- Hiện tại chỉ hỗ trợ từ tiếng Anh → tiếng Việt
- Cần kết nối internet
- Phụ thuộc vào chất lượng của Gemini API
- Có thể không chính xác 100% với thuật ngữ chuyên môn 