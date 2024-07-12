from gi.repository import Gtk, Gdk

def input_dialog(parent, title, message):
    dialog = Gtk.Dialog(title=title, transient_for=parent, flags=0)
    dialog.set_border_width(10)

    box = dialog.get_content_area()

    label = Gtk.Label(message)
    box.add(label)

    entry = Gtk.Entry()
    box.add(entry)

    dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("Ok", Gtk.ResponseType.OK)

    dialog.show_all()

    def on_key_press(widget, event):
        if event.keyval == Gdk.KEY_Return:
            dialog.response(Gtk.ResponseType.OK)
            return True
    entry.connect("key-press-event", on_key_press)

    response = dialog.run()

    input_text = ""
    if response == Gtk.ResponseType.OK:
        input_text = entry.get_text()

    dialog.destroy()
    return input_text
