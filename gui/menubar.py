from gi.repository import Gtk, Gdk

from input import input_dialog

class Menubar(Gtk.MenuBar):
    def __init__(self, app):
        super().__init__()
        self.app = app

        store_menu = Gtk.Menu()
        pass_item = Gtk.MenuItem(label="Change Passphrase")
        pass_item.connect("activate", self.on_pass)
        store_menu.append(pass_item)

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", Gtk.main_quit)
        store_menu.append(quit_item)

        store_menu_item = Gtk.MenuItem(label="Store")
        store_menu_item.set_submenu(store_menu)
        super().append(store_menu_item)

    def on_pass(self, widget):
        new_passphrase = input_dialog(self.app, "Passphrase", "Enter new passphrase:", hide=True)
        self.app.store.change_passphrase(self.app.passphrase, new_passphrase)
        self.app.passphrase = new_passphrase
