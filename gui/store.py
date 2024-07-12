from gpgfile import GPGFile
import json
import os

class PasswordStore(GPGFile):
    def __init__(self, path):
        home = os.getenv("PASSNAKE_HOME")
        if home is None:
            home = os.getcwd()
        super().__init__(os.path.join(home, path))

    def add_entry(self, path, value, passphrase):
        data = self.load_data(passphrase)
        location = data
        for entry in path[:-1]:
            location[entry] = location.get(entry, {})
            location = location.get(entry)
            if location is None:
                return None
        location[path[-1]] = value
        self.save_data(data, passphrase)

    def get_entry(self, path, passphrase):
        data = self.load_data(passphrase)
        for entry in path:
            data = data.get(entry)
            if data is None:
                return None
        return data

    def delete_entry(self, path, passphrase):
        data = self.load_data(passphrase)
        if len(path) != 0:
            location = data
            for entry in path[:-1]:
                location[entry] = location.get(entry, {})
                location = location.get(entry)
                if location is None:
                    return None
            location.pop(path[-1])
        else:
            data = {}
        self.save_data(data, passphrase)
