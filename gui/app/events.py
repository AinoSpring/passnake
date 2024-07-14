from .input_dialog import InputDialog


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
    path = treeview.get_path_at_pos(int(event.x), int(event.y))
    if path is None:
        return
    path = path[0]
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
    self.entry_tree.expand_row(path, False)

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
    self.on_selected(self.entry_tree, self.entry_tree.get_cursor()[0], None)

def on_move(self, source, destination):
    source_names = self.get_path_names(source)
    destination_names = self.get_path_names(destination)
    data = self.store.get_entry(source_names, self.passphrase)
    self.store.delete_entry(source_names, self.passphrase)
    self.store.add_entry(destination_names + [source_names[-1]], data, self.passphrase)
    self.entry_tree.expand_row(destination, False)
