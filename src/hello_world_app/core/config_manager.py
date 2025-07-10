"""
Config Manager - Quản lý cấu hình ứng dụng
"""

import os
import json
import logging
from typing import Dict, Any, Optional

class ConfigManager:
    """Class quản lý cấu hình ứng dụng"""
    
    def __init__(self):
        self.config_dir = os.path.expanduser('~/.local/share/hello-world-app')
        self.config_file = os.path.join(self.config_dir, 'config.json')
        self._config = {}
        self._ensure_config_dir()
        self._load_config()
    
    def _ensure_config_dir(self):
        """Đảm bảo thư mục config tồn tại"""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
        except Exception as e:
            logging.error(f"Không thể tạo thư mục config: {e}")
    
    def _load_config(self):
        """Tải cấu hình từ file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                logging.info("Đã tải cấu hình thành công")
            else:
                self._config = self._get_default_config()
                self._save_config()
                logging.info("Tạo cấu hình mặc định")
        except Exception as e:
            logging.error(f"Lỗi khi tải cấu hình: {e}")
            self._config = self._get_default_config()
    
    def _save_config(self):
        """Lưu cấu hình vào file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            logging.info("Đã lưu cấu hình thành công")
        except Exception as e:
            logging.error(f"Lỗi khi lưu cấu hình: {e}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Lấy cấu hình mặc định"""
        return {
            "ai": {
                "gemini_api_key": "",
                "model": "gemini-2.0-flash-exp",
                "temperature": 0.3
            },
            "ui": {
                "window_width": 500,
                "window_height": 400,
                "remember_window_size": True,
                "show_advanced_fields": False
            },
            "vocabulary": {
                "auto_save": True,
                "show_pronunciation": True,
                "show_context": True,
                "show_synonyms": True,
                "show_antonyms": True
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Lấy giá trị cấu hình theo key path (VD: 'ai.gemini_api_key')"""
        try:
            keys = key.split('.')
            value = self._config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Thiết lập giá trị cấu hình theo key path"""
        try:
            keys = key.split('.')
            config = self._config
            
            # Navigate to parent
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            # Set final value
            config[keys[-1]] = value
            self._save_config()
            logging.info(f"Đã cập nhật cấu hình: {key} = {value}")
        except Exception as e:
            logging.error(f"Lỗi khi thiết lập cấu hình {key}: {e}")
    
    def get_gemini_api_key(self) -> Optional[str]:
        """Lấy Gemini API key (ưu tiên config file, sau đó environment variable)"""
        # Ưu tiên lấy từ config file
        api_key = self.get('ai.gemini_api_key', '')
        if api_key and api_key.strip():
            return api_key.strip()
        
        # Fallback đến environment variable
        env_key = os.environ.get('GEMINI_API_KEY')
        if env_key and env_key.strip():
            return env_key.strip()
        
        return None
    
    def set_gemini_api_key(self, api_key: str):
        """Thiết lập Gemini API key"""
        self.set('ai.gemini_api_key', api_key.strip() if api_key else '')
    
    def get_ui_setting(self, setting: str, default: Any = None) -> Any:
        """Lấy thiết lập UI"""
        return self.get(f'ui.{setting}', default)
    
    def set_ui_setting(self, setting: str, value: Any):
        """Thiết lập UI"""
        self.set(f'ui.{setting}', value)
    
    def get_vocabulary_setting(self, setting: str, default: Any = None) -> Any:
        """Lấy thiết lập từ vựng"""
        return self.get(f'vocabulary.{setting}', default)
    
    def set_vocabulary_setting(self, setting: str, value: Any):
        """Thiết lập từ vựng"""
        self.set(f'vocabulary.{setting}', value)
    
    def export_config(self) -> str:
        """Export cấu hình thành JSON string"""
        try:
            # Tạo copy và ẩn API key để bảo mật
            export_config = self._config.copy()
            if 'ai' in export_config and 'gemini_api_key' in export_config['ai']:
                if export_config['ai']['gemini_api_key']:
                    export_config['ai']['gemini_api_key'] = '[HIDDEN]'
            
            return json.dumps(export_config, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Lỗi export cấu hình: {e}")
            return "{}"
    
    def import_config(self, config_json: str, include_api_key: bool = False):
        """Import cấu hình từ JSON string"""
        try:
            new_config = json.loads(config_json)
            
            if not include_api_key:
                # Giữ lại API key hiện tại nếu không import
                current_api_key = self.get('ai.gemini_api_key', '')
                if 'ai' not in new_config:
                    new_config['ai'] = {}
                new_config['ai']['gemini_api_key'] = current_api_key
            
            self._config = new_config
            self._save_config()
            logging.info("Import cấu hình thành công")
            return True
        except Exception as e:
            logging.error(f"Lỗi import cấu hình: {e}")
            return False
    
    def reset_to_default(self):
        """Reset về cấu hình mặc định"""
        try:
            self._config = self._get_default_config()
            self._save_config()
            logging.info("Đã reset cấu hình về mặc định")
        except Exception as e:
            logging.error(f"Lỗi reset cấu hình: {e}")

# Global instance
config_manager = ConfigManager() 