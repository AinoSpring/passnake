from gi.repository import Gtk, Gdk

from passnake import PasswordStore
from input_dialog import InputDialog

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
        self.builder.get_object("MenuBarChangePassphrase").connect("activate", self.change_passphrase)

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
            parent = self.entry_store.append(parent, [key])
            value = data[key]
            if isinstance(value, dict):
                self.insert_data(value, parent)

    def get_path_names(self, path):
        paths = [path[:i] for i in range(1, len(path) + 1)]
        return [self.entry_store.get_value(self.entry_store.get_iter(p), 0) for p in paths]

    def change_passphrase(self, widget):
        new_passphrase = self.ask_passphrase()
        if not new_passphrase:
            return
        self.store.change_passphrase(self.passphrase, new_passphrase)
        self.passphrase = new_passphrase

    def on_selected(self, treeview, path, view_column, double_click=True):
        iter = self.entry_store.get_iter(path)
        has_child = self.entry_store.iter_has_child(iter)
        self.can_input(not has_child)
        if has_child:
            self.data_entry.set_text("")
            if double_click:
                self.toggle_extended(path)
            return
        path_names = self.get_path_names(path)
        data = self.store.get_entry(path_names, self.passphrase)
        self.data_entry.set_text(str(data))

    def on_button_press(self, treeview, event):
        path = treeview.get_path_at_pos(int(event.x), int(event.y))[0]
        if event.button == 1:
            self.on_selected(treeview, path, None, False)
        elif event.button == 3:
            self.tree_menu.popup(None, None, None, None, event.button, event.time)

    def on_save(self, widget):
        data = self.data_entry.get_text()
        path = self.entry_tree.get_cursor()[0]
        iter = self.entry_store.get_iter(path)
        if self.entry_store.iter_has_child(iter):
            return
        path_names = self.get_path_names(path)
        self.store.add_entry(path_names, data, self.passphrase)

    def on_add(self, widget):
        path = self.entry_tree.get_cursor()[0]
        iter = self.entry_store.get_iter(path)
        name = InputDialog(self.builder, "Enter name:").run()
        if not name:
            return
        path_names = self.get_path_names(path)
        self.store.add_entry(path_names + [name], "", self.passphrase)
        self.insert_data({name: ""}, iter)

    def on_rename(self, widget):
        path = self.entry_tree.get_cursor()[0]
        iter = self.entry_store.get_iter(path)
        path_names = self.get_path_names(path)
        name = InputDialog(self.builder, "Enter new name:", default=path_names[-1]).run()
        if not name:
            return
        data = self.store.get_entry(path_names, self.passphrase)
        self.store.delete_entry(path_names, self.passphrase)
        self.store.add_entry(path_names[:-1] + [name], data, self.passphrase)
        self.entry_store.set_value(iter, 0, name)

    def on_delete(self, widget):
        path = self.entry_tree.get_cursor()[0]
        iter = self.entry_store.get_iter(path)
        path_names = self.get_path_names(path)
        self.store.delete_entry(path_names, self.passphrase)
        self.entry_store.remove(iter)
        self.on_row_activated(self.entry_tree, self.entry_tree.get_cursor()[0], None)

    def run(self):
        self.window.show_all()
        Gtk.main()
