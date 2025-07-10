"""
Main window GUI cho Hello World App
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
from typing import Optional, Dict
import threading

from ..core.config import AppConfig
from ..core.vocabulary_manager import VocabularyManager
from ..gui.settings_window import SettingsWindow
from ..utils.helpers import format_system_info, log_message
from ..utils.ai_helper import ai_helper
from ..core.config_manager import config_manager

class MainWindow:
    """Quản lý cửa sổ chính của ứng dụng"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.window = None
        self.vocab_manager = VocabularyManager()
        
        # Stack và switcher để chuyển đổi chế độ
        self.stack = None
        self.mode_switcher = None
        self.current_mode = "quick"  # "quick" hoặc "full"
        
        # Quick add widgets
        self.word_entry = None
        self.definition_entry = None
        self.quick_add_status_label = None
        self.ai_button = None
        self.ai_status_label = None
        
        # Quick add advanced widgets (when enabled)
        self.quick_pronunciation_entry = None
        self.quick_part_of_speech_combo = None
        self.quick_example_textview = None
        self.quick_context_sentences_textview = None
        self.quick_synonyms_entry = None
        self.quick_antonyms_entry = None
        
        # Full management widgets
        self.vocabulary_list = None
        self.search_entry = None
        self.full_word_entry = None
        self.definition_textview = None
        self.example_textview = None
        self.pronunciation_entry = None
        self.part_of_speech_combo = None
        self.context_sentences_textview = None
        self.synonyms_entry = None
        self.antonyms_entry = None
        self.current_editing_id = None
        self.save_button = None
        self.cancel_button = None
        self.stats_content = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        self.window = Gtk.Window()
        self.window.set_title(AppConfig.WINDOW_TITLE)
        self.window.set_default_size(900, 600)  # Larger default size
        self.window.set_position(Gtk.WindowPosition.CENTER)
        
        # Tạo header bar
        self._create_header()
        
        # Tạo layout chính với stack
        vbox = self._create_main_layout()
        self.window.add(vbox)
        
        # Kết nối signal handlers
        self.window.connect("delete-event", self._on_window_delete)
        self.window.connect("key-press-event", self._on_key_press)
    
    def _create_main_layout(self) -> Gtk.VBox:
        """Tạo layout chính của cửa sổ"""
        vbox = Gtk.VBox(spacing=0)
        
        # Stack chứa 2 chế độ
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)
        
        # Thêm trang "Thêm nhanh"
        quick_page = self._create_quick_add_page()
        self.stack.add_titled(quick_page, "quick", "Thêm nhanh")
        
        # Thêm trang "Quản lý đầy đủ"
        full_page = self._create_full_management_page()
        self.stack.add_titled(full_page, "full", "Quản lý đầy đủ")
        
        vbox.pack_start(self.stack, True, True, 0)
        
        return vbox
    
    def _create_header(self):
        """Tạo header bar với nút chuyển đổi chế độ"""
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.set_title("Hello World - Ứng dụng từ vựng")
        
        # Nút chuyển đổi chế độ
        mode_button = Gtk.Button()
        mode_button.set_label("📚 Chế độ quản lý")
        mode_button.connect("clicked", self._on_mode_switch_clicked)
        header.pack_start(mode_button)
        self.mode_button = mode_button
        
        # Nút Settings
        settings_button = Gtk.Button()
        settings_button.set_label("⚙️ Cấu hình")
        settings_button.connect("clicked", self._on_settings_clicked)
        header.pack_end(settings_button)
        
        if self.window:
            self.window.set_titlebar(header)
    
    def _create_quick_add_page(self) -> Gtk.VBox:
        """Tạo trang thêm từ vựng nhanh"""
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
        
        vbox.pack_start(self._create_hotkey_info_label(), False, False, 0)
        
        return vbox
    
    def _create_full_management_page(self) -> Gtk.Paned:
        """Tạo trang quản lý từ vựng đầy đủ"""
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        
        # Phần trái: Form nhập liệu
        left_panel = self._create_full_input_panel()
        paned.pack1(left_panel, False, False)
        
        # Phần phải: Danh sách từ vựng
        right_panel = self._create_list_panel()
        paned.pack2(right_panel, True, False)
        
        paned.set_position(400)
        
        # Load dữ liệu khi trang được tạo
        GLib.idle_add(self.refresh_vocabulary_list)
        
        return paned
    
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
    
    def _create_vocabulary_quick_add_section(self) -> Gtk.VBox:
        """Tạo phần thêm từ vựng nhanh"""
        section_vbox = Gtk.VBox(spacing=10)
        
        # Tiêu đề
        title_hbox = Gtk.HBox(spacing=10)
        title_label = Gtk.Label()
        title_label.set_markup('<span size="large" weight="bold">📝 Thêm từ vựng nhanh</span>')
        title_label.set_halign(Gtk.Align.START)
        title_hbox.pack_start(title_label, False, False, 0)
        
        # Nút toggle advanced fields
        show_advanced = config_manager.get_ui_setting('show_advanced_fields', False)
        toggle_button = Gtk.ToggleButton(label="📋 Trường nâng cao")
        toggle_button.set_active(show_advanced)
        toggle_button.connect("toggled", self._on_toggle_advanced_fields)
        title_hbox.pack_end(toggle_button, False, False, 0)
        
        section_vbox.pack_start(title_hbox, False, False, 0)
        
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
        word_label.set_size_request(120, -1)
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
        def_label.set_size_request(120, -1)
        def_label.set_halign(Gtk.Align.START)
        self.definition_entry = Gtk.Entry()
        self.definition_entry.set_placeholder_text("Nhập nghĩa của từ...")
        self.definition_entry.connect("activate", self._on_quick_add_word)
        def_hbox.pack_start(def_label, False, False, 0)
        def_hbox.pack_start(self.definition_entry, True, True, 0)
        form_vbox.pack_start(def_hbox, False, False, 0)
        
        # Advanced fields section
        self.advanced_fields_box = Gtk.VBox(spacing=10)
        
        # Pronunciation
        pron_hbox = Gtk.HBox(spacing=10)
        pron_label = Gtk.Label("Phát âm:")
        pron_label.set_size_request(120, -1)
        pron_label.set_halign(Gtk.Align.START)
        self.quick_pronunciation_entry = Gtk.Entry()
        self.quick_pronunciation_entry.set_placeholder_text("/ˈeksæmpəl/...")
        self.quick_pronunciation_entry.connect("activate", self._on_quick_add_word)
        pron_hbox.pack_start(pron_label, False, False, 0)
        pron_hbox.pack_start(self.quick_pronunciation_entry, True, True, 0)
        self.advanced_fields_box.pack_start(pron_hbox, False, False, 0)
        
        # Part of speech
        pos_hbox = Gtk.HBox(spacing=10)
        pos_label = Gtk.Label("Loại từ:")
        pos_label.set_size_request(120, -1)
        pos_label.set_halign(Gtk.Align.START)
        self.quick_part_of_speech_combo = Gtk.ComboBoxText()
        parts_of_speech = [
            "", "Noun (Danh từ)", "Verb (Động từ)", "Adjective (Tính từ)",
            "Adverb (Trạng từ)", "Preposition (Giới từ)", "Conjunction (Liên từ)",
            "Pronoun (Đại từ)", "Interjection (Thán từ)"
        ]
        for part in parts_of_speech:
            self.quick_part_of_speech_combo.append_text(part)
        self.quick_part_of_speech_combo.set_active(0)
        pos_hbox.pack_start(pos_label, False, False, 0)
        pos_hbox.pack_start(self.quick_part_of_speech_combo, True, True, 0)
        self.advanced_fields_box.pack_start(pos_hbox, False, False, 0)
        
        # Example sentences
        ex_label = Gtk.Label("Ví dụ:")
        ex_label.set_halign(Gtk.Align.START)
        self.quick_example_textview = Gtk.TextView()
        self.quick_example_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.quick_example_textview.set_editable(True)
        self.quick_example_textview.set_cursor_visible(True)
        ex_scrolled = Gtk.ScrolledWindow()
        ex_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        ex_scrolled.set_min_content_height(60)
        ex_scrolled.add(self.quick_example_textview)
        self.advanced_fields_box.pack_start(ex_label, False, False, 0)
        self.advanced_fields_box.pack_start(ex_scrolled, False, False, 0)
        
        # Context sentences
        ctx_label = Gtk.Label("Ngữ cảnh sử dụng:")
        ctx_label.set_halign(Gtk.Align.START)
        self.quick_context_sentences_textview = Gtk.TextView()
        self.quick_context_sentences_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.quick_context_sentences_textview.set_editable(True)
        self.quick_context_sentences_textview.set_cursor_visible(True)
        ctx_scrolled = Gtk.ScrolledWindow()
        ctx_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        ctx_scrolled.set_min_content_height(60)
        ctx_scrolled.add(self.quick_context_sentences_textview)
        self.advanced_fields_box.pack_start(ctx_label, False, False, 0)
        self.advanced_fields_box.pack_start(ctx_scrolled, False, False, 0)
        
        # Synonyms
        syn_hbox = Gtk.HBox(spacing=10)
        syn_label = Gtk.Label("Từ đồng nghĩa:")
        syn_label.set_size_request(120, -1)
        syn_label.set_halign(Gtk.Align.START)
        self.quick_synonyms_entry = Gtk.Entry()
        self.quick_synonyms_entry.set_placeholder_text("big, large, huge...")
        self.quick_synonyms_entry.connect("activate", self._on_quick_add_word)
        syn_hbox.pack_start(syn_label, False, False, 0)
        syn_hbox.pack_start(self.quick_synonyms_entry, True, True, 0)
        self.advanced_fields_box.pack_start(syn_hbox, False, False, 0)
        
        # Antonyms
        ant_hbox = Gtk.HBox(spacing=10)
        ant_label = Gtk.Label("Từ trái nghĩa:")
        ant_label.set_size_request(120, -1)
        ant_label.set_halign(Gtk.Align.START)
        self.quick_antonyms_entry = Gtk.Entry()
        self.quick_antonyms_entry.set_placeholder_text("small, tiny, little...")
        self.quick_antonyms_entry.connect("activate", self._on_quick_add_word)
        ant_hbox.pack_start(ant_label, False, False, 0)
        ant_hbox.pack_start(self.quick_antonyms_entry, True, True, 0)
        self.advanced_fields_box.pack_start(ant_hbox, False, False, 0)
        
        # Set visibility of advanced fields
        self.advanced_fields_box.set_visible(show_advanced)
        form_vbox.pack_start(self.advanced_fields_box, False, False, 0)
        
        # Separator for advanced fields
        self.advanced_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.advanced_separator.set_visible(show_advanced)
        form_vbox.pack_start(self.advanced_separator, False, False, 5)
        
        # Button and status
        button_hbox = Gtk.HBox(spacing=10)
        
        add_button = Gtk.Button(label="➕ Thêm từ vựng")
        add_button.connect("clicked", self._on_quick_add_word)
        add_button.get_style_context().add_class("suggested-action")
        button_hbox.pack_start(add_button, False, False, 0)
        
        # Nút AI sinh nghĩa hoặc dữ liệu đầy đủ
        if show_advanced:
            self.ai_button = Gtk.Button(label="🤖 AI sinh dữ liệu đầy đủ")
            self.ai_button.connect("clicked", self._on_ai_generate_comprehensive_quick)
        else:
            self.ai_button = Gtk.Button(label="🤖 AI sinh nghĩa")
            self.ai_button.connect("clicked", self._on_ai_generate_definition)
        
        if ai_helper.is_available():
            self.ai_button.get_style_context().add_class("suggested-action")
        else:
            self.ai_button.set_sensitive(False)
        button_hbox.pack_start(self.ai_button, False, False, 0)
        
        clear_button = Gtk.Button(label="🗑️ Xóa")
        clear_button.connect("clicked", self._on_clear_quick_form)
        button_hbox.pack_start(clear_button, False, False, 0)
        
        form_vbox.pack_start(button_hbox, False, False, 0)
        
        # Status label
        self.quick_add_status_label = Gtk.Label()
        self.quick_add_status_label.set_halign(Gtk.Align.START)
        form_vbox.pack_start(self.quick_add_status_label, False, False, 0)
        
        # AI status label
        self.ai_status_label = Gtk.Label()
        self.ai_status_label.set_halign(Gtk.Align.START)
        ai_status_text = ai_helper.get_setup_instructions()
        if ai_helper.is_available():
            self.ai_status_label.set_markup('<span size="small" color="green">✅ AI đã sẵn sàng!</span>')
        else:
            self.ai_status_label.set_markup('<span size="small" color="orange">⚠️ AI chưa sẵn sàng - xem hướng dẫn bên dưới</span>')
        form_vbox.pack_start(self.ai_status_label, False, False, 0)
        
        form_frame.add(form_vbox)
        section_vbox.pack_start(form_frame, False, False, 0)
        
        # Instructions
        instruction_label = Gtk.Label()
        instruction_label.set_markup('<span size="small" style="italic" color="gray">💡 Mẹo: Nhấn Enter để thêm nhanh, nút 🤖 để AI sinh nghĩa, hoặc Ctrl+M để mở quản lý từ vựng đầy đủ</span>')
        instruction_label.set_halign(Gtk.Align.START)
        section_vbox.pack_start(instruction_label, False, False, 0)
        
        # AI setup instructions (nếu cần)
        if not ai_helper.is_available():
            ai_setup_label = Gtk.Label()
            setup_text = ai_helper.get_setup_instructions()
            ai_setup_label.set_markup(f'<span size="small" color="orange">{setup_text}</span>')
            ai_setup_label.set_halign(Gtk.Align.START)
            ai_setup_label.set_line_wrap(True)
            ai_setup_label.set_max_width_chars(80)
            section_vbox.pack_start(ai_setup_label, False, False, 0)
        
        return section_vbox
    
    def _create_full_input_panel(self) -> Gtk.VBox:
        """Tạo phần nhập liệu cho quản lý đầy đủ"""
        vbox = Gtk.VBox(spacing=15)
        vbox.set_margin_left(20)
        vbox.set_margin_right(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        
        # Từ vựng
        word_label = Gtk.Label("Từ vựng:")
        word_label.set_halign(Gtk.Align.START)
        self.full_word_entry = Gtk.Entry()
        self.full_word_entry.set_placeholder_text("Nhập từ vựng...")
        self.full_word_entry.connect("activate", self._on_save_vocabulary)
        vbox.pack_start(word_label, False, False, 0)
        vbox.pack_start(self.full_word_entry, False, False, 0)
        
        # Nghĩa tiếng Việt
        def_label = Gtk.Label("Nghĩa tiếng Việt:")
        def_label.set_halign(Gtk.Align.START)
        self.definition_textview = Gtk.TextView()
        self.definition_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.definition_textview.set_editable(True)
        self.definition_textview.set_cursor_visible(True)
        self.definition_textview.set_can_focus(True)
        self.definition_textview.connect("key-press-event", self._on_textview_key_press)
        def_scrolled = Gtk.ScrolledWindow()
        def_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        def_scrolled.set_min_content_height(60)
        def_scrolled.add(self.definition_textview)
        vbox.pack_start(def_label, False, False, 0)
        vbox.pack_start(def_scrolled, False, False, 0)
        
        # Loại từ
        part_of_speech_label = Gtk.Label("Loại từ:")
        part_of_speech_label.set_halign(Gtk.Align.START)
        self.part_of_speech_combo = Gtk.ComboBoxText()
        
        # Thêm các tùy chọn loại từ
        parts_of_speech = [
            "", "Noun (Danh từ)", "Verb (Động từ)", "Adjective (Tính từ)",
            "Adverb (Trạng từ)", "Preposition (Giới từ)", "Conjunction (Liên từ)",
            "Pronoun (Đại từ)", "Interjection (Thán từ)"
        ]
        
        for part in parts_of_speech:
            self.part_of_speech_combo.append_text(part)
        
        self.part_of_speech_combo.set_active(0) # Mặc định là trống
        vbox.pack_start(part_of_speech_label, False, False, 0)
        vbox.pack_start(self.part_of_speech_combo, False, False, 0)
        
        # Phát âm
        pronunciation_label = Gtk.Label("Phát âm:")
        pronunciation_label.set_halign(Gtk.Align.START)
        self.pronunciation_entry = Gtk.Entry()
        self.pronunciation_entry.set_placeholder_text("Nhập phát âm (VD: /wɜːrd/)...")
        self.pronunciation_entry.connect("activate", self._on_save_vocabulary)
        vbox.pack_start(pronunciation_label, False, False, 0)
        vbox.pack_start(self.pronunciation_entry, False, False, 0)
        
        # Ví dụ
        example_label = Gtk.Label("Ví dụ:")
        example_label.set_halign(Gtk.Align.START)
        self.example_textview = Gtk.TextView()
        self.example_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.example_textview.set_editable(True)
        self.example_textview.set_cursor_visible(True)
        self.example_textview.set_can_focus(True)
        self.example_textview.connect("key-press-event", self._on_textview_key_press)
        ex_scrolled = Gtk.ScrolledWindow()
        ex_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        ex_scrolled.set_min_content_height(60)
        ex_scrolled.add(self.example_textview)
        vbox.pack_start(example_label, False, False, 0)
        vbox.pack_start(ex_scrolled, False, False, 0)
        
        # Ngữ cảnh sử dụng
        context_label = Gtk.Label("Ngữ cảnh sử dụng:")
        context_label.set_halign(Gtk.Align.START)
        self.context_sentences_textview = Gtk.TextView()
        self.context_sentences_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.context_sentences_textview.set_editable(True)
        self.context_sentences_textview.set_cursor_visible(True)
        self.context_sentences_textview.set_can_focus(True)
        self.context_sentences_textview.connect("key-press-event", self._on_textview_key_press)
        context_scrolled = Gtk.ScrolledWindow()
        context_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        context_scrolled.set_min_content_height(80)
        context_scrolled.add(self.context_sentences_textview)
        vbox.pack_start(context_label, False, False, 0)
        vbox.pack_start(context_scrolled, False, False, 0)
        
        # Từ đồng nghĩa
        synonyms_label = Gtk.Label("Từ đồng nghĩa:")
        synonyms_label.set_halign(Gtk.Align.START)
        self.synonyms_entry = Gtk.Entry()
        self.synonyms_entry.set_placeholder_text("Nhập từ đồng nghĩa (cách nhau bằng dấu phẩy)...")
        self.synonyms_entry.connect("activate", self._on_save_vocabulary)
        vbox.pack_start(synonyms_label, False, False, 0)
        vbox.pack_start(self.synonyms_entry, False, False, 0)
        
        # Từ trái nghĩa
        antonyms_label = Gtk.Label("Từ trái nghĩa:")
        antonyms_label.set_halign(Gtk.Align.START)
        self.antonyms_entry = Gtk.Entry()
        self.antonyms_entry.set_placeholder_text("Nhập từ trái nghĩa (cách nhau bằng dấu phẩy)...")
        self.antonyms_entry.connect("activate", self._on_save_vocabulary)
        vbox.pack_start(antonyms_label, False, False, 0)
        vbox.pack_start(self.antonyms_entry, False, False, 0)
        
        # Nút AI sinh dữ liệu đầy đủ và lưu
        button_box = Gtk.HBox(spacing=10)
        
        ai_full_button = Gtk.Button(label="🤖 AI sinh dữ liệu đầy đủ")
        ai_full_button.connect("clicked", self._on_ai_generate_full_data)
        if ai_helper.is_available():
            ai_full_button.get_style_context().add_class("suggested-action")
        else:
            ai_full_button.set_sensitive(False)
        button_box.pack_start(ai_full_button, False, False, 0)
        
        self.save_button = Gtk.Button(label="💾 Lưu từ vựng")
        self.save_button.connect("clicked", self._on_save_vocabulary)
        self.save_button.get_style_context().add_class("suggested-action")
        button_box.pack_start(self.save_button, False, False, 0)
        
        self.cancel_button = Gtk.Button(label="❌ Hủy")
        self.cancel_button.connect("clicked", self._on_cancel_vocabulary)
        button_box.pack_start(self.cancel_button, False, False, 0)
        
        vbox.pack_start(button_box, False, False, 0)
        
        return vbox
    
    def _create_list_panel(self) -> Gtk.VBox:
        """Tạo phần danh sách từ vựng"""
        vbox = Gtk.VBox(spacing=15)
        vbox.set_margin_left(20)
        vbox.set_margin_right(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        
        # Tìm kiếm
        search_label = Gtk.Label("Tìm kiếm từ vựng:")
        search_label.set_halign(Gtk.Align.START)
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Nhập từ vựng để tìm...")
        self.search_entry.connect("activate", self._on_search_vocabulary)
        vbox.pack_start(search_label, False, False, 0)
        vbox.pack_start(self.search_entry, False, False, 0)
        
        # Danh sách từ vựng
        self.vocabulary_list = Gtk.TreeView()
        self.vocabulary_list.set_headers_visible(True)
        self.vocabulary_list.set_can_focus(True)
        
        # Cột cho Từ vựng
        word_column = Gtk.TreeViewColumn("Từ vựng", Gtk.CellRendererText(), text=0)
        self.vocabulary_list.append_column(word_column)
        
        # Cột cho Nghĩa
        def_column = Gtk.TreeViewColumn("Nghĩa", Gtk.CellRendererText(), text=1)
        self.vocabulary_list.append_column(def_column)
        
        # Cột cho Bộ phận
        part_of_speech_column = Gtk.TreeViewColumn("Bộ phận", Gtk.CellRendererText(), text=2)
        self.vocabulary_list.append_column(part_of_speech_column)
        
        # Cột cho Ví dụ
        example_column = Gtk.TreeViewColumn("Ví dụ", Gtk.CellRendererText(), text=3)
        self.vocabulary_list.append_column(example_column)
        
        # Cột cho Phát âm
        pronunciation_column = Gtk.TreeViewColumn("Phát âm", Gtk.CellRendererText(), text=4)
        self.vocabulary_list.append_column(pronunciation_column)
        
        # Cột cho ID (ẩn)
        id_column = Gtk.TreeViewColumn("ID", Gtk.CellRendererText(), text=5)
        self.vocabulary_list.append_column(id_column)
        
        # Kết nối signal cho sự kiện double-click
        self.vocabulary_list.connect("row-activated", self._on_vocabulary_row_activated)
        
        # Kết nối signal cho sự kiện chọn (thông qua selection object)
        selection = self.vocabulary_list.get_selection()
        selection.connect("changed", self._on_vocabulary_selection_changed)
        
        vbox.pack_start(self.vocabulary_list, True, True, 0)
        
        # Thông tin thống kê
        self.stats_content = Gtk.Label()
        self.stats_content.set_halign(Gtk.Align.START)
        vbox.pack_start(self.stats_content, False, False, 0)
        
        return vbox
    
    def _on_quick_add_word(self, widget):
        """Xử lý thêm từ vựng nhanh"""
        if not self.word_entry or not self.definition_entry:
            return
            
        word = self.word_entry.get_text().strip()
        definition = self.definition_entry.get_text().strip()
        
        if not word or not definition:
            self._update_status("❌ Vui lòng nhập cả từ vựng và nghĩa!", "error")
            return
        
        # Lấy dữ liệu từ các trường nâng cao (nếu có)
        pronunciation = ""
        part_of_speech = ""
        example = ""
        context_sentences = ""
        synonyms = ""
        antonyms = ""
        
        # Kiểm tra nếu advanced fields đang hiển thị
        show_advanced = config_manager.get_ui_setting('show_advanced_fields', False)
        if show_advanced:
            # Pronunciation
            if self.quick_pronunciation_entry:
                pronunciation = self.quick_pronunciation_entry.get_text().strip()
            
            # Part of speech
            if self.quick_part_of_speech_combo:
                part_of_speech = self.quick_part_of_speech_combo.get_active_text() or ""
            
            # Example
            if self.quick_example_textview:
                buffer = self.quick_example_textview.get_buffer()
                start_iter = buffer.get_start_iter()
                end_iter = buffer.get_end_iter()
                example = buffer.get_text(start_iter, end_iter, False).strip()
            
            # Context sentences
            if self.quick_context_sentences_textview:
                buffer = self.quick_context_sentences_textview.get_buffer()
                start_iter = buffer.get_start_iter()
                end_iter = buffer.get_end_iter()
                context_sentences = buffer.get_text(start_iter, end_iter, False).strip()
            
            # Synonyms
            if self.quick_synonyms_entry:
                synonyms = self.quick_synonyms_entry.get_text().strip()
            
            # Antonyms
            if self.quick_antonyms_entry:
                antonyms = self.quick_antonyms_entry.get_text().strip()
        
        # Thêm từ vựng vào database với tất cả các trường
        success = self.vocab_manager.add_vocabulary(
            word, definition, example, pronunciation, part_of_speech,
            context_sentences, synonyms, antonyms
        )
        
        if success:
            self._update_status(f"✅ Đã thêm từ '{word}' thành công!", "success")
            # Clear form sau khi thêm thành công
            self._clear_quick_form()
            # Refresh danh sách từ vựng để hiển thị realtime
            self.refresh_vocabulary_list()
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
        
        # Xóa các trường nâng cao nếu có
        if hasattr(self, 'quick_pronunciation_entry') and self.quick_pronunciation_entry:
            self.quick_pronunciation_entry.set_text("")
        
        if hasattr(self, 'quick_part_of_speech_combo') and self.quick_part_of_speech_combo:
            self.quick_part_of_speech_combo.set_active(0)
        
        if hasattr(self, 'quick_example_textview') and self.quick_example_textview:
            buffer = self.quick_example_textview.get_buffer()
            buffer.set_text("")
        
        if hasattr(self, 'quick_context_sentences_textview') and self.quick_context_sentences_textview:
            buffer = self.quick_context_sentences_textview.get_buffer()
            buffer.set_text("")
        
        if hasattr(self, 'quick_synonyms_entry') and self.quick_synonyms_entry:
            self.quick_synonyms_entry.set_text("")
        
        if hasattr(self, 'quick_antonyms_entry') and self.quick_antonyms_entry:
            self.quick_antonyms_entry.set_text("")
        
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
        elif status_type == "info":
            markup = f'<span color="blue">{message}</span>'
        else:
            markup = message
        
        self.quick_add_status_label.set_markup(markup)
        
        # Tự động xóa thông báo sau 3 giây (trừ khi đang loading)
        if message and "Đang sinh nghĩa" not in message:
            GLib.timeout_add_seconds(3, lambda: self._update_status("", ""))
    
    def _on_hide_clicked(self, widget):
        """Xử lý khi click nút ẩn"""
        self.hide()
    
    def _on_ai_generate_definition(self, widget):
        """Xử lý khi click nút AI sinh nghĩa"""
        log_message("DEBUG: _on_ai_generate_definition called")
        
        if not ai_helper.is_available():
            self._update_status("❌ AI chưa sẵn sàng! Vui lòng kiểm tra thiết lập.", "error")
            return
        
        if not self.word_entry:
            log_message("ERROR: word_entry is None")
            return
            
        word = self.word_entry.get_text().strip()
        if not word:
            self._update_status("❌ Vui lòng nhập từ vựng trước!", "error")
            return
        
        log_message(f"DEBUG: Generating definition for word: {word}")
        
        # Disable nút AI và hiển thị trạng thái loading
        if self.ai_button:
            self.ai_button.set_sensitive(False)
            self.ai_button.set_label("⏳ Đang sinh nghĩa...")
        
        self._update_status("🤖 AI đang sinh nghĩa...", "info")
        
        # Sử dụng GLib.idle_add để tránh block UI
        def generate_in_background():
            try:
                log_message("DEBUG: Starting AI generation in background thread")
                definition = ai_helper.generate_definition(word)
                log_message(f"DEBUG: AI generation complete, result: {definition}")
                
                # Cập nhật UI trong main thread
                GLib.idle_add(self._on_ai_generation_complete, definition, word)
                
            except Exception as e:
                log_message(f"ERROR: Lỗi trong background AI generation: {e}")
                GLib.idle_add(self._on_ai_generation_complete, None, word)
        
        # Chạy AI generation trong background thread
        import threading
        thread = threading.Thread(target=generate_in_background)
        thread.daemon = True
        thread.start()
        log_message("DEBUG: Background thread started")

    def _on_ai_generation_complete(self, definition, word):
        """Xử lý khi AI hoàn thành sinh nghĩa"""
        log_message(f"DEBUG: _on_ai_generation_complete called with definition: {definition}")
        
        # Restore nút AI
        if self.ai_button:
            self.ai_button.set_sensitive(True)
            self.ai_button.set_label("🤖 AI sinh nghĩa")
        
        if definition:
            # Điền nghĩa vào definition entry
            if self.definition_entry:
                log_message("DEBUG: Setting definition to entry")
                self.definition_entry.set_text(definition)
            else:
                log_message("ERROR: definition_entry is None")
            
            self._update_status(f"✅ AI đã sinh nghĩa cho '{word}' thành công!", "success")
            
            # Focus vào definition entry để user có thể chỉnh sửa
            if self.definition_entry:
                self.definition_entry.grab_focus()
                # Di chuyển cursor đến cuối text
                self.definition_entry.set_position(-1)
                
        else:
            self._update_status(f"❌ Không thể sinh nghĩa cho '{word}'. Vui lòng thử lại hoặc nhập thủ công.", "error")
        
        return False  # Chỉ chạy một lần
    
    def _on_vocabulary_clicked(self, widget):
        """Xử lý khi click nút từ vựng"""
        # This method is no longer needed as the full management is in the stack
        # self.vocabulary_window = VocabularyWindow(self.window)
        # self.vocabulary_window.show()
        # log_message("Mở cửa sổ quản lý từ vựng")
        pass # No-op as the full management is in the stack
    
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
        # if self.vocabulary_window:
        #     self.vocabulary_window.destroy()
        
        if self.window:
            self.window.destroy()
            log_message("Đóng cửa sổ chính") 

    def _on_mode_switch_clicked(self, widget):
        """Xử lý khi click nút chuyển đổi chế độ"""
        if self.current_mode == "quick":
            if self.stack:
                self.stack.set_visible_child_name("full")
            self.current_mode = "full"
            if self.mode_button:
                self.mode_button.set_label("📝 Chế độ thêm nhanh")
            if self.window:
                self.window.set_default_size(900, 600)
            log_message("Chuyển sang chế độ quản lý đầy đủ")
        else:
            if self.stack:
                self.stack.set_visible_child_name("quick")
            self.current_mode = "quick"
            if self.mode_button:
                self.mode_button.set_label("📚 Chế độ quản lý")
            if self.window:
                self.window.set_default_size(500, 400)
            log_message("Chuyển sang chế độ thêm nhanh")
    
    def _on_ai_generate_full_data(self, widget):
        """Xử lý khi click nút AI sinh dữ liệu đầy đủ"""
        if not ai_helper.is_available():
            self._show_message("❌ AI chưa sẵn sàng! Vui lòng kiểm tra thiết lập.", "error")
            return
        
        if not self.full_word_entry:
            return
            
        word = self.full_word_entry.get_text().strip()
        if not word:
            self._show_message("❌ Vui lòng nhập từ vựng trước!", "error")
            return
        
        # Disable nút AI và hiển thị trạng thái loading
        widget.set_sensitive(False)
        widget.set_label("⏳ Đang sinh dữ liệu...")
        
        self._show_message("🤖 AI đang sinh dữ liệu đầy đủ...", "info")
        
        # Sử dụng GLib.idle_add để tránh block UI
        def generate_in_background():
            try:
                vocab_data = ai_helper.generate_comprehensive_vocabulary_data(word)
                
                # Cập nhật UI trong main thread
                GLib.idle_add(self._on_ai_full_generation_complete, vocab_data, word, widget)
                
            except Exception as e:
                log_message(f"ERROR: Lỗi trong background AI generation: {e}")
                GLib.idle_add(self._on_ai_full_generation_complete, None, word, widget)
        
        # Chạy AI generation trong background thread
        import threading
        thread = threading.Thread(target=generate_in_background)
        thread.daemon = True
        thread.start()
    
    def _on_ai_full_generation_complete(self, vocab_data, word, ai_button):
        """Xử lý khi AI hoàn thành sinh dữ liệu đầy đủ"""
        # Restore nút AI
        ai_button.set_sensitive(True)
        ai_button.set_label("🤖 AI sinh dữ liệu đầy đủ")
        
        if vocab_data:
            # Điền dữ liệu vào các trường
            
            # Nghĩa tiếng Việt
            if self.definition_textview and vocab_data.get('vietnamese_meaning'):
                def_buffer = self.definition_textview.get_buffer()
                def_buffer.set_text(vocab_data['vietnamese_meaning'])
            
            # Loại từ
            if self.part_of_speech_combo and vocab_data.get('word_type'):
                word_type = vocab_data['word_type']
                combo_model = self.part_of_speech_combo.get_model()
                for i, row in enumerate(combo_model):
                    if word_type.lower() in row[0].lower():
                        self.part_of_speech_combo.set_active(i)
                        break
            
            # Phát âm
            if self.pronunciation_entry and vocab_data.get('pronunciation'):
                self.pronunciation_entry.set_text(vocab_data['pronunciation'])
            
            # Ngữ cảnh sử dụng
            if self.context_sentences_textview and vocab_data.get('context_sentences'):
                context_buffer = self.context_sentences_textview.get_buffer()
                context_buffer.set_text(vocab_data['context_sentences'])
            
            # Từ đồng nghĩa
            if self.synonyms_entry and vocab_data.get('synonyms'):
                self.synonyms_entry.set_text(vocab_data['synonyms'])
            
            # Từ trái nghĩa
            if self.antonyms_entry and vocab_data.get('antonyms'):
                self.antonyms_entry.set_text(vocab_data['antonyms'])
            
            self._show_message(f"✅ AI đã sinh dữ liệu đầy đủ cho '{word}' thành công!", "success")
            
            # Focus vào definition để user có thể chỉnh sửa
            if self.definition_textview:
                self.definition_textview.grab_focus()
                
        else:
            self._show_message(f"❌ Không thể sinh dữ liệu cho '{word}'. Vui lòng thử lại hoặc nhập thủ công.", "error")
        
        return False  # Chỉ chạy một lần
    
    def _on_vocabulary_clicked(self, widget):
        """Xử lý khi click nút từ vựng"""
        # This method is no longer needed as the full management is in the stack
        # self.vocabulary_window = VocabularyWindow(self.window)
        # self.vocabulary_window.show()
        # log_message("Mở cửa sổ quản lý từ vựng")
        pass # No-op as the full management is in the stack
    
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
        # if self.vocabulary_window:
        #     self.vocabulary_window.destroy()
        
        if self.window:
            self.window.destroy()
            log_message("Đóng cửa sổ chính") 

    def _on_mode_switch_clicked(self, widget):
        """Xử lý khi click nút chuyển đổi chế độ"""
        if self.current_mode == "quick":
            if self.stack:
                self.stack.set_visible_child_name("full")
            self.current_mode = "full"
            if self.mode_button:
                self.mode_button.set_label("📝 Chế độ thêm nhanh")
            if self.window:
                self.window.set_default_size(900, 600)
            log_message("Chuyển sang chế độ quản lý đầy đủ")
        else:
            if self.stack:
                self.stack.set_visible_child_name("quick")
            self.current_mode = "quick"
            if self.mode_button:
                self.mode_button.set_label("📚 Chế độ quản lý")
            if self.window:
                self.window.set_default_size(500, 400)
            log_message("Chuyển sang chế độ thêm nhanh")
    
    def _on_save_vocabulary(self, widget):
        """Xử lý lưu từ vựng trong chế độ quản lý đầy đủ"""
        if not self.full_word_entry or not self.definition_textview:
            return
            
        word = self.full_word_entry.get_text().strip()
        
        # Lấy definition từ textview
        definition = ""
        if self.definition_textview:
            def_buffer = self.definition_textview.get_buffer()
            if def_buffer:
                start_iter = def_buffer.get_start_iter()
                end_iter = def_buffer.get_end_iter()
                definition = def_buffer.get_text(start_iter, end_iter, False).strip()
        
        # Lấy example từ textview
        example = ""
        if self.example_textview:
            example_buffer = self.example_textview.get_buffer()
            if example_buffer:
                start_iter = example_buffer.get_start_iter()
                end_iter = example_buffer.get_end_iter()
                example = example_buffer.get_text(start_iter, end_iter, False).strip()
        
        # Lấy context sentences từ textview
        context_sentences = ""
        if self.context_sentences_textview:
            context_buffer = self.context_sentences_textview.get_buffer()
            if context_buffer:
                start_iter = context_buffer.get_start_iter()
                end_iter = context_buffer.get_end_iter()
                context_sentences = context_buffer.get_text(start_iter, end_iter, False).strip()
        
        pronunciation = self.pronunciation_entry.get_text().strip() if self.pronunciation_entry else ""
        part_of_speech = self.part_of_speech_combo.get_active_text() if self.part_of_speech_combo else ""
        synonyms = self.synonyms_entry.get_text().strip() if self.synonyms_entry else ""
        antonyms = self.antonyms_entry.get_text().strip() if self.antonyms_entry else ""
        
        if not word or not definition:
            self._show_message("Vui lòng nhập cả từ vựng và nghĩa!", "error")
            return
        
        # Lưu vào database với tất cả các trường
        success = self.vocab_manager.add_vocabulary(
            word, definition, example, pronunciation, part_of_speech,
            context_sentences, synonyms, antonyms
        )
        if success:
            self._show_message(f"Đã thêm từ '{word}' thành công!", "success")
            self._clear_full_form()
            self.refresh_vocabulary_list()
        else:
            self._show_message(f"Từ '{word}' đã tồn tại hoặc có lỗi!", "error")
    
    def _on_cancel_vocabulary(self, widget):
        """Xử lý hủy chỉnh sửa từ vựng"""
        self._clear_full_form()
        self.current_editing_id = None
    
    def _on_search_vocabulary(self, widget):
        """Xử lý tìm kiếm từ vựng"""
        if not self.search_entry:
            return
        search_term = self.search_entry.get_text().strip()
        if search_term:
            vocabularies = self.vocab_manager.search_vocabulary(search_term)
        else:
            vocabularies = self.vocab_manager.get_all_vocabulary()
        self._populate_vocabulary_list(vocabularies)
    
    def _on_vocabulary_row_activated(self, treeview, path, column):
        """Xử lý khi double-click vào hàng trong danh sách từ vựng"""
        # Hiện tại chỉ làm gì đó đơn giản vì không có get_vocabulary_by_id
        log_message("Đã click vào hàng từ vựng")
    
    def _on_vocabulary_selection_changed(self, selection):
        """Xử lý khi thay đổi lựa chọn trong danh sách từ vựng"""
        # Có thể thêm logic để hiển thị thông tin chi tiết khi chọn từ vựng
        pass
    
    def _on_textview_key_press(self, widget, event):
        """Xử lý phím tắt trong textview"""
        # Ctrl+Enter để lưu
        if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_Return:
            self._on_save_vocabulary(None)
            return True
        return False
    
    def _clear_full_form(self):
        """Xóa form trong chế độ quản lý đầy đủ"""
        if self.full_word_entry:
            self.full_word_entry.set_text("")
        
        if self.definition_textview:
            def_buffer = self.definition_textview.get_buffer()
            if def_buffer:
                def_buffer.set_text("")
        
        if self.example_textview:
            example_buffer = self.example_textview.get_buffer()
            if example_buffer:
                example_buffer.set_text("")
        
        if self.context_sentences_textview:
            context_buffer = self.context_sentences_textview.get_buffer()
            if context_buffer:
                context_buffer.set_text("")
            
        if self.pronunciation_entry:
            self.pronunciation_entry.set_text("")
        
        if self.synonyms_entry:
            self.synonyms_entry.set_text("")
        
        if self.antonyms_entry:
            self.antonyms_entry.set_text("")
            
        if self.part_of_speech_combo:
            self.part_of_speech_combo.set_active(0)

    def _populate_vocabulary_list(self, vocabularies):
        """Điền danh sách từ vựng vào TreeView"""
        if not self.vocabulary_list:
            return
            
        # Tạo model cho TreeView với nhiều cột hơn
        store = Gtk.ListStore(str, str, str, str, str, str, str, str, int)  # word, definition, part_of_speech, pronunciation, synonyms, antonyms, context_sentences, example, id
        
        for vocab in vocabularies:
            store.append([
                vocab.get('word', ''),
                vocab.get('definition', ''),
                vocab.get('part_of_speech', ''),
                vocab.get('pronunciation', ''),
                vocab.get('synonyms', ''),
                vocab.get('antonyms', ''),
                vocab.get('context_sentences', ''),
                vocab.get('example', ''),
                vocab.get('id', 0)
            ])
        
        self.vocabulary_list.set_model(store)
        
        # Cập nhật thống kê
        if self.stats_content:
            self.stats_content.set_text(f"Tổng số từ vựng: {len(vocabularies)}")
    
    def refresh_vocabulary_list(self):
        """Làm mới danh sách từ vựng"""
        vocabularies = self.vocab_manager.get_all_vocabulary()
        self._populate_vocabulary_list(vocabularies)
        return False  # For GLib.idle_add
    
    def _show_message(self, message, message_type="info"):
        """Hiển thị thông báo"""
        # Tạm thời log message, có thể thêm popup dialog sau
        log_message(f"[{message_type.upper()}] {message}")
        print(f"[{message_type.upper()}] {message}")
    
    def _on_settings_clicked(self, widget):
        """Hiển thị cửa sổ Settings"""
        try:
            settings_window = SettingsWindow(self.window)
            settings_window.show()
            log_message("Opened Settings window")
        except Exception as e:
            log_message(f"Error opening Settings: {e}", "ERROR")
            self._show_message(f"Lỗi mở Settings: {e}", "error")
    
    def _on_toggle_advanced_fields(self, toggle_button):
        """Toggle hiển thị các trường nâng cao trong quick add"""
        show_advanced = toggle_button.get_active()
        
        # Lưu vào config và đảm bảo nó được lưu
        config_manager.set_ui_setting('show_advanced_fields', show_advanced)
        
        # Cập nhật hiển thị
        if hasattr(self, 'advanced_fields_box'):
            self.advanced_fields_box.set_visible(show_advanced)
        if hasattr(self, 'advanced_separator'):
            self.advanced_separator.set_visible(show_advanced)
        
        # Cập nhật nút AI
        if self.ai_button:
            # Disconnect existing handlers
            try:
                self.ai_button.disconnect_by_func(self._on_ai_generate_definition)
            except:
                pass
            try:
                self.ai_button.disconnect_by_func(self._on_ai_generate_comprehensive_quick)
            except:
                pass
            
            if show_advanced:
                self.ai_button.set_label("🤖 AI sinh dữ liệu đầy đủ")
                self.ai_button.connect("clicked", self._on_ai_generate_comprehensive_quick)
                log_message("AI button switched to comprehensive mode")
            else:
                self.ai_button.set_label("🤖 AI sinh nghĩa")
                self.ai_button.connect("clicked", self._on_ai_generate_definition)
                log_message("AI button switched to simple mode")
        
        log_message(f"Toggled advanced fields: {show_advanced}")

    def _on_ai_generate_comprehensive_quick(self, widget):
        """Generate comprehensive data trong quick add mode"""
        word = self.word_entry.get_text().strip()
        if not word:
            self._update_status("Vui lòng nhập từ vựng trước!", "error")
            return
        
        if not ai_helper.is_available():
            self._update_status("AI không sẵn sàng. Vui lòng kiểm tra cấu hình.", "error")
            return
        
        # Disable button và hiển thị trạng thái
        widget.set_sensitive(False)
        widget.set_label("⏳ AI đang sinh dữ liệu...")
        self._update_status("🤖 AI đang sinh dữ liệu đầy đủ...", "")
        
        def generate_in_background():
            try:
                vocab_data = ai_helper.generate_comprehensive_vocabulary_data(word)
                GLib.idle_add(self._on_ai_comprehensive_quick_complete, vocab_data, word, widget)
            except Exception as e:
                GLib.idle_add(self._on_ai_comprehensive_quick_complete, None, word, widget, str(e))
        
        thread = threading.Thread(target=generate_in_background)
        thread.daemon = True
        thread.start()
    
    def _on_ai_comprehensive_quick_complete(self, vocab_data, word, ai_button, error=None):
        """Xử lý kết quả sinh dữ liệu AI cho quick add"""
        ai_button.set_sensitive(True)
        ai_button.set_label("🤖 AI sinh dữ liệu đầy đủ")
        
        if error:
            self._update_status(f"Lỗi AI: {error}", "error")
            return False
        
        if not vocab_data:
            self._update_status("AI không thể sinh dữ liệu. Vui lòng thử lại.", "error")
            return False
        
        try:
            log_message(f"DEBUG: Filling comprehensive data: {vocab_data}")
            
            # Điền nghĩa tiếng Việt
            vietnamese_meaning = vocab_data.get('vietnamese_meaning', '').strip()
            if vietnamese_meaning and self.definition_entry:
                self.definition_entry.set_text(vietnamese_meaning)
                log_message(f"DEBUG: Set definition: {vietnamese_meaning}")
            
            # Điền phát âm
            pronunciation = vocab_data.get('pronunciation', '').strip()
            if pronunciation and hasattr(self, 'quick_pronunciation_entry') and self.quick_pronunciation_entry:
                self.quick_pronunciation_entry.set_text(pronunciation)
                log_message(f"DEBUG: Set pronunciation: {pronunciation}")
            
            # Điền loại từ
            word_type = vocab_data.get('word_type', '').strip()
            if word_type and hasattr(self, 'quick_part_of_speech_combo') and self.quick_part_of_speech_combo:
                # Tìm và select word type phù hợp
                combo_model = self.quick_part_of_speech_combo.get_model()
                if combo_model:
                    for i, row in enumerate(combo_model):
                        if row[0] and word_type.lower() in row[0].lower():
                            self.quick_part_of_speech_combo.set_active(i)
                            log_message(f"DEBUG: Set part of speech: {row[0]}")
                            break
            
            # Điền ví dụ
            example = vocab_data.get('example', '').strip()
            if example and hasattr(self, 'quick_example_textview') and self.quick_example_textview:
                buffer = self.quick_example_textview.get_buffer()
                buffer.set_text(example)
                log_message(f"DEBUG: Set example: {example}")
            
            # Điền ngữ cảnh sử dụng
            context_sentences = vocab_data.get('context_sentences', '')
            if context_sentences and hasattr(self, 'quick_context_sentences_textview') and self.quick_context_sentences_textview:
                if isinstance(context_sentences, list):
                    context_text = '\n'.join(context_sentences)
                else:
                    context_text = str(context_sentences)
                buffer = self.quick_context_sentences_textview.get_buffer()
                buffer.set_text(context_text)
                log_message(f"DEBUG: Set context: {context_text}")
            
            # Điền từ đồng nghĩa
            synonyms = vocab_data.get('synonyms', '')
            if synonyms and hasattr(self, 'quick_synonyms_entry') and self.quick_synonyms_entry:
                if isinstance(synonyms, list):
                    synonyms_text = ', '.join(synonyms)
                else:
                    synonyms_text = str(synonyms)
                self.quick_synonyms_entry.set_text(synonyms_text)
                log_message(f"DEBUG: Set synonyms: {synonyms_text}")
            
            # Điền từ trái nghĩa
            antonyms = vocab_data.get('antonyms', '')
            if antonyms and hasattr(self, 'quick_antonyms_entry') and self.quick_antonyms_entry:
                if isinstance(antonyms, list):
                    antonyms_text = ', '.join(antonyms)
                else:
                    antonyms_text = str(antonyms)
                self.quick_antonyms_entry.set_text(antonyms_text)
                log_message(f"DEBUG: Set antonyms: {antonyms_text}")
            
            self._update_status("✅ AI đã sinh dữ liệu đầy đủ thành công!", "success")
            log_message(f"AI generated comprehensive data for word: {word}")
            
        except Exception as e:
            log_message(f"ERROR: Error populating quick form: {e}", "ERROR")
            self._update_status(f"Lỗi điền dữ liệu: {e}", "error")
        
        return False