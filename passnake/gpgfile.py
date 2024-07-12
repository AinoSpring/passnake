import gnupg
import json
import os

class GPGFile:
    def __init__(self, path):
        self.gpg = gnupg.GPG()
        self.path = path

    def load_data(self, passphrase):
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = self.gpg.decrypt(encrypted_data, passphrase=passphrase)
        if decrypted_data.ok:
            data = decrypted_data.data.decode("utf-8")
            return json.loads(data)
        else:
            raise Exception(f"Decryption failed: {decrypted_data.stderr}")

    def save_data(self, data, passphrase):
        data = json.dumps(data)
        encrypted_data = self.gpg.encrypt(data, None, symmetric=True, passphrase=passphrase)
        if encrypted_data.ok:
            with open(self.path, "wb") as f:
                f.write(encrypted_data.data)
        else:
            raise Exception(f"Encryption failed: {encrypted_data.stderr}")
