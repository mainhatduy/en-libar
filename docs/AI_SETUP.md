# Hướng dẫn thiết lập AI sinh dữ liệu từ vựng đầy đủ

## Tổng quan

Ứng dụng Hello World App hỗ trợ tính năng AI tự động sinh **dữ liệu từ vựng đầy đủ** sử dụng Google Gemini API. Tính năng này không chỉ sinh nghĩa tiếng Việt mà còn cung cấp:

- **Nghĩa tiếng Việt**: Nghĩa chính xác và phổ biến nhất
- **Loại từ**: Danh từ, động từ, tính từ, trạng từ...
- **Phát âm**: Ký hiệu IPA hoặc phiên âm đơn giản
- **Ngữ cảnh sử dụng**: Ít nhất 2 câu ví dụ thực tế
- **Từ đồng nghĩa**: Danh sách các từ có nghĩa tương tự
- **Từ trái nghĩa**: Danh sách các từ có nghĩa đối lập

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

### Tính năng mới: AI sinh dữ liệu đầy đủ

#### Trong giao diện chế độ quản lý đầy đủ:

1. Nhập từ vựng vào ô "Từ vựng"
2. Nhấn nút **"🤖 AI sinh dữ liệu đầy đủ"**
3. Chờ AI sinh dữ liệu (thường mất 3-5 giây)
4. Tất cả các trường sẽ được điền tự động:
   - Nghĩa tiếng Việt
   - Loại từ
   - Phát âm
   - Ngữ cảnh sử dụng
   - Từ đồng nghĩa
   - Từ trái nghĩa
5. Bạn có thể chỉnh sửa bất kỳ trường nào trước khi lưu
6. Nhấn **"💾 Lưu từ vựng"** để lưu vào database

#### Trong giao diện chính (tương thích ngược):

1. Nhập từ vựng vào ô "Từ vựng"
2. Nhấn nút "🤖 AI sinh nghĩa"
3. Chờ AI sinh nghĩa (thường mất 1-3 giây)
4. Nghĩa sẽ tự động điền vào ô "Nghĩa"
5. Bạn có thể chỉnh sửa nghĩa trước khi thêm vào từ điển

### Ví dụ kết quả AI sinh cho từ "beautiful":

```
📝 Nghĩa tiếng Việt: đẹp, xinh đẹp
📚 Loại từ: adjective
🔊 Phát âm: /ˈbjuːtɪfəl/
💬 Ngữ cảnh sử dụng:
   • She wore a beautiful dress to the party.
   • The sunset was beautiful tonight.
🔄 Từ đồng nghĩa: gorgeous, lovely, attractive, pretty
🔀 Từ trái nghĩa: ugly, hideous, unattractive
```

### Trạng thái AI

- **✅ AI đã sẵn sàng**: AI hoạt động bình thường
- **⚠️ AI chưa sẵn sàng**: Cần thiết lập API key hoặc cài đặt dependencies

## Test tính năng

### Chạy script test:

```bash
python scripts/test_ai_comprehensive.py
```

Script này sẽ:
- Kiểm tra AI có sẵn sàng không
- Test sinh dữ liệu cho 5 từ mẫu
- Lưu kết quả vào database
- Hiển thị thống kê

### Xem database:

```bash
sqlite3 ~/.local/share/hello-world-app/vocabulary.db "SELECT word, definition, synonyms, antonyms FROM vocabulary LIMIT 5;"
```

## Troubleshooting

### Lỗi "AI chưa sẵn sàng"

**Nguyên nhân**: Chưa cài đặt `google-genai` hoặc chưa thiết lập API key

**Giải pháp**:
1. Cài đặt: `pip install google-genai`
2. Thiết lập GEMINI_API_KEY theo hướng dẫn trên

### Lỗi "Không thể sinh dữ liệu"

**Nguyên nhân**: API key không hợp lệ, mạng có vấn đề, hoặc từ không được AI nhận diện

**Giải pháp**:
1. Kiểm tra API key có hợp lệ
2. Kiểm tra kết nối mạng
3. Thử lại với từ khác
4. Nhập dữ liệu thủ công nếu cần

### Lỗi timeout hoặc chậm

**Nguyên nhân**: API Gemini đang chậm hoặc quá tải

**Giải pháp**:
1. Đợi và thử lại
2. Kiểm tra kết nối mạng
3. Sử dụng tính năng "AI sinh nghĩa" đơn giản thay vì sinh dữ liệu đầy đủ

### Database schema cũ

Nếu bạn đã sử dụng phiên bản cũ, database sẽ tự động được cập nhật với các cột mới:
- `context_sentences`
- `synonyms` 
- `antonyms`

Không cần làm gì thêm, hệ thống sẽ tự động migration.

## Tính năng nâng cao

### API Response Schema

AI trả về dữ liệu theo format JSON:

```json
{
  "vietnamese_meaning": "đẹp, xinh đẹp",
  "word_type": "adjective", 
  "pronunciation": "/ˈbjuːtɪfəl/",
  "context_sentences": [
    "She wore a beautiful dress to the party.",
    "The sunset was beautiful tonight."
  ],
  "synonyms": ["gorgeous", "lovely", "attractive", "pretty"],
  "antonyms": ["ugly", "hideous", "unattractive"]
}
```

### Tùy chỉnh Prompt

Bạn có thể tùy chỉnh prompt trong file `src/hello_world_app/utils/ai_helper.py` tại method `_create_comprehensive_prompt()`.

### Database Schema

Bảng `vocabulary` hiện có các cột:

- `id`: ID tự động tăng
- `word`: Từ vựng
- `definition`: Nghĩa tiếng Việt  
- `example`: Ví dụ đơn giản
- `pronunciation`: Phát âm
- `part_of_speech`: Loại từ
- `context_sentences`: Ngữ cảnh sử dụng (mới)
- `synonyms`: Từ đồng nghĩa (mới)
- `antonyms`: Từ trái nghĩa (mới)
- `created_at`: Thời gian tạo
- `last_reviewed`: Lần ôn tập cuối
- `review_count`: Số lần ôn tập

## Support

Nếu gặp vấn đề, hãy:

1. Kiểm tra log trong terminal
2. Chạy script test để debug
3. Kiểm tra thiết lập API key
4. Báo cáo lỗi kèm log chi tiết 