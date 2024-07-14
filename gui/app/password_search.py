from gi.repository import Gtk, Gdk

def unique(list):
    list = sorted(list, reverse=True)
    last = object()
    for item in list:
        if item == last:
            continue
        yield item
        last = item

def search(self, term, data=None, path=[]):
    if data is None:
        data = self.fetched_data
    if not isinstance(data, dict):
        return []
    results = []
    for key in data.keys():
        if term.lower() in key.lower() or key.lower() in term.lower():
            results.append(path + [key])
    for key in data.keys():
        results += self.search(term, data[key], path + [key])
    return results

def search_data(self, term):
    self.search_results = self.search(term)
    self.search_results = self.expand_search_results(self.search_results)
    self.search_results = list(unique(self.search_results))
    self.search_results.reverse()
    self.password_search_store.clear()
    for result in self.search_results:
        if len(result) < 2:
            continue
        self.password_search_store.append([str(x) for x in result[-2:]])

def on_password_search(self, widget):
    term = self.password_search_entry.get_text()
    self.search_data(term)

def password_search(self, widget):
    self.password_search_window.show_all()
    self.fetched_data = self.store.get_entry([], self.passphrase)
    self.on_password_search(None)

def on_password_window_key_press(self, widget, event):
    if event.keyval == Gdk.KEY_Escape:
        self.password_search_window.hide()

def expand_search_results(self, results):
    expanded_results = []
    for path in results:
        value = data_get_path(path, self.fetched_data)
        if not isinstance(value, dict):
            expanded_results.append(path)
            continue
        expanded_results += self.expand_search_results([path + [key] for key in value.keys()])
    return expanded_results

def data_get_path(path, data):
    if len(path) == 0 or not isinstance(path, list):
        return data
    return data_get_path(path[1:], data[path[0]])
