from gi.repository import Gtk, Gdk

class InputDialog:
    def __init__(self, builder, message, hide=False, default=""):
        self.dialog = builder.get_object("InputDialog")
        self.entry = builder.get_object("InputDialogEntry")
        self.entry.set_visibility(not hide)
        self.entry.set_text(default)
        self.entry.connect("activate", lambda _: self.dialog.response(Gtk.ResponseType.OK))
        self.label = builder.get_object("InputDialogLabel")
        self.label.set_text(message)

    def run(self):
        self.dialog.show_all()
        response = self.dialog.run()
        input_text = ""
        if response == Gtk.ResponseType.OK:
            input_text = self.entry.get_text()
        self.dialog.hide()
        return input_text
