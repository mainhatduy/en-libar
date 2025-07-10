"""
Vocabulary Window - Giao diện quản lý từ vựng
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject
from typing import Optional, Dict

from ..core.vocabulary_manager import VocabularyManager
from ..utils.helpers import log_message
from ..utils.ai_helper import ai_helper

class VocabularyWindow:
    """Class quản lý cửa sổ từ vựng"""
    
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.vocab_manager = VocabularyManager()
        self.window = None
        self.vocabulary_list = None
        self.search_entry = None
        self.word_entry = None
        self.definition_textview = None
        self.example_textview = None
        self.pronunciation_entry = None
        self.part_of_speech_combo = None
        self.context_sentences_textview = None
        self.synonyms_entry = None
        self.antonyms_entry = None
        self.current_editing_id = None
        self.setup_ui()
        self.refresh_vocabulary_list()
    
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        self.window = Gtk.Window()
        self.window.set_title("Quản lý Từ vựng")
        self.window.set_default_size(900, 600)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        
        if self.parent_window:
            self.window.set_transient_for(self.parent_window)
        
        # Tạo layout chính
        main_paned = self._create_main_layout()
        self.window.add(main_paned)
        
        # Kết nối signal handlers
        self.window.connect("delete-event", self._on_window_delete)
        self.window.connect("key-press-event", self._on_key_press)
    
    def _create_main_layout(self) -> Gtk.Paned:
        """Tạo layout chính với paned"""
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        
        # Phần trái: Form nhập liệu
        left_panel = self._create_input_panel()
        paned.pack1(left_panel, False, False)
        
        # Phần phải: Danh sách từ vựng
        right_panel = self._create_list_panel()
        paned.pack2(right_panel, True, False)
        
        paned.set_position(400)
        return paned
    
    def _create_input_panel(self) -> Gtk.ScrolledWindow:
        """Tạo panel nhập liệu"""
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        vbox = Gtk.VBox(spacing=10)
        vbox.set_margin_left(15)
        vbox.set_margin_right(15)
        vbox.set_margin_top(15)
        vbox.set_margin_bottom(15)
        
        # Tiêu đề
        title_label = Gtk.Label()
        title_label.set_markup('<span size="large" weight="bold">📝 Thêm từ vựng mới</span>')
        title_label.set_halign(Gtk.Align.START)
        vbox.pack_start(title_label, False, False, 0)
        
        # Form fields
        vbox.pack_start(self._create_word_field(), False, False, 0)
        vbox.pack_start(self._create_pronunciation_field(), False, False, 0)
        vbox.pack_start(self._create_part_of_speech_field(), False, False, 0)
        vbox.pack_start(self._create_definition_field(), True, True, 0)
        vbox.pack_start(self._create_example_field(), True, True, 0)
        vbox.pack_start(self._create_context_sentences_field(), True, True, 0)
        vbox.pack_start(self._create_synonyms_field(), False, False, 0)
        vbox.pack_start(self._create_antonyms_field(), False, False, 0)
        
        # Buttons
        button_box = self._create_button_box()
        vbox.pack_start(button_box, False, False, 0)
        
        # Stats
        stats_box = self._create_stats_box()
        vbox.pack_start(stats_box, False, False, 0)
        
        scrolled.add(vbox)
        return scrolled
    
    def _create_word_field(self) -> Gtk.VBox:
        """Tạo field nhập từ vựng"""
        vbox = Gtk.VBox(spacing=5)
        
        label = Gtk.Label("Từ vựng *")
        label.set_halign(Gtk.Align.START)
        vbox.pack_start(label, False, False, 0)
        
        self.word_entry = Gtk.Entry()
        self.word_entry.set_placeholder_text("Nhập từ vựng...")
        self.word_entry.connect("activate", self._on_save_clicked)
        vbox.pack_start(self.word_entry, False, False, 0)
        
        return vbox
    
    def _create_pronunciation_field(self) -> Gtk.VBox:
        """Tạo field nhập phát âm"""
        vbox = Gtk.VBox(spacing=5)
        
        label = Gtk.Label("Phát âm")
        label.set_halign(Gtk.Align.START)
        vbox.pack_start(label, False, False, 0)
        
        self.pronunciation_entry = Gtk.Entry()
        self.pronunciation_entry.set_placeholder_text("/pronunciation/")
        vbox.pack_start(self.pronunciation_entry, False, False, 0)
        
        return vbox
    
    def _create_part_of_speech_field(self) -> Gtk.VBox:
        """Tạo field chọn loại từ"""
        vbox = Gtk.VBox(spacing=5)
        
        label = Gtk.Label("Loại từ")
        label.set_halign(Gtk.Align.START)
        vbox.pack_start(label, False, False, 0)
        
        self.part_of_speech_combo = Gtk.ComboBoxText()
        parts_of_speech = [
            "", "Noun (Danh từ)", "Verb (Động từ)", "Adjective (Tính từ)",
            "Adverb (Trạng từ)", "Preposition (Giới từ)", "Conjunction (Liên từ)",
            "Pronoun (Đại từ)", "Interjection (Thán từ)"
        ]
        
        for part in parts_of_speech:
            self.part_of_speech_combo.append_text(part)
        
        self.part_of_speech_combo.set_active(0)
        vbox.pack_start(self.part_of_speech_combo, False, False, 0)
        
        return vbox
    
    def _create_definition_field(self) -> Gtk.VBox:
        """Tạo field nhập nghĩa"""
        vbox = Gtk.VBox(spacing=5)
        
        label = Gtk.Label("Nghĩa tiếng Việt *")
        label.set_halign(Gtk.Align.START)
        vbox.pack_start(label, False, False, 0)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(80)
        
        self.definition_textview = Gtk.TextView()
        self.definition_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled.add(self.definition_textview)
        vbox.pack_start(scrolled, True, True, 0)
        
        return vbox
    
    def _create_example_field(self) -> Gtk.VBox:
        """Tạo field nhập ví dụ"""
        vbox = Gtk.VBox(spacing=5)
        
        label = Gtk.Label("Ví dụ")
        label.set_halign(Gtk.Align.START)
        vbox.pack_start(label, False, False, 0)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(80)
        
        self.example_textview = Gtk.TextView()
        self.example_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled.add(self.example_textview)
        vbox.pack_start(scrolled, True, True, 0)
        
        return vbox

    def _create_context_sentences_field(self) -> Gtk.VBox:
        """Tạo field nhập ngữ cảnh sử dụng"""
        vbox = Gtk.VBox(spacing=5)
        
        label = Gtk.Label("Ngữ cảnh sử dụng")
        label.set_halign(Gtk.Align.START)
        vbox.pack_start(label, False, False, 0)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(100)
        
        self.context_sentences_textview = Gtk.TextView()
        self.context_sentences_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled.add(self.context_sentences_textview)
        vbox.pack_start(scrolled, True, True, 0)
        
        return vbox

    def _create_synonyms_field(self) -> Gtk.VBox:
        """Tạo field nhập từ đồng nghĩa"""
        vbox = Gtk.VBox(spacing=5)
        
        label = Gtk.Label("Từ đồng nghĩa")
        label.set_halign(Gtk.Align.START)
        vbox.pack_start(label, False, False, 0)
        
        self.synonyms_entry = Gtk.Entry()
        self.synonyms_entry.set_placeholder_text("Nhập từ đồng nghĩa (cách nhau bằng dấu phẩy)")
        vbox.pack_start(self.synonyms_entry, False, False, 0)
        
        return vbox

    def _create_antonyms_field(self) -> Gtk.VBox:
        """Tạo field nhập từ trái nghĩa"""
        vbox = Gtk.VBox(spacing=5)
        
        label = Gtk.Label("Từ trái nghĩa")
        label.set_halign(Gtk.Align.START)
        vbox.pack_start(label, False, False, 0)
        
        self.antonyms_entry = Gtk.Entry()
        self.antonyms_entry.set_placeholder_text("Nhập từ trái nghĩa (cách nhau bằng dấu phẩy)")
        vbox.pack_start(self.antonyms_entry, False, False, 0)
        
        return vbox

    def _create_button_box(self) -> Gtk.HBox:
        """Tạo box chứa các nút"""
        hbox = Gtk.HBox(spacing=10)
        
        # Nút AI sinh dữ liệu đầy đủ
        ai_button = Gtk.Button(label="🤖 AI sinh dữ liệu đầy đủ")
        ai_button.connect("clicked", self._on_ai_generate_full_data)
        if ai_helper.is_available():
            ai_button.get_style_context().add_class("suggested-action")
        else:
            ai_button.set_sensitive(False)
        hbox.pack_start(ai_button, False, False, 0)
        
        # Nút Lưu
        save_button = Gtk.Button(label="💾 Lưu")
        save_button.connect("clicked", self._on_save_clicked)
        save_button.get_style_context().add_class("suggested-action")
        hbox.pack_start(save_button, False, False, 0)
        
        # Nút Clear
        clear_button = Gtk.Button(label="🗑️ Clear")
        clear_button.connect("clicked", self._on_clear_clicked)
        hbox.pack_start(clear_button, False, False, 0)
        
        # Nút Cancel Edit (chỉ hiển thị khi đang edit)
        self.cancel_edit_button = Gtk.Button(label="❌ Hủy sửa")
        self.cancel_edit_button.connect("clicked", self._on_cancel_edit_clicked)
        self.cancel_edit_button.set_visible(False)
        hbox.pack_start(self.cancel_edit_button, False, False, 0)
        
        return hbox
    
    def _create_stats_box(self) -> Gtk.VBox:
        """Tạo box hiển thị thống kê"""
        vbox = Gtk.VBox(spacing=5)
        
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(separator, False, False, 10)
        
        stats_label = Gtk.Label()
        stats_label.set_markup('<span size="small" weight="bold">📊 Thống kê</span>')
        stats_label.set_halign(Gtk.Align.START)
        vbox.pack_start(stats_label, False, False, 0)
        
        self.stats_content = Gtk.Label()
        self.stats_content.set_halign(Gtk.Align.START)
        self._update_stats()
        vbox.pack_start(self.stats_content, False, False, 0)
        
        return vbox
    
    def _create_list_panel(self) -> Gtk.VBox:
        """Tạo panel danh sách từ vựng"""
        vbox = Gtk.VBox(spacing=10)
        vbox.set_margin_left(15)
        vbox.set_margin_right(15)
        vbox.set_margin_top(15)
        vbox.set_margin_bottom(15)
        
        # Tiêu đề và tìm kiếm
        header_box = self._create_list_header()
        vbox.pack_start(header_box, False, False, 0)
        
        # Danh sách từ vựng
        list_scrolled = self._create_vocabulary_list()
        vbox.pack_start(list_scrolled, True, True, 0)
        
        return vbox
    
    def _create_list_header(self) -> Gtk.VBox:
        """Tạo header cho danh sách"""
        vbox = Gtk.VBox(spacing=10)
        
        # Tiêu đề
        title_label = Gtk.Label()
        title_label.set_markup('<span size="large" weight="bold">📚 Danh sách từ vựng</span>')
        title_label.set_halign(Gtk.Align.START)
        vbox.pack_start(title_label, False, False, 0)
        
        # Tìm kiếm
        search_box = Gtk.HBox(spacing=10)
        
        search_label = Gtk.Label("🔍")
        search_box.pack_start(search_label, False, False, 0)
        
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Tìm kiếm từ vựng...")
        self.search_entry.connect("changed", self._on_search_changed)
        search_box.pack_start(self.search_entry, True, True, 0)
        
        refresh_button = Gtk.Button(label="🔄")
        refresh_button.set_tooltip_text("Làm mới danh sách")
        refresh_button.connect("clicked", self._on_refresh_clicked)
        search_box.pack_start(refresh_button, False, False, 0)
        
        vbox.pack_start(search_box, False, False, 0)
        
        return vbox
    
    def _create_vocabulary_list(self) -> Gtk.ScrolledWindow:
        """Tạo danh sách từ vựng"""
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        # Tạo TreeView với các cột
        self.vocabulary_list = Gtk.TreeView()
        
        # Model: word, pronunciation, part_of_speech, definition, example, created_at, id
        self.list_store = Gtk.ListStore(str, str, str, str, str, str, str, str, str, int)
        self.vocabulary_list.set_model(self.list_store)
        
        # Tạo các cột
        self._create_tree_columns()
        
        # Kết nối signal
        self.vocabulary_list.connect("row-activated", self._on_row_activated)
        self.vocabulary_list.connect("button-press-event", self._on_list_button_press)
        
        scrolled.add(self.vocabulary_list)
        return scrolled
    
    def _create_tree_columns(self):
        """Tạo các cột cho TreeView"""
        columns_config = [
            ("Từ vựng", 0, 120),
            ("Phát âm", 1, 100),
            ("Loại từ", 2, 100),
            ("Nghĩa", 3, 200),
            ("Ví dụ", 4, 150),
            ("Ngữ cảnh", 5, 200),
            ("Đồng nghĩa", 6, 120),
            ("Trái nghĩa", 7, 120),
            ("Ngày tạo", 8, 100)
        ]
        
        for title, column_id, width in columns_config:
            renderer = Gtk.CellRendererText()
            renderer.set_property("wrap-mode", 2)  # WRAP_WORD
            renderer.set_property("wrap-width", width)
            
            column = Gtk.TreeViewColumn(title, renderer, text=column_id)
            column.set_resizable(True)
            column.set_min_width(width)
            column.set_sort_column_id(column_id)
            
            self.vocabulary_list.append_column(column)

    def _on_ai_generate_full_data(self, widget):
        """Xử lý khi click nút AI sinh dữ liệu đầy đủ"""
        if not ai_helper.is_available():
            self._show_message("❌ AI chưa sẵn sàng! Vui lòng kiểm tra thiết lập.", "error")
            return
        
        word = self.word_entry.get_text().strip()
        if not word:
            self._show_message("❌ Vui lòng nhập từ vựng trước!", "error")
            return
        
        # Disable nút AI và hiển thị trạng thái loading
        widget.set_sensitive(False)
        widget.set_label("⏳ Đang sinh dữ liệu...")
        
        # Sử dụng GLib.idle_add để tránh block UI
        def generate_in_background():
            try:
                vocab_data = ai_helper.generate_comprehensive_vocabulary_data(word)
                
                # Cập nhật UI trong main thread
                GObject.idle_add(self._on_ai_full_generation_complete, vocab_data, word, widget)
                
            except Exception as e:
                log_message(f"ERROR: Lỗi trong background AI generation: {e}")
                GObject.idle_add(self._on_ai_full_generation_complete, None, word, widget)
        
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
            if vocab_data.get('vietnamese_meaning'):
                def_buffer = self.definition_textview.get_buffer()
                def_buffer.set_text(vocab_data['vietnamese_meaning'])
            
            # Loại từ
            if vocab_data.get('word_type'):
                word_type = vocab_data['word_type']
                combo_model = self.part_of_speech_combo.get_model()
                for i, row in enumerate(combo_model):
                    if word_type.lower() in row[0].lower():
                        self.part_of_speech_combo.set_active(i)
                        break
            
            # Phát âm
            if vocab_data.get('pronunciation'):
                self.pronunciation_entry.set_text(vocab_data['pronunciation'])
            
            # Ngữ cảnh sử dụng
            if vocab_data.get('context_sentences'):
                context_buffer = self.context_sentences_textview.get_buffer()
                context_buffer.set_text(vocab_data['context_sentences'])
            
            # Từ đồng nghĩa
            if vocab_data.get('synonyms'):
                self.synonyms_entry.set_text(vocab_data['synonyms'])
            
            # Từ trái nghĩa
            if vocab_data.get('antonyms'):
                self.antonyms_entry.set_text(vocab_data['antonyms'])
            
            self._show_message(f"✅ AI đã sinh dữ liệu đầy đủ cho '{word}' thành công!", "success")
                
        else:
            self._show_message(f"❌ Không thể sinh dữ liệu cho '{word}'. Vui lòng thử lại hoặc nhập thủ công.", "error")
        
        return False  # Chỉ chạy một lần

    def _on_save_clicked(self, widget):
        """Xử lý khi click nút Lưu"""
        word = self.word_entry.get_text().strip()
        pronunciation = self.pronunciation_entry.get_text().strip()
        part_of_speech = self.part_of_speech_combo.get_active_text() or ""
        
        # Lấy definition
        def_buffer = self.definition_textview.get_buffer()
        definition = def_buffer.get_text(
            def_buffer.get_start_iter(),
            def_buffer.get_end_iter(),
            False
        ).strip()
        
        # Lấy example
        ex_buffer = self.example_textview.get_buffer()
        example = ex_buffer.get_text(
            ex_buffer.get_start_iter(),
            ex_buffer.get_end_iter(),
            False
        ).strip()
        
        # Lấy context sentences
        context_buffer = self.context_sentences_textview.get_buffer()
        context_sentences = context_buffer.get_text(
            context_buffer.get_start_iter(),
            context_buffer.get_end_iter(),
            False
        ).strip()
        
        # Lấy synonyms và antonyms
        synonyms = self.synonyms_entry.get_text().strip()
        antonyms = self.antonyms_entry.get_text().strip()
        
        # Validation
        if not word or not definition:
            self._show_message("Vui lòng nhập từ vựng và định nghĩa!", "error")
            return
        
        # Lưu hoặc cập nhật
        if self.current_editing_id is not None:
            # Cập nhật
            success = self.vocab_manager.update_vocabulary(
                self.current_editing_id, word, definition, example, pronunciation, 
                part_of_speech, context_sentences, synonyms, antonyms
            )
            if success:
                self._show_message(f"Đã cập nhật từ '{word}' thành công!", "success")
                self._cancel_edit_mode()
            else:
                self._show_message("Lỗi khi cập nhật từ vựng!", "error")
        else:
            # Thêm mới
            success = self.vocab_manager.add_vocabulary(
                word, definition, example, pronunciation, part_of_speech,
                context_sentences, synonyms, antonyms
            )
            if success:
                self._show_message(f"Đã thêm từ '{word}' thành công!", "success")
                self._clear_form()
            else:
                self._show_message(f"Từ '{word}' đã tồn tại hoặc có lỗi xảy ra!", "error")
        
        if success:
            self.refresh_vocabulary_list()
            self._update_stats()
    
    def _on_clear_clicked(self, widget):
        """Xử lý khi click nút Clear"""
        self._clear_form()
    
    def _on_cancel_edit_clicked(self, widget):
        """Xử lý khi click nút Cancel edit"""
        self._cancel_edit_mode()
    
    def _on_search_changed(self, widget):
        """Xử lý khi thay đổi text tìm kiếm"""
        search_text = self.search_entry.get_text().strip()
        if search_text:
            vocabularies = self.vocab_manager.search_vocabulary(search_text)
        else:
            vocabularies = self.vocab_manager.get_all_vocabulary()
        
        self._populate_list(vocabularies)
    
    def _on_refresh_clicked(self, widget):
        """Xử lý khi click nút refresh"""
        self.refresh_vocabulary_list()
        self._update_stats()
    
    def _on_row_activated(self, treeview, path, column):
        """Xử lý khi double-click vào row"""
        model = treeview.get_model()
        iter = model.get_iter(path)
        vocab_id = model.get_value(iter, 9)  # ID ở cột ẩn cuối
        self._edit_vocabulary(vocab_id)
    
    def _on_list_button_press(self, widget, event):
        """Xử lý khi click chuột vào list"""
        if event.button == 3:  # Right click
            log_message("Right-click detected on vocabulary list")
            path_info = widget.get_path_at_pos(int(event.x), int(event.y))
            if path_info:
                path = path_info[0]
                log_message(f"Right-click on path: {path}")
                widget.get_selection().select_path(path)
                self._show_context_menu(event, path)
            else:
                log_message("Right-click but no path info found")
    
    def _show_context_menu(self, event, path):
        """Hiển thị context menu"""
        menu = Gtk.Menu()
        
        # Menu Edit
        edit_item = Gtk.MenuItem(label="✏️ Chỉnh sửa")
        edit_item.connect("activate", lambda x: self._edit_vocabulary_from_path(path))
        menu.append(edit_item)
        
        # Menu Delete
        delete_item = Gtk.MenuItem(label="🗑️ Xóa")
        delete_item.connect("activate", lambda x: self._delete_vocabulary_from_path(path))
        menu.append(delete_item)
        
        # Menu Mark as reviewed
        reviewed_item = Gtk.MenuItem(label="✅ Đánh dấu đã ôn")
        reviewed_item.connect("activate", lambda x: self._mark_reviewed_from_path(path))
        menu.append(reviewed_item)
        
        menu.show_all()
        menu.popup(None, None, None, None, event.button, event.time)
    
    def _edit_vocabulary_from_path(self, path):
        """Chỉnh sửa từ vựng từ path"""
        model = self.vocabulary_list.get_model()
        iter = model.get_iter(path)
        vocab_id = model.get_value(iter, 9)
        self._edit_vocabulary(vocab_id)
    
    def _delete_vocabulary_from_path(self, path):
        """Xóa từ vựng từ path"""
        try:
            model = self.vocabulary_list.get_model()
            iter = model.get_iter(path)
            vocab_id = model.get_value(iter, 9)
            word = model.get_value(iter, 0)
            
            # Debug logging
            log_message(f"Attempting to delete vocabulary - ID: {vocab_id}, Word: '{word}'")
            
            # Validate that we have a valid vocab_id
            if not vocab_id or not isinstance(vocab_id, int) or vocab_id <= 0:
                log_message(f"ERROR: Invalid vocab_id: {vocab_id} (type: {type(vocab_id)})")
                self._show_message("Lỗi: ID từ vựng không hợp lệ!", "error")
                return
            
            # Confirm dialog
            dialog = Gtk.MessageDialog(
                transient_for=self.window,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text=f"Bạn có chắc muốn xóa từ '{word}'?"
            )
            
            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                log_message(f"User confirmed deletion of vocab ID: {vocab_id}")
                
                delete_result = self.vocab_manager.delete_vocabulary(vocab_id)
                log_message(f"Delete operation result: {delete_result}")
                
                if delete_result:
                    self.refresh_vocabulary_list()
                    self._update_stats()
                    log_message(f"Successfully deleted vocabulary: {word}")
                else:
                    self._show_message("Lỗi khi xóa từ vựng!", "error")
                    log_message(f"Failed to delete vocabulary: {word}")
            else:
                log_message("User cancelled deletion")
            
            dialog.destroy()
            
        except Exception as e:
            log_message(f"ERROR in _delete_vocabulary_from_path: {e}")
            self._show_message(f"Lỗi xóa từ vựng: {str(e)}", "error")
    
    def _mark_reviewed_from_path(self, path):
        """Đánh dấu đã ôn từ path"""
        model = self.vocabulary_list.get_model()
        iter = model.get_iter(path)
        vocab_id = model.get_value(iter, 9)
        word = model.get_value(iter, 0)
        
        if self.vocab_manager.mark_as_reviewed(vocab_id):
            self._show_message(f"Đã đánh dấu ôn tập từ '{word}'!", "success")
            self._update_stats()
        else:
            self._show_message("Lỗi khi đánh dấu ôn tập!", "error")
    
    def _edit_vocabulary(self, vocab_id):
        """Chỉnh sửa từ vựng"""
        # Lấy thông tin từ vựng
        vocabularies = self.vocab_manager.get_all_vocabulary()
        vocab = next((v for v in vocabularies if v['id'] == vocab_id), None)
        
        if not vocab:
            self._show_message("Không tìm thấy từ vựng!", "error")
            return
        
        # Điền vào form
        self.word_entry.set_text(vocab['word'] or "")
        self.pronunciation_entry.set_text(vocab['pronunciation'] or "")
        
        # Set part of speech
        part_of_speech = vocab['part_of_speech'] or ""
        combo_model = self.part_of_speech_combo.get_model()
        for i, row in enumerate(combo_model):
            if row[0] == part_of_speech:
                self.part_of_speech_combo.set_active(i)
                break
        
        # Set definition
        def_buffer = self.definition_textview.get_buffer()
        def_buffer.set_text(vocab['definition'] or "")
        
        # Set example
        ex_buffer = self.example_textview.get_buffer()
        ex_buffer.set_text(vocab['example'] or "")
        
        # Set context sentences
        context_buffer = self.context_sentences_textview.get_buffer()
        context_buffer.set_text(vocab['context_sentences'] or "")
        
        # Set synonyms and antonyms
        self.synonyms_entry.set_text(vocab['synonyms'] or "")
        self.antonyms_entry.set_text(vocab['antonyms'] or "")
        
        # Chuyển sang edit mode
        self.current_editing_id = vocab_id
        self._update_edit_mode()
        
        # Focus vào word entry
        self.word_entry.grab_focus()
        log_message(f"Bắt đầu chỉnh sửa từ vựng: {vocab['word']}")

    def _cancel_edit_mode(self):
        """Hủy chế độ chỉnh sửa"""
        self.current_editing_id = None
        self._update_edit_mode()
    
    def _clear_form(self):
        """Xóa form"""
        self.word_entry.set_text("")
        self.pronunciation_entry.set_text("")
        self.part_of_speech_combo.set_active(0)
        
        # Clear textviews
        def_buffer = self.definition_textview.get_buffer()
        def_buffer.set_text("")
        
        ex_buffer = self.example_textview.get_buffer()
        ex_buffer.set_text("")
        
        context_buffer = self.context_sentences_textview.get_buffer()
        context_buffer.set_text("")
        
        # Clear entries
        self.synonyms_entry.set_text("")
        self.antonyms_entry.set_text("")
        
        # Focus vào word entry
        self.word_entry.grab_focus()

    def _update_edit_mode(self):
        """Cập nhật giao diện khi vào chế độ chỉnh sửa"""
        self.save_button.set_label("💾 Cập nhật")
        self.cancel_edit_button.set_visible(True)
        self.cancel_edit_button.show()
    
    def _populate_list(self, vocabularies):
        """Điền dữ liệu vào danh sách"""
        self.list_store.clear()
        
        for vocab in vocabularies:
            # Format ngày tạo
            created_at = vocab['created_at'][:10] if vocab['created_at'] else ""
            
            # Validate vocab ID
            vocab_id = vocab.get('id')
            if vocab_id is None:
                log_message(f"WARNING: Missing ID for vocabulary: {vocab.get('word', 'unknown')}")
                continue
                
            try:
                vocab_id = int(vocab_id)
            except (ValueError, TypeError):
                log_message(f"ERROR: Invalid ID type for vocabulary {vocab.get('word', 'unknown')}: {vocab_id} (type: {type(vocab_id)})")
                continue
            
            if vocab_id <= 0:
                log_message(f"ERROR: Invalid ID value for vocabulary {vocab.get('word', 'unknown')}: {vocab_id}")
                continue
            
            # Truncate long text for display
            def truncate_text(text, max_length=50):
                if not text:
                    return ""
                return text[:max_length] + "..." if len(text) > max_length else text
            
            self.list_store.append([
                vocab['word'] or "",
                vocab['pronunciation'] or "",
                vocab['part_of_speech'] or "",
                truncate_text(vocab['definition'] or ""),
                truncate_text(vocab['example'] or ""),
                truncate_text(vocab['context_sentences'] or ""),
                truncate_text(vocab['synonyms'] or ""),
                truncate_text(vocab['antonyms'] or ""),
                created_at,
                vocab_id  # Cột ẩn chứa ID (đã validate)
            ])
            
        log_message(f"Populated list with {len(vocabularies)} vocabularies")
    
    def _update_stats(self):
        """Cập nhật thống kê"""
        stats = self.vocab_manager.get_vocabulary_stats()
        stats_text = f"""📊 Tổng số từ: {stats['total_words']}
