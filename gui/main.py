import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from app import App

if __name__ == "__main__":
    app = App()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
