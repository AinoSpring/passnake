import gi
gi.require_version("Gtk", "3.0")

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.realpath("__FILE__"), os.pardir, os.pardir)))
from app import App

if __name__ == "__main__":
    App().run()
