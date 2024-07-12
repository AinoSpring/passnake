from gi.repository import Gtk, Gdk

class Tree(Gtk.TreeView):
    def __init__(self, loader, move, delete, click, add):
        self.move = move
        self.delete = delete
        self.click = click
        self.add = add
        self.tree_store = Gtk.TreeStore(str)
        loader(self.tree_store)
        super().__init__(model=self.tree_store)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Items", renderer, text=0)
        super().append_column(column)

        super().enable_model_drag_source(
            Gdk.ModifierType.BUTTON1_MASK,
            [Gtk.TargetEntry.new("text/plain", Gtk.TargetFlags.SAME_APP, 0)],
            Gdk.DragAction.MOVE
        )
        super().enable_model_drag_dest(
            [Gtk.TargetEntry.new("text/plain", Gtk.TargetFlags.SAME_APP, 0)],
            Gdk.DragAction.MOVE
        )

        super().connect("drag-data-get", self.on_drag_data_get)
        super().connect("drag-data-received", self.on_drag_data_received)
        super().connect("row-activated", self.on_row_activated)
        super().connect("button-press-event", self.on_button_press)

        super().set_headers_visible(False)

    def on_drag_data_get(self, treeview, context, selection_data, info, time):
        model, tree_iter = treeview.get_selection().get_selected()
        if tree_iter:
            path = model.get_path(tree_iter)
            selection_data.set_text(str(path), -1)
            self.dragged_path = path

    def on_drag_data_received(self, treeview, context, x, y, selection_data, info, time):
        drop_info = treeview.get_dest_row_at_pos(x, y)
        if drop_info:
            path, position = drop_info
            model = treeview.get_model()

            dragged_path = Gtk.TreePath.new_from_string(selection_data.get_text())
            dragged_iter = model.get_iter(dragged_path)
            dragged_item = model.get_value(dragged_iter, 0)

            if position == Gtk.TreeViewDropPosition.BEFORE:
                target_iter = model.get_iter(path)
                parent = model.iter_parent(target_iter)
                new_iter = model.insert_before(parent, target_iter, [dragged_item])
            elif position == Gtk.TreeViewDropPosition.AFTER:
                target_iter = model.get_iter(path)
                parent = model.iter_parent(target_iter)
                new_iter = model.insert_after(parent, target_iter, [dragged_item])
            elif position == Gtk.TreeViewDropPosition.INTO_OR_BEFORE or position == Gtk.TreeViewDropPosition.INTO_OR_AFTER:
                target_iter = model.get_iter(path)
                new_iter = model.append(target_iter, [dragged_item])
            else:
                return

            dragged_path = self.get_path(dragged_iter)
            new_path = self.get_path(new_iter)
            if dragged_path == new_path[:len(dragged_path)]:
                return

            self.move(dragged_path, new_path)

            if model.iter_has_child(dragged_iter):
                self.move_children(model, dragged_iter, new_iter)

            model.remove(dragged_iter)

    def move_children(self, model, source_iter, target_iter):
        if model.iter_has_child(source_iter):
            child_iter = model.iter_children(source_iter)
            while child_iter is not None:
                child_value = model.get_value(child_iter, 0)
                new_child_iter = model.append(target_iter, [child_value])
                self.move_children(model, child_iter, new_child_iter)
                child_iter = model.iter_next(child_iter)

    def on_row_activated(self, treeview, path, column):
        model = treeview.get_model()
        tree_iter = model.get_iter(path)
        has_children = model.iter_has_child(tree_iter)
        if has_children:
            if treeview.row_expanded(path):
                treeview.collapse_row(path)
            else:
                treeview.expand_row(path, False)

    def on_button_press(self, treeview, event):
        model = self.get_model()
        path_info = treeview.get_path_at_pos(int(event.x), int(event.y))
        if event.button == 1:
            if path_info:
                path, column, cell_x, cell_y = path_info
                iter = treeview.get_model().get_iter(path)
                self.click(self.get_path(iter), model.iter_has_child(iter))
        elif event.button == 3:
            menu = Gtk.Menu()
            iter = None
            if path_info:
                path, column, cell_x, cell_y = path_info
                treeview.grab_focus()
                treeview.set_cursor(path, column, 0)
                iter = treeview.get_model().get_iter(path)
                delete_item = Gtk.MenuItem(label="Delete")
                delete_item.connect("activate", self.delete_wrapper(path))
                menu.append(delete_item)
            add_item = Gtk.MenuItem(label="Add")
            add_item.connect("activate", self.add_wrapper(iter))
            menu.append(add_item)
            menu.show_all()
            menu.popup(None, None, None, None, event.button, event.time)

    def delete_wrapper(self, path):
        iter = self.tree_store.get_iter(path)
        name_path = self.get_path(iter)
        def on_delete(widget):
            self.delete(name_path)
            self.tree_store.remove(iter)
        return on_delete

    def add_wrapper(self, iter):
        name_path = []
        if iter is not None:
            name_path = self.get_path(iter)
        def on_add(widget):
            name = self.add(name_path)
            if name != "":
                new_iter = self.tree_store.append(iter, [name])
                model = self.get_model()
                new_path = model.get_path(new_iter)
                parent_path = model.get_path(iter)
                self.expand_row(parent_path, False)
        return on_add

    def get_path(self, iter):
        model = super().get_model()
        path = model.get_path(iter)
        paths = [path[:i] for i in range(1, len(path) + 1)]
        return [model.get_value(model.get_iter(p), 0) for p in paths]
