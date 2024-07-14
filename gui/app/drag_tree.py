from gi.repository import Gtk, Gdk


def make_tree_draggable(self):
    self.entry_tree.enable_model_drag_source(
        Gdk.ModifierType.BUTTON1_MASK,
        [Gtk.TargetEntry.new("text/plain", Gtk.TargetFlags.SAME_APP, 0)],
        Gdk.DragAction.MOVE
    )
    self.entry_tree.enable_model_drag_dest(
        [Gtk.TargetEntry.new("text/plain", Gtk.TargetFlags.SAME_APP, 0)],
        Gdk.DragAction.MOVE
    )
    self.entry_tree.connect("drag-data-get", self.on_drag_data_get)
    self.entry_tree.connect("drag-data-received", self.on_drag_data_received)

def on_drag_data_get(self, treeview, context, selection_data, info, time):
    model, tree_iter = treeview.get_selection().get_selected()
    if tree_iter:
        path = model.get_path(tree_iter)
        selection_data.set_text(str(path), -1)
        self.dragged_path = path

def on_drag_data_received(self, treeview, context, x, y, selection_data, info, time):
    drop_info = treeview.get_dest_row_at_pos(x, y)
    if drop_info is None:
        return
    path, position = drop_info
    if self.dragged_path[:] == path[:len(self.dragged_path)]:
        return
    source_iter = self.entry_store.get_iter(self.dragged_path)
    value = self.entry_store.get_value(source_iter, 0)
    target = self.entry_store.get_iter(path)
    parent = self.entry_store.iter_parent(target)
    if position == Gtk.TreeViewDropPosition.BEFORE:
        iter = self.entry_store.insert_before(parent, target, [value])
    elif position == Gtk.TreeViewDropPosition.AFTER:
        iter = self.entry_store.insert_after(parent, target, [value])
    else:
        iter = self.entry_store.append(target, [value])
    self.copy_children(source_iter, iter)
    self.on_move(self.dragged_path, path)
    self.entry_store.remove(source_iter)

def copy_children(self, source_iter, destination_iter):
    if not self.entry_store.iter_has_child(source_iter):
        return
    child_iter = self.entry_store.iter_children(source_iter)
    while child_iter is not None:
        child_value = self.entry_store.get_value(child_iter, 0)
        new_child_iter = self.entry_store.append(destination_iter, [child_value])
        self.copy_children(child_iter, new_child_iter)
        child_iter = self.entry_store.iter_next(child_iter)
