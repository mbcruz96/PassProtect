import passwordmanager as pm

class Model:
    def __init__(self):
        self.auth_model = AuthModel()
        self.password_model = PasswordModel()

class AuthModel():
    logged_in = False
    current_user_fullname = None
    current_user = None
    current_id = 0
    users = pm.get_json('master_passwords.json')
    user = None
    key = None
    
    def __init__(self):
        super().__init__()
       

    def login(self, username, password):
        logged_in = pm.login(username, password)
        if logged_in is True:
            AuthModel.logged_in = True
            AuthModel.user = self.users[username]
            AuthModel.current_user_fullname = self.user['full_name']
            AuthModel.current_user = username
            AuthModel.current_id = self.user['user_id']
            AuthModel.key = pm.get_key(self.user['key_file'])
        else:
            AuthModel.logged_in = False
            AuthModel.current_user_fullname = None
            AuthModel.current_user = None
        return logged_in

    def logout(self):
        AuthModel.logged_in = False
        AuthModel.current_user_fullname = None
        AuthModel.current_user = None
        AuthModel.current_id = 0
        AuthModel.user = None
        AuthModel.key = None

    def signup(self, name, username, password):
        signed_up = pm.signup(name, username, password)

        if signed_up is True:
            AuthModel.users = pm.get_json('master_passwords.json')
            AuthModel.logged_in = True
            AuthModel.user = self.users[username]
            AuthModel.current_user_fullname = name
            AuthModel.current_user = username
            AuthModel.current_id = self.user['user_id']
            AuthModel.key = pm.get_key(self.user['key_file'])
            return True
        else:
            return False

class PasswordModel(AuthModel):
    def __init__(self):
        super().__init__()
        self.passwords = pm.get_json('passwords.json')
        self.num_passwords = len(self.passwords)

    def add_password(self, website, username, password):
        passwords = pm.add_password(website, username, password, AuthModel.current_user, AuthModel.key, self.passwords)
        if passwords is None:
            return False
        else:
            self.passwords = passwords
            self.num_passwords += 1
            return True

    def get_password(self, website):
        pm.get_password(website, self.key, self.passwords)



