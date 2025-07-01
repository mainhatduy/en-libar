"""
Test cases cho main module của Hello World App
"""

import pytest
import sys
from unittest.mock import Mock, patch

# Add src to path for testing
sys.path.insert(0, 'src')

from hello_world_app.core.app import HelloWorldApp
from hello_world_app.core.config import AppConfig


class TestAppConfig:
    """Test cases cho AppConfig"""
    
    def test_app_constants(self):
        """Test các hằng số của ứng dụng"""
        assert AppConfig.APP_NAME == "Hello World App"
        assert AppConfig.APP_ID == "hello-world-app"
        assert AppConfig.APP_VERSION == "1.0.0"
        assert AppConfig.WINDOW_DEFAULT_WIDTH == 400
        assert AppConfig.WINDOW_DEFAULT_HEIGHT == 300


class TestHelloWorldApp:
    """Test cases cho HelloWorldApp"""
    
    @patch('hello_world_app.core.app.MainWindow')
    @patch('hello_world_app.core.app.SystemTray')
    def test_app_initialization(self, mock_tray, mock_window):
        """Test khởi tạo ứng dụng"""
        app = HelloWorldApp()
        
        # Kiểm tra các thành phần đã được khởi tạo
        assert app.main_window is not None
        assert app.system_tray is not None
        
        # Kiểm tra các constructor được gọi
        mock_window.assert_called_once_with(app)
        mock_tray.assert_called_once_with(app)
    
    @patch('hello_world_app.core.app.MainWindow')
    @patch('hello_world_app.core.app.SystemTray')
    def test_show_window(self, mock_tray, mock_window):
        """Test hiển thị cửa sổ"""
        app = HelloWorldApp()
        mock_window_instance = Mock()
        app.main_window = mock_window_instance
        
        app.show_window()
        mock_window_instance.show.assert_called_once()
    
    @patch('hello_world_app.core.app.MainWindow')
    @patch('hello_world_app.core.app.SystemTray')
    def test_hide_window(self, mock_tray, mock_window):
        """Test ẩn cửa sổ"""
        app = HelloWorldApp()
        mock_window_instance = Mock()
        app.main_window = mock_window_instance
        
        app.hide_window()
        mock_window_instance.hide.assert_called_once()


@pytest.mark.integration
class TestAppIntegration:
    """Integration tests cho ứng dụng"""
    
    @patch('gi.repository.Gtk.main')
    @patch('hello_world_app.core.app.MainWindow')
    @patch('hello_world_app.core.app.SystemTray')
    def test_app_run_lifecycle(self, mock_tray, mock_window, mock_gtk_main):
        """Test vòng đời chạy ứng dụng"""
        app = HelloWorldApp()
        mock_window_instance = Mock()
        app.main_window = mock_window_instance
        
        app.run()
        
        # Kiểm tra show window được gọi
        mock_window_instance.show.assert_called_once()
        
        # Kiểm tra GTK main loop được gọi
        mock_gtk_main.assert_called_once() 