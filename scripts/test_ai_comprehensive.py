#!/usr/bin/env python3
"""
Test script cho tính năng AI sinh dữ liệu từ vựng đầy đủ

Chạy script này để test tính năng AI mới:
python scripts/test_ai_comprehensive.py
"""

import sys
import os

# Thêm src vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hello_world_app.utils.ai_helper import ai_helper
from hello_world_app.core.vocabulary_manager import VocabularyManager
from hello_world_app.utils.helpers import log_message

def test_ai_comprehensive():
    """Test tính năng AI sinh dữ liệu đầy đủ"""
    
    print("🤖 Test tính năng AI sinh dữ liệu từ vựng đầy đủ")
    print("=" * 60)
    
    # Kiểm tra AI có sẵn sàng không
    if not ai_helper.is_available():
        print("❌ AI chưa sẵn sàng!")
        print(ai_helper.get_setup_instructions())
        return False
    
    print("✅ AI đã sẵn sàng!")
    print()
    
    # Test với một số từ mẫu
    test_words = ["beautiful", "run", "happiness", "technology", "ocean"]
    
    vocab_manager = VocabularyManager()
    
    for word in test_words:
        print(f"🔍 Đang test từ: '{word}'")
        print("-" * 40)
        
        # Sinh dữ liệu đầy đủ
        data = ai_helper.generate_comprehensive_vocabulary_data(word)
        
        if data:
            print(f"📝 Nghĩa tiếng Việt: {data.get('vietnamese_meaning', 'Không có')}")
            print(f"📚 Loại từ: {data.get('word_type', 'Không có')}")
            print(f"🔊 Phát âm: {data.get('pronunciation', 'Không có')}")
            
            print(f"💬 Ngữ cảnh sử dụng:")
            context = data.get('context_sentences', '')
            if context:
                for line in context.split('\n'):
                    if line.strip():
                        print(f"   • {line.strip()}")
            else:
                print("   • Không có")
            
            print(f"🔄 Từ đồng nghĩa: {data.get('synonyms', 'Không có')}")
            print(f"🔀 Từ trái nghĩa: {data.get('antonyms', 'Không có')}")
            
            # Lưu vào database
            success = vocab_manager.add_vocabulary(
                word=word,
                definition=data.get('vietnamese_meaning', ''),
                example="",  # Để trống vì đã có context_sentences
                pronunciation=data.get('pronunciation', ''),
                part_of_speech=data.get('word_type', ''),
                context_sentences=data.get('context_sentences', ''),
                synonyms=data.get('synonyms', ''),
                antonyms=data.get('antonyms', '')
            )
            
            if success:
                print("✅ Đã lưu vào database thành công!")
            else:
                print("⚠️ Từ đã tồn tại trong database")
            
        else:
            print("❌ Không thể sinh dữ liệu cho từ này")
        
        print()
    
    # Hiển thị thống kê
    stats = vocab_manager.get_vocabulary_stats()
    print("📊 Thống kê database:")
    print(f"   • Tổng số từ: {stats['total_words']}")
    print(f"   • Từ thêm hôm nay: {stats['today_words']}")
    
    return True

def test_backwards_compatibility():
    """Test tính năng tương thích ngược với generate_definition"""
    
    print("\n🔄 Test tính năng tương thích ngược")
    print("=" * 60)
    
    test_words = ["computer", "love"]
    
    for word in test_words:
        print(f"🔍 Test generate_definition cho: '{word}'")
        definition = ai_helper.generate_definition(word)
        
        if definition:
            print(f"📝 Kết quả: {definition}")
        else:
            print("❌ Không thể sinh nghĩa")
        print()

if __name__ == "__main__":
    print("🚀 Bắt đầu test tính năng AI...")
    print()
    
    try:
        # Test tính năng chính
        success = test_ai_comprehensive()
        
        if success:
            # Test tương thích ngược
            test_backwards_compatibility()
            
            print("🎉 Test hoàn tất!")
            print("\n💡 Bây giờ bạn có thể:")
            print("   1. Chạy ứng dụng: python -m hello_world_app")
            print("   2. Thử tính năng 'AI sinh dữ liệu đầy đủ' trong giao diện")
            print("   3. Kiểm tra database tại: ~/.local/share/hello-world-app/vocabulary.db")
            
    except KeyboardInterrupt:
        print("\n⚠️ Test bị hủy bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi trong quá trình test: {e}")
        import traceback
        traceback.print_exc() 