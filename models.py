import passwordmanager as pm

class BaseModel:
    def __init__(self):
        self.event_listeners = {}

    def add_listener(self, event, callback):
        try:
            self.event_listeners[event].append(callback)
        except KeyError:
            self.event_listeners[event] = callback

    def trigger_event(self, event):
        if event not in self.event_listeners.keys():
            return
        for callback in self.event_listeners[event]:
            callback(self)

class Model:
    def __init__(self):
        self.auth_model = AuthModel()
        self.password_model = PasswordModel()

class AuthModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.logged_in = False
        self.current_user = None
        self.users = pm.get_json_file('master_passwords.json')

    def login(self, username, password):
        logged_in = pm.login(username, password)
        if logged_in is True:
            self.logged_in = True
            self.current_user = self.users[username]['full_name']
            self.trigger_event('on_login')
        else:
            self.logged_in = False
            self.current_user = None
        return logged_in

    def logout(self):
        self.logged_in = False
        self.current_user = None
        self.trigger_event('on_logout')

    def signup(self, name, username, password):
        signed_up = pm.signup(name, username, password)
        if signed_up is True:
            self.users = pm.get_json_file('master_passwords.json')
            self.logged_in = True
            self.current_user = self.users[username]['full_name']
            self.trigger_event('on_login')
            return True
        else:
            return False

class PasswordModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.passwords = pm.get_json_file('passwords.json')
        self.key = pm.get_key_file()
        self.num_passwords = len(self.passwords)

    def add_password(self, website, username, password):
        self.passwords = pm.add_password(website, username, password, self.key, self.passwords)
        self.num_passwords += 1
        self.trigger_event('add_password')

    def get_password(self, website):
        pm.get_password(website, self.key, self.passwords)
        self.trigger_event('get_password')

