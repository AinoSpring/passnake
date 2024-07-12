from gi.repository import Gtk, Gdk

from tree import Tree
from input import input_dialog
from menubar import Menubar
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.realpath("__FILE__"), os.pardir, os.pardir)))
from passnake import PasswordStore

class App(Gtk.Window):
    def __init__(self):
        super().__init__(title="Passnake GUI")
        self.set_default_size(400, 300)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)

        menubar = Menubar(self)
        vbox.pack_start(menubar, False, False, 0)

        self.passphrase = input_dialog(self, "Passphrase", "Enter passphrase:", hide=True)
        self.store = PasswordStore("passnake.gpg")

        self.current_path = []

        self.paned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(self.paned, True, True, 0)

        self.tree = Tree(self.populate_tree, self.on_move, self.on_delete, self.on_click, self.on_add)
        self.paned.add(self.tree)
        self.paned.set_position(200)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.label = Gtk.Label()
        box.add(self.label)
        self.entry = Gtk.Entry()
        box.add(self.entry)
        self.button = Gtk.Button(label="Save")
        self.button.connect("clicked", self.on_save)
        self.button.set_sensitive(False)
        box.add(self.button)
        self.paned.add(box)

        def on_key_press(widget, event):
            if event.keyval == Gdk.KEY_Return:
                self.on_save(None)
                return True
        self.entry.connect("key-press-event", on_key_press)

        self.show_all()

    def populate_tree(self, tree_store):
        data = self.store.get_entry([], self.passphrase)
        self.insert_dict(tree_store, data)

    def insert_dict(self, tree_store, d, parent=None):
        for key in d.keys():
            value = d[key]
            iter = tree_store.append(parent, [key])
            if isinstance(value, dict):
                self.insert_dict(tree_store, value, parent=iter)

    def on_save(self, widget):
        data = self.entry.get_text()
        self.store.add_entry(self.current_path, data, self.passphrase)

    def on_move(self, source_path, dest_path):
        data = self.store.get_entry(source_path, self.passphrase)
        self.store.delete_entry(source_path, self.passphrase)
        self.store.add_entry(dest_path, data, self.passphrase)

    def on_delete(self, path):
        self.store.delete_entry(path, self.passphrase)

    def on_click(self, path, only_select):
        if only_select:
            self.label.set_text("")
            self.entry.set_text("")
            self.button.set_sensitive(False)
            return
        data = self.store.get_entry(path, self.passphrase)
        self.current_path = path
        self.label.set_text(str(path[-1]))
        self.entry.set_text(str(data))
        self.button.set_sensitive(True)

    def on_add(self, path):
        name = input_dialog(self, "New Entry", "Enter name:")
        if name != "":
            self.store.add_entry(path + [name], {}, self.passphrase)
        return name
