from gi.repository import Gtk, Gdk
from passnake import PasswordStore
from .input_dialog import InputDialog

class App:
    def __init__(self):
        self.store = PasswordStore("passnake.gpg")

        self.builder = Gtk.Builder()
        self.builder.add_from_file("passnake.glade")

        self.passphrase = self.ask_passphrase()

        self.window = self.builder.get_object("MainWindow")
        self.entry_store = self.builder.get_object("EntryStore")
        self.data_entry = self.builder.get_object("DataEntry")
        self.save_button = self.builder.get_object("SaveButton")
        self.entry_tree = self.builder.get_object("EntryTree")
        self.tree_menu = self.builder.get_object("TreeMenu")
        self.password_search_window = self.builder.get_object("PasswordSearchWindow")
        self.password_search_entry = self.builder.get_object("PasswordSearchEntry")
        self.password_search_store = self.builder.get_object("PasswordSearchStore")

        self.window.connect("destroy", Gtk.main_quit)

        self.insert_data()

        self.data_entry.connect("activate", self.on_save)
        self.save_button.connect("clicked", self.on_save)
        self.can_input(False)

        self.entry_tree.connect("row-activated", self.on_selected)
        self.entry_tree.connect("button-press-event", self.on_button_press)

        self.builder.get_object("TreeMenuAdd").connect("activate", self.on_add)
        self.builder.get_object("TreeMenuRename").connect("activate", self.on_rename)
        self.builder.get_object("TreeMenuDelete").connect("activate", self.on_delete)
        self.builder.get_object("MenuBarPasswordSearch").connect("activate", self.password_search)
        self.builder.get_object("MenuBarChangePassphrase").connect("activate", self.change_passphrase)

        self.make_tree_draggable()
        self.password_search_entry.connect("search-changed", self.on_password_search)
        self.password_search_window.connect("key-press-event", self.on_password_window_key_press)
        self.password_search_window.connect("focus-out-event", lambda *_: self.password_search_window.hide())

    def ask_passphrase(self):
        return InputDialog(self.builder, "Enter passphrase:", hide=True).run()

    def can_input(self, value):
        self.data_entry.set_sensitive(value)
        self.save_button.set_sensitive(value)

    def toggle_extended(self, path):
        if self.entry_tree.row_expanded(path):
            self.entry_tree.collapse_row(path)
        else:
            self.entry_tree.expand_row(path, False)

    def insert_data(self, data=None, parent=None):
        if data is None:
            data = self.store.get_entry([], self.passphrase)
        assert data is not None
        for key in data.keys():
            iter = self.entry_store.append(parent, [key])
            value = data[key]
            if isinstance(value, dict):
                self.insert_data(value, iter)

    def get_path_names(self, path):
        paths = [path[:i] for i in range(1, len(path) + 1)]
        return [self.entry_store.get_value(self.entry_store.get_iter(p), 0) for p in paths]

    def change_passphrase(self, widget):
        new_passphrase = self.ask_passphrase()
        if not new_passphrase:
            return
        self.store.change_passphrase(self.passphrase, new_passphrase)
        self.passphrase = new_passphrase

    def run(self):
        self.window.show_all()
        Gtk.main()

    from .drag_tree import make_tree_draggable, on_drag_data_get, on_drag_data_received, copy_children
    from .events import on_move, on_add, on_save, on_delete, on_rename, on_selected, on_button_press
    from .password_search import search, search_data, on_password_search, password_search, on_password_window_key_press, expand_search_results
