import argparse
import os
from getpass import getpass
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.realpath("__FILE__"), os.pardir, os.pardir)))
from passnake import PasswordStore

class App:
    def __init__(self):
        self.parse()

    def parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--passphrase", help="Passphrase")
        parser.add_argument("-f", "--file", help="Passstore file", default="passnake.gpg")
        subparsers = parser.add_subparsers()
        add = subparsers.add_parser("add", help="Add an entry")
        add.add_argument("path", nargs="*", help="Path to the entry")
        add.add_argument("value", help="Value of the entry")
        add.set_defaults(func=self.add)
        get = subparsers.add_parser("get", help="Get an entry")
        get.add_argument("path", nargs="*", help="Path to the entry")
        get.set_defaults(func=self.get)
        delete = subparsers.add_parser("delete", help="Delete an entry")
        delete.add_argument("path", nargs="*", help="Path to the entry")
        delete.set_defaults(func=self.delete)
        args = parser.parse_args()
        if not hasattr(args, "func"):
            parser.print_help()
            return
        self.store = PasswordStore(args.file)
        if args.passphrase:
            self.passphrase = args.passphrase
        else:
            self.passphrase = getpass("Enter your passphrase: ")
        if not self.verify():
            print("Invalid passphrase")
            return
        args.func(args)

    def verify(self):
        try:
            self.store.load_data(self.passphrase)
        except:
            return False
        return True

    def add(self, args):
        self.store.add_entry(args.path, args.value, self.passphrase)

    def get(self, args):
        print(self.store.get_entry(args.path, self.passphrase))

    def delete(self, args):
        self.store.delete_entry(args.path, self.passphrase)