✅ Đã ôn tập: {stats['reviewed_words']}
🆕 Hôm nay: {stats['today_words']}
⏳ Chưa ôn: {stats['unreviewed_words']}"""
        
        self.stats_content.set_markup(f'<span size="small">{stats_text}</span>')
    
    def _show_message(self, message, message_type="info"):
        """Hiển thị thông báo"""
        if message_type == "error":
            msg_type = Gtk.MessageType.ERROR
        elif message_type == "success":
            msg_type = Gtk.MessageType.INFO
        else:
            msg_type = Gtk.MessageType.INFO
        
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=msg_type,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        
        dialog.run()
        dialog.destroy()
    
    def _on_window_delete(self, widget, event):
        """Xử lý khi đóng cửa sổ"""
        return False  # Cho phép đóng cửa sổ
    
    def _on_key_press(self, widget, event):
        """Xử lý phím tắt"""
        # Ctrl+S để lưu
        if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_s:
            self._on_save_clicked(None)
            return True
        
        # Ctrl+R để refresh
        if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_r:
            self._on_refresh_clicked(None)
            return True
        
        # Delete key để xóa từ vựng đã chọn
        if event.keyval == Gdk.KEY_Delete:
            selection = self.vocabulary_list.get_selection()
            model, iter = selection.get_selected()
            if iter:
                path = model.get_path(iter)
                log_message(f"Delete key pressed, deleting item at path: {path}")
                self._delete_vocabulary_from_path(path)
                return True
        
        # Escape để hủy edit
        if event.keyval == Gdk.KEY_Escape and self.current_editing_id is not None:
            self._cancel_edit_mode()
            return True
        
        return False
    
    def refresh_vocabulary_list(self):
        """Làm mới danh sách từ vựng"""
        log_message("Refreshing vocabulary list...")
        search_text = self.search_entry.get_text().strip() if self.search_entry else ""
        
        if search_text:
            log_message(f"Searching vocabularies with term: '{search_text}'")
            vocabularies = self.vocab_manager.search_vocabulary(search_text)
        else:
            log_message("Getting all vocabularies")
            vocabularies = self.vocab_manager.get_all_vocabulary()
        
        log_message(f"Retrieved {len(vocabularies)} vocabularies from database")
        self._populate_list(vocabularies)
    
    def show(self):
        """Hiển thị cửa sổ"""
        if self.window:
            self.window.show_all()
            self.window.present()
            log_message("Hiển thị cửa sổ từ vựng")
    
    def hide(self):
        """Ẩn cửa sổ"""
        if self.window:
            self.window.hide()
    
    def destroy(self):
        """Hủy cửa sổ"""
        if self.window:
            self.window.destroy() 