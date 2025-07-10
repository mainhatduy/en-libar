"""
AI Helper module để tích hợp Gemini API
"""

import os
import json
import asyncio
from typing import Optional, Dict, Any
from ..utils.helpers import log_message
from ..core.config_manager import config_manager

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
            
        # Sử dụng config manager để lấy API key
        api_key = config_manager.get_gemini_api_key()
        if not api_key:
            log_message("WARNING: GEMINI_API_KEY không được thiết lập. Vui lòng thiết lập trong Settings hoặc environment variables")
            return False
        
        try:
            self.client = genai.Client(api_key=api_key)
            # Cập nhật model từ config nếu có
            model_config = config_manager.get('ai.model', self.model)
            if model_config:
                self.model = model_config
            log_message("Đã khởi tạo Gemini client thành công")
            return True
        except Exception as e:
            log_message(f"ERROR: Lỗi khi khởi tạo Gemini client: {e}")
            return False
    
    def is_available(self) -> bool:
        """Kiểm tra xem AI có sẵn sàng sử dụng không"""
        return GEMINI_AVAILABLE and self.client is not None
    
    def reinitialize(self):
        """Khởi tạo lại client (gọi sau khi cập nhật API key)"""
        return self._initialize_client()
    
    def generate_comprehensive_vocabulary_data(self, word: str) -> Optional[Dict]:
        """
        Sinh đầy đủ dữ liệu từ vựng sử dụng Gemini API
        
        Args:
            word: Từ vựng cần sinh dữ liệu
            
        Returns:
            Dict chứa tất cả thông tin từ vựng hoặc None nếu có lỗi
        """
        if not self.is_available():
            return None
        
        if not word or not word.strip():
            return None
        
        word = word.strip()
        
        try:
            # Tạo prompt để sinh dữ liệu đầy đủ
            prompt = self._create_comprehensive_prompt(word)
            
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
                        "vietnamese_meaning": genai.types.Schema(
                            type=genai.types.Type.STRING,
                            description="Nghĩa tiếng Việt của từ",
                        ),
                        "word_type": genai.types.Schema(
                            type=genai.types.Type.STRING,
                            description="Loại từ (danh từ, động từ, tính từ...)",
                        ),
                        "pronunciation": genai.types.Schema(
                            type=genai.types.Type.STRING,
                            description="Phát âm IPA của từ",
                        ),
                        "context_sentences": genai.types.Schema(
                            type=genai.types.Type.ARRAY,
                            items=genai.types.Schema(type=genai.types.Type.STRING),
                            description="Ít nhất 2 câu ví dụ sử dụng từ trong ngữ cảnh",
                        ),
                        "synonyms": genai.types.Schema(
                            type=genai.types.Type.ARRAY,
                            items=genai.types.Schema(type=genai.types.Type.STRING),
                            description="Danh sách từ đồng nghĩa",
                        ),
                        "antonyms": genai.types.Schema(
                            type=genai.types.Type.ARRAY,
                            items=genai.types.Schema(type=genai.types.Type.STRING),
                            description="Danh sách từ trái nghĩa",
                        ),
                    },
                ),
            )
            
            log_message(f"Đang sinh dữ liệu đầy đủ cho từ: {word}")
            
            # Gọi API để sinh dữ liệu
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
                
                # Xử lý và format dữ liệu
                processed_data = {
                    'vietnamese_meaning': result.get("vietnamese_meaning", "").strip(),
                    'word_type': result.get("word_type", "").strip(),
                    'pronunciation': result.get("pronunciation", "").strip(),
                    'context_sentences': "\n".join(result.get("context_sentences", [])),
                    'synonyms': ", ".join(result.get("synonyms", [])),
                    'antonyms': ", ".join(result.get("antonyms", []))
                }
                
                log_message(f"Đã sinh dữ liệu thành công cho '{word}'")
                return processed_data
                    
            except json.JSONDecodeError as e:
                log_message(f"ERROR: Lỗi parse JSON response: {e}")
                log_message(f"Raw response: {full_response}")
                return None
                
        except Exception as e:
            log_message(f"ERROR: Lỗi khi sinh dữ liệu cho từ '{word}': {e}")
            return None

    def generate_definition(self, word: str) -> Optional[str]:
        """
        Sinh nghĩa đơn giản cho từ vựng (để tương thích ngược)
        
        Args:
            word: Từ vựng cần sinh nghĩa
            
        Returns:
            Nghĩa của từ (tiếng Việt) hoặc None nếu có lỗi
        """
        comprehensive_data = self.generate_comprehensive_vocabulary_data(word)
        if comprehensive_data and comprehensive_data.get('vietnamese_meaning'):
            vietnamese_meaning = comprehensive_data['vietnamese_meaning']
            word_type = comprehensive_data.get('word_type', '')
            
            # Kết hợp nghĩa và loại từ nếu có
            if word_type:
                return f"({word_type}) {vietnamese_meaning}"
            else:
                return vietnamese_meaning
        
        return None
    
    def _create_comprehensive_prompt(self, word: str) -> str:
        """Tạo prompt để sinh dữ liệu đầy đủ cho từ"""
        return f"""Hãy cung cấp thông tin đầy đủ cho từ tiếng Anh: "{word}"

Yêu cầu cung cấp:
1. Nghĩa tiếng Việt: Nghĩa chính xác và phổ biến nhất (ngắn gọn, dễ hiểu)
2. Loại từ: Xác định chính xác (noun, verb, adjective, adverb, preposition, conjunction, pronoun, interjection)
3. Phát âm: Ký hiệu IPA hoặc phiên âm đơn giản
4. Ngữ cảnh sử dụng: Ít nhất 2 câu ví dụ thực tế có nghĩa trong tiếng Anh
5. Từ đồng nghĩa: Danh sách các từ có nghĩa tương tự (nếu có)
6. Từ trái nghĩa: Danh sách các từ có nghĩa đối lập (nếu có)

Ví dụ format:
- "beautiful" → 
  * Nghĩa: "đẹp, xinh đẹp"
  * Loại từ: "adjective"
  * Phát âm: "/ˈbjuːtɪfəl/"
  * Ngữ cảnh: ["She wore a beautiful dress to the party.", "The sunset was beautiful tonight."]
  * Đồng nghĩa: ["gorgeous", "lovely", "attractive", "pretty"]
  * Trái nghĩa: ["ugly", "hideous", "unattractive"]

Từ cần phân tích: "{word}"

Lưu ý:
- Nếu từ không có đồng nghĩa hoặc trái nghĩa phù hợp, trả về mảng rỗng
- Ngữ cảnh phải là câu hoàn chỉnh và có ý nghĩa thực tế
- Ưu tiên nghĩa phổ biến nhất nếu từ có nhiều nghĩa
"""

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
        
        api_key = config_manager.get_gemini_api_key()
        if not api_key:
            instructions.append("2. Thiết lập GEMINI_API_KEY:")
            instructions.append("   - Vào Settings > AI Configuration để nhập API key")
            instructions.append("   - Hoặc thiết lập environment variable: export GEMINI_API_KEY='your_key'")
            instructions.append("   - Lấy API key tại: https://makersuite.google.com/app/apikey")
        
        if not instructions:
            return "✅ AI đã sẵn sàng sử dụng!"
        
        return "⚠️ Để sử dụng AI, vui lòng:\n" + "\n".join(instructions)


# Global instance để sử dụng trong toàn bộ ứng dụng
ai_helper = AIHelper() 