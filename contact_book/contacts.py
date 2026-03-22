import json
import os


class ContactBook:
    def __init__(self, filepath):
        self.filepath = filepath
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.contacts = json.load(f)
        else:
            self.contacts = []
            self._save()

    def add_contact(self, name, phone, email):
        self.contacts.append({"name": name, "phone": phone, "email": email})
        self._save()

    def list_contacts(self):
        return self.contacts

    def search_contact(self, name):
        query = name.lower()
        return [c for c in self.contacts if query in c["name"].lower()]

    def delete_contact(self, name):
        query = name.lower()
        self.contacts = [c for c in self.contacts if query not in c["name"].lower()]
        self._save()

    def _save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.contacts, f, indent=2)
