"""
AI Helper module để tích hợp Gemini API
"""

import os
import json
import asyncio
from typing import Optional, Dict, Any
from ..utils.helpers import log_message

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class AIHelper:
    """Helper class để sử dụng AI sinh nghĩa từ vựng"""
    
    def __init__(self):
        self.client = None
        self.model = "gemini-2.0-flash-exp"
        self._initialize_client()
    
    def _initialize_client(self):
        """Khởi tạo Gemini client"""
        if not GEMINI_AVAILABLE:
            log_message("ERROR: google-genai không được cài đặt. Cài đặt bằng: pip install google-genai")
            return False
            
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            log_message("WARNING: GEMINI_API_KEY không được thiết lập trong environment variables")
            return False
        
        try:
            self.client = genai.Client(api_key=api_key)
            log_message("Đã khởi tạo Gemini client thành công")
            return True
        except Exception as e:
            log_message(f"ERROR: Lỗi khi khởi tạo Gemini client: {e}")
            return False
    
    def is_available(self) -> bool:
        """Kiểm tra xem AI có sẵn sàng sử dụng không"""
        return GEMINI_AVAILABLE and self.client is not None
    
    def generate_definition(self, word: str) -> Optional[str]:
        """
        Sinh nghĩa cho từ vựng sử dụng Gemini API
        
        Args:
            word: Từ vựng cần sinh nghĩa
            
        Returns:
            Nghĩa của từ (tiếng Việt) hoặc None nếu có lỗi
        """
        if not self.is_available():
            return None
        
        if not word or not word.strip():
            return None
        
        word = word.strip()
        
        try:
            # Tạo prompt để sinh nghĩa
            prompt = self._create_definition_prompt(word)
            
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)],
                ),
            ]
            
            generate_content_config = types.GenerateContentConfig(
                temperature=0.3,  # Giảm temperature để có kết quả ổn định hơn
                thinking_config=types.ThinkingConfig(
                    thinking_budget=0,
                ),
                response_mime_type="application/json",
                response_schema=genai.types.Schema(
                    type=genai.types.Type.OBJECT,
                    properties={
                        "vi": genai.types.Schema(
                            type=genai.types.Type.STRING,
                            description="Nghĩa tiếng Việt của từ",
                        ),
                        "word_type": genai.types.Schema(
                            type=genai.types.Type.STRING,
                            description="Loại từ (danh từ, động từ, tính từ...)",
                        ),
                    },
                ),
            )
            
            log_message(f"Đang sinh nghĩa cho từ: {word}")
            
            # Gọi API để sinh nghĩa
            response_chunks = []
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.text:
                    response_chunks.append(chunk.text)
            
            # Ghép và parse response
            full_response = "".join(response_chunks)
            
            if not full_response.strip():
                log_message(f"ERROR: Không nhận được response từ AI cho từ: {word}")
                return None
            
            try:
                result = json.loads(full_response)
                definition = result.get("vi", "").strip()
                word_type = result.get("word_type", "").strip()
                
                if definition:
                    # Kết hợp nghĩa và loại từ nếu có
                    final_definition = f"({word_type}) {definition}" if word_type else definition
                    log_message(f"Đã sinh nghĩa thành công cho '{word}': {final_definition}")
                    return final_definition
                else:
                    log_message(f"ERROR: Không tìm thấy nghĩa trong response cho từ: {word}")
                    return None
                    
            except json.JSONDecodeError as e:
                log_message(f"ERROR: Lỗi parse JSON response: {e}")
                log_message(f"Raw response: {full_response}")
                return None
                
        except Exception as e:
            log_message(f"ERROR: Lỗi khi sinh nghĩa cho từ '{word}': {e}")
            return None
    
    def _create_definition_prompt(self, word: str) -> str:
        """Tạo prompt để sinh nghĩa cho từ"""
        return f"""Hãy cung cấp nghĩa tiếng Việt cho từ tiếng Anh: "{word}"

Yêu cầu:
- Cung cấp nghĩa chính xác và phổ biến nhất
- Nghĩa phải ngắn gọn, dễ hiểu (1-2 câu)
- Nếu từ có nhiều nghĩa, chọn nghĩa phổ biến nhất
- Xác định loại từ (noun, verb, adjective, adverb...)

Ví dụ:
- "apple" → "quả táo"
- "run" → "chạy, điều hành"
- "beautiful" → "đẹp, xinh đẹp"

Từ cần tra: "{word}"
"""

    def get_setup_instructions(self) -> str:
        """Trả về hướng dẫn cài đặt để sử dụng AI"""
        instructions = []
        
        if not GEMINI_AVAILABLE:
            instructions.append("1. Cài đặt google-genai: pip install google-genai")
        
        if not os.environ.get("GEMINI_API_KEY"):
            instructions.append("2. Thiết lập GEMINI_API_KEY trong environment variables")
            instructions.append("   - Lấy API key tại: https://makersuite.google.com/app/apikey")
            instructions.append("   - Thêm vào ~/.bashrc: export GEMINI_API_KEY='your_api_key_here'")
        
        if not instructions:
            return "✅ AI đã sẵn sàng sử dụng!"
        
        return "⚠️ Để sử dụng AI, vui lòng:\n" + "\n".join(instructions)


# Global instance để sử dụng trong toàn bộ ứng dụng
ai_helper = AIHelper() 