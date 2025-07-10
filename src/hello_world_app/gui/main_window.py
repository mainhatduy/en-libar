"""
Main window GUI cho Hello World App
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

from ..core.config import AppConfig
from ..core.vocabulary_manager import VocabularyManager
from ..utils.helpers import format_system_info, log_message
from .vocabulary_window import VocabularyWindow

class MainWindow:
    """Quản lý cửa sổ chính của ứng dụng"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.window = None
        self.vocabulary_window = None
        self.vocab_manager = VocabularyManager()
        
        # Vocabulary form widgets
        self.word_entry = None
        self.definition_entry = None
        self.quick_add_status_label = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        self.window = Gtk.Window()
        self.window.set_title(AppConfig.WINDOW_TITLE)
        self.window.set_default_size(
            AppConfig.WINDOW_DEFAULT_WIDTH, 
            AppConfig.WINDOW_DEFAULT_HEIGHT
        )
        self.window.set_position(Gtk.WindowPosition.CENTER)
        
        # Tạo layout chính
        vbox = self._create_main_layout()
        self.window.add(vbox)
        
        # Kết nối signal handlers
        self.window.connect("delete-event", self._on_window_delete)
        self.window.connect("key-press-event", self._on_key_press)
    
    def _create_main_layout(self) -> Gtk.VBox:
        """Tạo layout chính của cửa sổ"""
        vbox = Gtk.VBox(spacing=15)
        vbox.set_margin_left(20)
        vbox.set_margin_right(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        
        # Thêm các widget
        vbox.pack_start(self._create_hello_label(), False, False, 0)
        vbox.pack_start(self._create_info_label(), False, False, 0)
        
        # Thêm phần form từ vựng nhanh
        vbox.pack_start(self._create_vocabulary_quick_add_section(), False, False, 0)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(separator, False, False, 10)
        
        vbox.pack_start(self._create_vocabulary_button(), False, False, 0)
        vbox.pack_start(self._create_hotkey_info_label(), False, False, 0)
        vbox.pack_start(self._create_hide_button(), False, False, 0)
        vbox.pack_start(self._create_quit_button(), False, False, 0)
        
        return vbox
    
    def _create_vocabulary_quick_add_section(self) -> Gtk.VBox:
        """Tạo phần thêm từ vựng nhanh"""
        section_vbox = Gtk.VBox(spacing=10)
        
        # Tiêu đề
        title_label = Gtk.Label()
        title_label.set_markup('<span size="large" weight="bold">📝 Thêm từ vựng nhanh</span>')
        title_label.set_halign(Gtk.Align.START)
        section_vbox.pack_start(title_label, False, False, 0)
        
        # Form container
        form_frame = Gtk.Frame()
        form_frame.set_shadow_type(Gtk.ShadowType.IN)
        
        form_vbox = Gtk.VBox(spacing=10)
        form_vbox.set_margin_left(15)
        form_vbox.set_margin_right(15)
        form_vbox.set_margin_top(15)
        form_vbox.set_margin_bottom(15)
        
        # Word entry
        word_hbox = Gtk.HBox(spacing=10)
        word_label = Gtk.Label("Từ vựng:")
        word_label.set_size_request(80, -1)
        word_label.set_halign(Gtk.Align.START)
        self.word_entry = Gtk.Entry()
        self.word_entry.set_placeholder_text("Nhập từ vựng...")
        self.word_entry.connect("activate", self._on_quick_add_word)
        word_hbox.pack_start(word_label, False, False, 0)
        word_hbox.pack_start(self.word_entry, True, True, 0)
        form_vbox.pack_start(word_hbox, False, False, 0)
        
        # Definition entry
        def_hbox = Gtk.HBox(spacing=10)
        def_label = Gtk.Label("Nghĩa:")
        def_label.set_size_request(80, -1)
        def_label.set_halign(Gtk.Align.START)
        self.definition_entry = Gtk.Entry()
        self.definition_entry.set_placeholder_text("Nhập nghĩa của từ...")
        self.definition_entry.connect("activate", self._on_quick_add_word)
        def_hbox.pack_start(def_label, False, False, 0)
        def_hbox.pack_start(self.definition_entry, True, True, 0)
        form_vbox.pack_start(def_hbox, False, False, 0)
        
        # Button and status
        button_hbox = Gtk.HBox(spacing=10)
        
        add_button = Gtk.Button(label="➕ Thêm từ vựng")
        add_button.connect("clicked", self._on_quick_add_word)
        add_button.get_style_context().add_class("suggested-action")
        button_hbox.pack_start(add_button, False, False, 0)
        
        clear_button = Gtk.Button(label="🗑️ Xóa")
        clear_button.connect("clicked", self._on_clear_quick_form)
        button_hbox.pack_start(clear_button, False, False, 0)
        
        form_vbox.pack_start(button_hbox, False, False, 0)
        
        # Status label
        self.quick_add_status_label = Gtk.Label()
        self.quick_add_status_label.set_halign(Gtk.Align.START)
        form_vbox.pack_start(self.quick_add_status_label, False, False, 0)
        
        form_frame.add(form_vbox)
        section_vbox.pack_start(form_frame, False, False, 0)
        
        # Instructions
        instruction_label = Gtk.Label()
        instruction_label.set_markup('<span size="small" style="italic" color="gray">💡 Mẹo: Nhấn Enter để thêm nhanh, hoặc Ctrl+M để mở quản lý từ vựng đầy đủ</span>')
        instruction_label.set_halign(Gtk.Align.START)
        section_vbox.pack_start(instruction_label, False, False, 0)
        
        return section_vbox
    
    def _create_hello_label(self) -> Gtk.Label:
        """Tạo label chào mừng chính"""
        label = Gtk.Label()
        label.set_markup('<span size="xx-large" weight="bold">Hello World!</span>')
        label.set_halign(Gtk.Align.CENTER)
        return label
    
    def _create_info_label(self) -> Gtk.Label:
        """Tạo label thông tin hệ thống"""
        label = Gtk.Label()
        label.set_markup(format_system_info())
        label.set_halign(Gtk.Align.CENTER)
        return label
    
    def _create_hotkey_info_label(self) -> Gtk.Label:
        """Tạo label thông tin về hotkey"""
        label = Gtk.Label()
        label.set_markup('<span style="italic" color="blue">💡 Sử dụng Super+T để hiển thị cửa sổ từ bất kỳ đâu</span>')
        label.set_halign(Gtk.Align.CENTER)
        return label
    
    def _create_hide_button(self) -> Gtk.Button:
        """Tạo nút ẩn xuống system tray"""
        button = Gtk.Button(label="Ẩn xuống System Tray")
        button.connect("clicked", self._on_hide_clicked)
        return button
    
    def _create_vocabulary_button(self) -> Gtk.Button:
        """Tạo nút mở cửa sổ từ vựng"""
        button = Gtk.Button(label="📚 Quản lý Từ vựng đầy đủ")
        button.connect("clicked", self._on_vocabulary_clicked)
        button.get_style_context().add_class("suggested-action")
        return button
    
    def _create_quit_button(self) -> Gtk.Button:
        """Tạo nút thoát ứng dụng"""
        button = Gtk.Button(label="Thoát ứng dụng")
        button.connect("clicked", self._on_quit_clicked)
        return button
    
    def _on_quick_add_word(self, widget):
        """Xử lý thêm từ vựng nhanh"""
        if not self.word_entry or not self.definition_entry:
            return
            
        word = self.word_entry.get_text().strip()
        definition = self.definition_entry.get_text().strip()
        
        if not word or not definition:
            self._update_status("❌ Vui lòng nhập cả từ vựng và nghĩa!", "error")
            return
        
        # Thêm từ vựng vào database
        success = self.vocab_manager.add_vocabulary(word, definition)
        
        if success:
            self._update_status(f"✅ Đã thêm từ '{word}' thành công!", "success")
            # Clear form sau khi thêm thành công
            self._clear_quick_form()
            # Focus vào word entry để tiếp tục thêm
            if self.word_entry:
                self.word_entry.grab_focus()
            log_message(f"Thêm từ vựng nhanh: {word}")
        else:
            self._update_status(f"❌ Từ '{word}' đã tồn tại hoặc có lỗi!", "error")
    
    def _on_clear_quick_form(self, widget):
        """Xóa form thêm nhanh"""
        self._clear_quick_form()
    
    def _clear_quick_form(self):
        """Xóa nội dung form thêm nhanh"""
        if self.word_entry:
            self.word_entry.set_text("")
        if self.definition_entry:
            self.definition_entry.set_text("")
        self._update_status("", "")
        if self.word_entry:
            self.word_entry.grab_focus()
    
    def _update_status(self, message: str, status_type: str = ""):
        """Cập nhật thông báo trạng thái"""
        if not self.quick_add_status_label:
            return
            
        if status_type == "success":
            markup = f'<span color="green">{message}</span>'
        elif status_type == "error":
            markup = f'<span color="red">{message}</span>'
        else:
            markup = message
        
        self.quick_add_status_label.set_markup(markup)
        
        # Tự động xóa thông báo sau 3 giây
        if message:
            GLib.timeout_add_seconds(3, lambda: self._update_status("", ""))
    
    def _on_hide_clicked(self, widget):
        """Xử lý khi click nút ẩn"""
        self.hide()
    
    def _on_vocabulary_clicked(self, widget):
        """Xử lý khi click nút từ vựng"""
        if self.vocabulary_window is None:
            self.vocabulary_window = VocabularyWindow(self.window)
        
        self.vocabulary_window.show()
        log_message("Mở cửa sổ quản lý từ vựng")
    
    def _on_quit_clicked(self, widget):
        """Xử lý khi click nút thoát"""
        self.app.quit()
    
    def _on_window_delete(self, widget, event):
        """Xử lý khi đóng cửa sổ"""
        self.hide()
        return True  # Ngăn destroy window
    
    def _on_key_press(self, widget, event):
        """Xử lý phím tắt"""
        # Ctrl+M để mở quản lý từ vựng đầy đủ
        if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_m:
            self._on_vocabulary_clicked(None)
            return True
        
        # Ctrl+Q để thoát
        if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_q:
            self._on_quit_clicked(None)
            return True
        
        # Escape để xóa form
        if event.keyval == Gdk.KEY_Escape:
            self._clear_quick_form()
            return True
        
        return False
    
    def show(self):
        """Hiển thị cửa sổ"""
        if self.window:
            # Đảm bảo cửa sổ hiển thị
            self.window.show_all()
            
            # Đặt cửa sổ lên trên tất cả các cửa sổ khác
            self.window.set_keep_above(True)
            
            # Present để focus và đưa cửa sổ lên đầu
            self.window.present()
            
            # Đảm bảo cửa sổ có thể nhận input
            self.window.set_can_focus(True)
            
            # Grab focus cho cửa sổ
            self.window.grab_focus()
            
            # Unmap và map lại để force refresh (workaround cho một số DE)
            if not self.window.get_visible():
                self.window.deiconify()
            
            # Tắt keep_above sau một chút để không ảnh hưởng UX
            GLib.timeout_add_seconds(1, lambda: self._disable_keep_above())
            
            # Focus vào word entry để sẵn sàng nhập từ vựng
            if self.word_entry:
                GLib.timeout_add(100, self._delayed_focus_word_entry)
            
            log_message("Hiển thị cửa sổ chính")
    
    def _disable_keep_above(self):
        """Tắt keep_above sau khi cửa sổ đã hiển thị"""
        if self.window:
            self.window.set_keep_above(False)
        return False  # Chỉ chạy một lần
    
    def _delayed_focus_word_entry(self):
        """Focus vào word entry sau một delay ngắn"""
        if self.word_entry:
            self.word_entry.grab_focus()
        return False  # Chỉ chạy một lần
    
    def hide(self):
        """Ẩn cửa sổ"""
        if self.window:
            self.window.hide()
            log_message("Ẩn cửa sổ xuống system tray")
    
    def destroy(self):
        """Hủy cửa sổ"""
        # Đóng vocabulary window nếu đang mở
        if self.vocabulary_window:
            self.vocabulary_window.destroy()
        
        if self.window:
            self.window.destroy()
            log_message("Đóng cửa sổ chính") 