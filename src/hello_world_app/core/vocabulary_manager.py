"""
Vocabulary Manager - Quản lý kho từ vựng
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional
from ..utils.helpers import log_message

class VocabularyManager:
    """Class quản lý kho từ vựng"""
    
    def __init__(self):
        self.db_path = self._get_db_path()
        self._init_database()
    
    def _get_db_path(self) -> str:
        """Lấy đường dẫn database"""
        data_dir = os.path.expanduser('~/.local/share/hello-world-app')
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, 'vocabulary.db')
    
    def _init_database(self):
        """Khởi tạo database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tạo bảng vocabulary với các trường mới
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vocabulary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL UNIQUE,
                    definition TEXT NOT NULL,
                    example TEXT,
                    pronunciation TEXT,
                    part_of_speech TEXT,
                    context_sentences TEXT,
                    synonyms TEXT,
                    antonyms TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_reviewed TIMESTAMP,
                    review_count INTEGER DEFAULT 0
                )
            ''')
            
            # Thêm các cột mới vào bảng hiện có nếu chưa tồn tại
            try:
                cursor.execute('ALTER TABLE vocabulary ADD COLUMN context_sentences TEXT')
                log_message("Đã thêm cột context_sentences")
            except sqlite3.OperationalError:
                pass  # Cột đã tồn tại
            
            try:
                cursor.execute('ALTER TABLE vocabulary ADD COLUMN synonyms TEXT')
                log_message("Đã thêm cột synonyms")
            except sqlite3.OperationalError:
                pass  # Cột đã tồn tại
                
            try:
                cursor.execute('ALTER TABLE vocabulary ADD COLUMN antonyms TEXT')
                log_message("Đã thêm cột antonyms")
            except sqlite3.OperationalError:
                pass  # Cột đã tồn tại
            
            conn.commit()
            conn.close()
            log_message(f"Database đã sẵn sàng: {self.db_path}")
            
        except Exception as e:
            log_message(f"Lỗi khởi tạo database: {e}", "ERROR")
    
    def add_vocabulary(self, word: str, definition: str, example: str = "", 
                      pronunciation: str = "", part_of_speech: str = "",
                      context_sentences: str = "", synonyms: str = "", antonyms: str = "") -> bool:
        """Thêm từ vựng mới với tất cả các trường"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO vocabulary (word, definition, example, pronunciation, part_of_speech, 
                                      context_sentences, synonyms, antonyms)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (word.strip(), definition.strip(), example.strip(), 
                  pronunciation.strip(), part_of_speech.strip(),
                  context_sentences.strip(), synonyms.strip(), antonyms.strip()))
            
            conn.commit()
            conn.close()
            log_message(f"Đã thêm từ vựng: {word}")
            return True
            
        except sqlite3.IntegrityError:
            log_message(f"Từ '{word}' đã tồn tại", "WARNING")
            return False
        except Exception as e:
            log_message(f"Lỗi thêm từ vựng: {e}", "ERROR")
            return False
    
    def update_vocabulary(self, vocab_id: int, word: str, definition: str, 
                         example: str = "", pronunciation: str = "", 
                         part_of_speech: str = "", context_sentences: str = "",
                         synonyms: str = "", antonyms: str = "") -> bool:
        """Cập nhật từ vựng với tất cả các trường"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE vocabulary 
                SET word = ?, definition = ?, example = ?, 
                    pronunciation = ?, part_of_speech = ?, context_sentences = ?,
                    synonyms = ?, antonyms = ?
                WHERE id = ?
            ''', (word.strip(), definition.strip(), example.strip(),
                  pronunciation.strip(), part_of_speech.strip(), context_sentences.strip(),
                  synonyms.strip(), antonyms.strip(), vocab_id))
            
            conn.commit()
            conn.close()
            log_message(f"Đã cập nhật từ vựng: {word}")
            return True
            
        except Exception as e:
            log_message(f"Lỗi cập nhật từ vựng: {e}", "ERROR")
            return False
    
    def delete_vocabulary(self, vocab_id: int) -> bool:
        """Xóa từ vựng"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM vocabulary WHERE id = ?', (vocab_id,))
            
            conn.commit()
            conn.close()
            log_message(f"Đã xóa từ vựng ID: {vocab_id}")
            return True
            
        except Exception as e:
            log_message(f"Lỗi xóa từ vựng: {e}", "ERROR")
            return False
    
    def get_all_vocabulary(self) -> List[Dict]:
        """Lấy tất cả từ vựng"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, word, definition, example, pronunciation, 
                       part_of_speech, context_sentences, synonyms, antonyms,
                       created_at, last_reviewed, review_count
                FROM vocabulary 
                ORDER BY created_at DESC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            vocabularies = []
            for row in rows:
                vocabularies.append({
                    'id': row[0],
                    'word': row[1],
                    'definition': row[2],
                    'example': row[3],
                    'pronunciation': row[4],
                    'part_of_speech': row[5],
                    'context_sentences': row[6],
                    'synonyms': row[7],
                    'antonyms': row[8],
                    'created_at': row[9],
                    'last_reviewed': row[10],
                    'review_count': row[11]
                })
            
            return vocabularies
            
        except Exception as e:
            log_message(f"Lỗi lấy danh sách từ vựng: {e}", "ERROR")
            return []
    
    def search_vocabulary(self, search_term: str) -> List[Dict]:
        """Tìm kiếm từ vựng"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            search_pattern = f"%{search_term.strip()}%"
            cursor.execute('''
                SELECT id, word, definition, example, pronunciation, 
                       part_of_speech, context_sentences, synonyms, antonyms,
                       created_at, last_reviewed, review_count
                FROM vocabulary 
                WHERE word LIKE ? OR definition LIKE ? OR example LIKE ? 
                   OR context_sentences LIKE ? OR synonyms LIKE ? OR antonyms LIKE ?
                ORDER BY created_at DESC
            ''', (search_pattern, search_pattern, search_pattern, 
                  search_pattern, search_pattern, search_pattern))
            
            rows = cursor.fetchall()
            conn.close()
            
            vocabularies = []
            for row in rows:
                vocabularies.append({
                    'id': row[0],
                    'word': row[1],
                    'definition': row[2],
                    'example': row[3],
                    'pronunciation': row[4],
                    'part_of_speech': row[5],
                    'context_sentences': row[6],
                    'synonyms': row[7],
                    'antonyms': row[8],
                    'created_at': row[9],
                    'last_reviewed': row[10],
                    'review_count': row[11]
                })
            
            return vocabularies
            
        except Exception as e:
            log_message(f"Lỗi tìm kiếm từ vựng: {e}", "ERROR")
            return []
    
    def mark_as_reviewed(self, vocab_id: int) -> bool:
        """Đánh dấu từ vựng đã được ôn tập"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE vocabulary 
                SET last_reviewed = CURRENT_TIMESTAMP, 
                    review_count = review_count + 1
                WHERE id = ?
            ''', (vocab_id,))
            
            conn.commit()
            conn.close()
            log_message(f"Đã đánh dấu ôn tập từ vựng ID: {vocab_id}")
            return True
            
        except Exception as e:
            log_message(f"Lỗi đánh dấu ôn tập: {e}", "ERROR")
            return False
    
    def get_vocabulary_stats(self) -> Dict:
        """Lấy thống kê từ vựng"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tổng số từ
            cursor.execute('SELECT COUNT(*) FROM vocabulary')
            total_words = cursor.fetchone()[0]
            
            # Số từ đã ôn tập
            cursor.execute('SELECT COUNT(*) FROM vocabulary WHERE last_reviewed IS NOT NULL')
            reviewed_words = cursor.fetchone()[0]
            
            # Số từ chưa ôn tập
            unreviewed_words = total_words - reviewed_words
            
            # Số từ thêm hôm nay
            cursor.execute('''
                SELECT COUNT(*) FROM vocabulary 
                WHERE DATE(created_at) = DATE('now')
            ''')
            today_words = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_words': total_words,
                'reviewed_words': reviewed_words,
                'unreviewed_words': unreviewed_words,
                'today_words': today_words
            }
            
        except Exception as e:
            log_message(f"Lỗi lấy thống kê: {e}", "ERROR")
            return {
                'total_words': 0,
                'reviewed_words': 0,
                'unreviewed_words': 0,
                'today_words': 0
            }
    
    def get_random_vocabulary(self, limit: int = 10) -> List[Dict]:
        """Lấy từ vựng ngẫu nhiên để ôn tập"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, word, definition, example, pronunciation, 
                       part_of_speech, context_sentences, synonyms, antonyms,
                       created_at, last_reviewed, review_count
                FROM vocabulary 
                ORDER BY RANDOM()
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            vocabularies = []
            for row in rows:
                vocabularies.append({
                    'id': row[0],
                    'word': row[1],
                    'definition': row[2],
                    'example': row[3],
                    'pronunciation': row[4],
                    'part_of_speech': row[5],
                    'context_sentences': row[6],
                    'synonyms': row[7],
                    'antonyms': row[8],
                    'created_at': row[9],
                    'last_reviewed': row[10],
                    'review_count': row[11]
                })
            
            return vocabularies
            
        except Exception as e:
            log_message(f"Lỗi lấy từ vựng ngẫu nhiên: {e}", "ERROR")
            return [] 