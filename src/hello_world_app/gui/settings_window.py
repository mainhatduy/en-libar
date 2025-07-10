"""
Settings Window - Giao diện cấu hình ứng dụng
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject
from typing import Optional

from ..core.config_manager import config_manager
from ..utils.helpers import log_message
from ..utils.ai_helper import ai_helper

class SettingsWindow:
    """Class quản lý cửa sổ cấu hình"""
    
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.window = None
        self.api_key_entry = None
        self.model_combo = None
        self.temperature_spin = None
        self.show_advanced_check = None
        self.show_pronunciation_check = None
        self.show_context_check = None
        self.show_synonyms_check = None
        self.show_antonyms_check = None
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        self.window = Gtk.Window()
        self.window.set_title("⚙️ Cấu hình ứng dụng")
        self.window.set_default_size(600, 500)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_modal(True)
        
        if self.parent_window:
            self.window.set_transient_for(self.parent_window)
        
        # Tạo notebook để phân chia các tab
        notebook = Gtk.Notebook()
        
        # Tab AI Configuration
        ai_tab = self._create_ai_tab()
        notebook.append_page(ai_tab, Gtk.Label("🤖 AI Configuration"))
        
        # Tab UI Settings
        ui_tab = self._create_ui_tab()
        notebook.append_page(ui_tab, Gtk.Label("🖥️ Giao diện"))
        
        # Tab Vocabulary Settings
        vocab_tab = self._create_vocabulary_tab()
        notebook.append_page(vocab_tab, Gtk.Label("📚 Từ vựng"))
        
        # Container chính
        main_vbox = Gtk.VBox(spacing=10)
        main_vbox.set_margin_left(15)
        main_vbox.set_margin_right(15)
        main_vbox.set_margin_top(15)
        main_vbox.set_margin_bottom(15)
        
        main_vbox.pack_start(notebook, True, True, 0)
        
        # Buttons
        button_box = self._create_button_box()
        main_vbox.pack_start(button_box, False, False, 0)
        
        self.window.add(main_vbox)
        
        # Kết nối signal handlers
        self.window.connect("delete-event", self._on_window_delete)
        self.window.connect("key-press-event", self._on_key_press)
    
    def _create_ai_tab(self) -> Gtk.Widget:
        """Tạo tab cấu hình AI"""
        vbox = Gtk.VBox(spacing=15)
        vbox.set_margin_left(20)
        vbox.set_margin_right(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        
        # API Key section
        api_frame = Gtk.Frame(label="🔑 Gemini API Key")
        api_vbox = Gtk.VBox(spacing=10)
        api_vbox.set_margin_left(15)
        api_vbox.set_margin_right(15)
        api_vbox.set_margin_top(15)
        api_vbox.set_margin_bottom(15)
        
        # API Key input
        api_label = Gtk.Label("API Key:")
        api_label.set_halign(Gtk.Align.START)
        api_vbox.pack_start(api_label, False, False, 0)
        
        api_hbox = Gtk.HBox(spacing=10)
        
        self.api_key_entry = Gtk.Entry()
        self.api_key_entry.set_placeholder_text("Nhập Gemini API key của bạn...")
        self.api_key_entry.set_visibility(False)  # Hidden by default
        self.api_key_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "view-reveal-symbolic")
        self.api_key_entry.connect("icon-press", self._on_toggle_api_key_visibility)
        api_hbox.pack_start(self.api_key_entry, True, True, 0)
        
        test_button = Gtk.Button(label="🧪 Test")
        test_button.connect("clicked", self._on_test_api_key)
        api_hbox.pack_start(test_button, False, False, 0)
        
        api_vbox.pack_start(api_hbox, False, False, 0)
        
        # Instructions
        info_label = Gtk.Label()
        info_label.set_markup('<span size="small" color="gray">💡 Lấy API key miễn phí tại: <a href="https://makersuite.google.com/app/apikey">Google AI Studio</a></span>')
        info_label.set_halign(Gtk.Align.START)
        api_vbox.pack_start(info_label, False, False, 0)
        
        api_frame.add(api_vbox)
        vbox.pack_start(api_frame, False, False, 0)
        
        # AI Model settings
        model_frame = Gtk.Frame(label="🤖 Cấu hình Model")
        model_vbox = Gtk.VBox(spacing=10)
        model_vbox.set_margin_left(15)
        model_vbox.set_margin_right(15)
        model_vbox.set_margin_top(15)
        model_vbox.set_margin_bottom(15)
        
        # Model selection
        model_label = Gtk.Label("Model:")
        model_label.set_halign(Gtk.Align.START)
        model_vbox.pack_start(model_label, False, False, 0)
        
        self.model_combo = Gtk.ComboBoxText()
        models = [
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        ]
        for model in models:
            self.model_combo.append_text(model)
        self.model_combo.set_active(0)
        model_vbox.pack_start(self.model_combo, False, False, 0)
        
        # Temperature
        temp_label = Gtk.Label("Temperature (độ sáng tạo):")
        temp_label.set_halign(Gtk.Align.START)
        model_vbox.pack_start(temp_label, False, False, 0)
        
        temp_hbox = Gtk.HBox(spacing=10)
        self.temperature_spin = Gtk.SpinButton()
        self.temperature_spin.set_range(0.0, 1.0)
        self.temperature_spin.set_increments(0.1, 0.1)
        self.temperature_spin.set_digits(1)
        self.temperature_spin.set_value(0.3)
        temp_hbox.pack_start(self.temperature_spin, False, False, 0)
        
        temp_info = Gtk.Label()
        temp_info.set_markup('<span size="small" color="gray">0.0 = conservative, 1.0 = creative</span>')
        temp_hbox.pack_start(temp_info, False, False, 0)
        
        model_vbox.pack_start(temp_hbox, False, False, 0)
        
        model_frame.add(model_vbox)
        vbox.pack_start(model_frame, False, False, 0)
        
        return vbox
    
    def _create_ui_tab(self) -> Gtk.Widget:
        """Tạo tab cấu hình giao diện"""
        vbox = Gtk.VBox(spacing=15)
        vbox.set_margin_left(20)
        vbox.set_margin_right(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        
        # Quick add settings
        quick_frame = Gtk.Frame(label="⚡ Chế độ thêm nhanh")
        quick_vbox = Gtk.VBox(spacing=10)
        quick_vbox.set_margin_left(15)
        quick_vbox.set_margin_right(15)
        quick_vbox.set_margin_top(15)
        quick_vbox.set_margin_bottom(15)
        
        self.show_advanced_check = Gtk.CheckButton(label="Hiển thị các trường nâng cao trong chế độ thêm nhanh")
        quick_vbox.pack_start(self.show_advanced_check, False, False, 0)
        
        quick_frame.add(quick_vbox)
        vbox.pack_start(quick_frame, False, False, 0)
        
        return vbox
    
    def _create_vocabulary_tab(self) -> Gtk.Widget:
        """Tạo tab cấu hình từ vựng"""
        vbox = Gtk.VBox(spacing=15)
        vbox.set_margin_left(20)
        vbox.set_margin_right(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        
        # Display settings
        display_frame = Gtk.Frame(label="📋 Hiển thị thông tin")
        display_vbox = Gtk.VBox(spacing=10)
        display_vbox.set_margin_left(15)
        display_vbox.set_margin_right(15)
        display_vbox.set_margin_top(15)
        display_vbox.set_margin_bottom(15)
        
        self.show_pronunciation_check = Gtk.CheckButton(label="Hiển thị phát âm")
        display_vbox.pack_start(self.show_pronunciation_check, False, False, 0)
        
        self.show_context_check = Gtk.CheckButton(label="Hiển thị ngữ cảnh sử dụng")
        display_vbox.pack_start(self.show_context_check, False, False, 0)
        
        self.show_synonyms_check = Gtk.CheckButton(label="Hiển thị từ đồng nghĩa")
        display_vbox.pack_start(self.show_synonyms_check, False, False, 0)
        
        self.show_antonyms_check = Gtk.CheckButton(label="Hiển thị từ trái nghĩa")
        display_vbox.pack_start(self.show_antonyms_check, False, False, 0)
        
        display_frame.add(display_vbox)
        vbox.pack_start(display_frame, False, False, 0)
        
        return vbox
    
    def _create_button_box(self) -> Gtk.Widget:
        """Tạo box chứa các nút"""
        hbox = Gtk.HBox(spacing=10)
        
        # Import/Export buttons
        import_button = Gtk.Button(label="📥 Import")
        import_button.connect("clicked", self._on_import_config)
        hbox.pack_start(import_button, False, False, 0)
        
        export_button = Gtk.Button(label="📤 Export")
        export_button.connect("clicked", self._on_export_config)
        hbox.pack_start(export_button, False, False, 0)
        
        # Spacer
        hbox.pack_start(Gtk.Label(), True, True, 0)
        
        # Reset button
        reset_button = Gtk.Button(label="🔄 Reset")
        reset_button.connect("clicked", self._on_reset_config)
        hbox.pack_start(reset_button, False, False, 0)
        
        # Apply & Close buttons
        apply_button = Gtk.Button(label="✅ Áp dụng")
        apply_button.connect("clicked", self._on_apply_settings)
        apply_button.get_style_context().add_class("suggested-action")
        hbox.pack_start(apply_button, False, False, 0)
        
        close_button = Gtk.Button(label="❌ Đóng")
        close_button.connect("clicked", self._on_close)
        hbox.pack_start(close_button, False, False, 0)
        
        return hbox
    
    def load_settings(self):
        """Tải cấu hình hiện tại vào giao diện"""
        # AI settings
        api_key = config_manager.get('ai.gemini_api_key', '')
        if api_key:
            self.api_key_entry.set_text(api_key)
        
        model = config_manager.get('ai.model', 'gemini-2.0-flash-exp')
        combo_model = self.model_combo.get_model()
        for i, row in enumerate(combo_model):
            if row[0] == model:
                self.model_combo.set_active(i)
                break
        
        temperature = config_manager.get('ai.temperature', 0.3)
        self.temperature_spin.set_value(temperature)
        
        # UI settings
        show_advanced = config_manager.get_ui_setting('show_advanced_fields', False)
        self.show_advanced_check.set_active(show_advanced)
        
        # Vocabulary settings
        self.show_pronunciation_check.set_active(config_manager.get_vocabulary_setting('show_pronunciation', True))
        self.show_context_check.set_active(config_manager.get_vocabulary_setting('show_context', True))
        self.show_synonyms_check.set_active(config_manager.get_vocabulary_setting('show_synonyms', True))
        self.show_antonyms_check.set_active(config_manager.get_vocabulary_setting('show_antonyms', True))
    
    def _on_toggle_api_key_visibility(self, entry, icon_pos, event):
        """Toggle hiển thị/ẩn API key"""
        current_visibility = entry.get_visibility()
        entry.set_visibility(not current_visibility)
        
        if current_visibility:
            entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "view-reveal-symbolic")
        else:
            entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "view-conceal-symbolic")
    
    def _on_test_api_key(self, widget):
        """Test API key"""
        api_key = self.api_key_entry.get_text().strip()
        if not api_key:
            self._show_message("Vui lòng nhập API key trước!", "error")
            return
        
        # Lưu tạm và test
        old_key = config_manager.get('ai.gemini_api_key', '')
        config_manager.set_gemini_api_key(api_key)
        
        widget.set_sensitive(False)
        widget.set_label("⏳ Đang test...")
        
        def test_in_background():
            try:
                # Reinitialize AI helper với key mới
                success = ai_helper.reinitialize()
                
                if success:
                    # Test thực tế bằng cách gọi API
                    result = ai_helper.generate_definition("test")
                    
                    GObject.idle_add(self._on_test_complete, widget, True, "API key hợp lệ!")
                else:
                    GObject.idle_add(self._on_test_complete, widget, False, "API key không hợp lệ")
                    
            except Exception as e:
                GObject.idle_add(self._on_test_complete, widget, False, f"Lỗi: {str(e)}")
        
        import threading
        thread = threading.Thread(target=test_in_background)
        thread.daemon = True
        thread.start()
    
    def _on_test_complete(self, widget, success, message):
        """Xử lý kết quả test API key"""
        widget.set_sensitive(True)
        widget.set_label("🧪 Test")
        
        if success:
            self._show_message(message, "success")
        else:
            self._show_message(message, "error")
        
        return False
    
    def _on_apply_settings(self, widget):
        """Áp dụng cấu hình"""
        try:
            # Lưu AI settings
            api_key = self.api_key_entry.get_text().strip()
            config_manager.set_gemini_api_key(api_key)
            
            model = self.model_combo.get_active_text()
            if model:
                config_manager.set('ai.model', model)
            
            temperature = self.temperature_spin.get_value()
            config_manager.set('ai.temperature', temperature)
            
            # Lưu UI settings
            show_advanced = self.show_advanced_check.get_active()
            config_manager.set_ui_setting('show_advanced_fields', show_advanced)
            
            # Lưu vocabulary settings
            config_manager.set_vocabulary_setting('show_pronunciation', self.show_pronunciation_check.get_active())
            config_manager.set_vocabulary_setting('show_context', self.show_context_check.get_active())
            config_manager.set_vocabulary_setting('show_synonyms', self.show_synonyms_check.get_active())
            config_manager.set_vocabulary_setting('show_antonyms', self.show_antonyms_check.get_active())
            
            # Reinitialize AI helper
            ai_helper.reinitialize()
            
            self._show_message("Đã lưu cấu hình thành công!", "success")
            log_message("Settings saved successfully")
            
        except Exception as e:
            self._show_message(f"Lỗi khi lưu cấu hình: {e}", "error")
            log_message(f"Error saving settings: {e}", "ERROR")
    
    def _on_export_config(self, widget):
        """Export cấu hình"""
        dialog = Gtk.FileChooserDialog(
            title="Export cấu hình",
            parent=self.window,
            action=Gtk.FileChooserAction.SAVE
        )
        
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE, Gtk.ResponseType.OK
        )
        
        dialog.set_current_name("vocabulary_app_config.json")
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            try:
                config_json = config_manager.export_config()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(config_json)
                self._show_message(f"Đã export cấu hình tới {filename}", "success")
            except Exception as e:
                self._show_message(f"Lỗi export: {e}", "error")
        
        dialog.destroy()
    
    def _on_import_config(self, widget):
        """Import cấu hình"""
        dialog = Gtk.FileChooserDialog(
            title="Import cấu hình",
            parent=self.window,
            action=Gtk.FileChooserAction.OPEN
        )
        
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        # Add file filter
        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON files")
        filter_json.add_pattern("*.json")
        dialog.add_filter(filter_json)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    config_json = f.read()
                
                if config_manager.import_config(config_json):
                    self.load_settings()  # Reload UI
                    self._show_message(f"Đã import cấu hình từ {filename}", "success")
                else:
                    self._show_message("Lỗi import cấu hình", "error")
                    
            except Exception as e:
                self._show_message(f"Lỗi đọc file: {e}", "error")
        
        dialog.destroy()
    
    def _on_reset_config(self, widget):
        """Reset cấu hình về mặc định"""
        dialog = Gtk.MessageDialog(
            parent=self.window,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Bạn có chắc muốn reset tất cả cấu hình về mặc định?"
        )
        
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            config_manager.reset_to_default()
            self.load_settings()
            self._show_message("Đã reset cấu hình về mặc định", "success")
        
        dialog.destroy()
    
    def _on_close(self, widget):
        """Đóng cửa sổ"""
        self.window.destroy()
    
    def _on_window_delete(self, widget, event):
        """Xử lý khi đóng cửa sổ"""
        return False
    
    def _on_key_press(self, widget, event):
        """Xử lý phím tắt"""
        # Escape để đóng
        if event.keyval == Gdk.KEY_Escape:
            self._on_close(None)
            return True
        
        # Ctrl+S để apply
        if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_s:
            self._on_apply_settings(None)
            return True
        
        return False
    
    def _show_message(self, message, message_type="info"):
        """Hiển thị thông báo"""
        if message_type == "error":
            msg_type = Gtk.MessageType.ERROR
        elif message_type == "success":
            msg_type = Gtk.MessageType.INFO
        else:
            msg_type = Gtk.MessageType.INFO
        
        dialog = Gtk.MessageDialog(
            parent=self.window,
            flags=Gtk.DialogFlags.MODAL,
            message_type=msg_type,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        
        dialog.run()
        dialog.destroy()
    
    def show(self):
        """Hiển thị cửa sổ"""
        if self.window:
            self.window.show_all()
            self.window.present()
            log_message("Hiển thị cửa sổ Settings")
    
    def destroy(self):
        """Hủy cửa sổ"""
        if self.window:
            self.window.destroy() 