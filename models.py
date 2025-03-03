import passwordmanager as pm
import os
# Base model
class Model:
    '''
    class to handle the data of the application
    '''
    def __init__(self):
        self.auth_model = AuthModel()
        self.password_model = PasswordModel()

# Authorization model
class AuthModel():
    '''
    class to handle the authentication of the application
    '''
    logged_in = False
    current_user_fullname = None
    current_user = None
    current_id = None
    master_file = os.path.join('master', 'master_passwords.json')
    passwords_file = os.path.join('passwords', 'passwords.json')
    users = None
    user = None
    user_passwords = None
    key = None
    
    def __init__(self):
        super().__init__()
       

    def login(self, username, password):
        # checking if any users exist
        if os.path.exists(AuthModel.master_file) is False:
            return None
        logged_in = pm.login(username, password)
        if logged_in is True:
            AuthModel.logged_in = True
            AuthModel.users = pm.get_json(AuthModel.master_file)
            AuthModel.user = self.users[username]
            AuthModel.current_user_fullname = self.user['full_name']
            AuthModel.current_user = username
            AuthModel.current_id = int(self.user['user_id'])
            passwords = pm.get_json(AuthModel.passwords_file)
            AuthModel.user_passwords = passwords[AuthModel.current_id]
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
        AuthModel.users = None
        AuthModel.user_passwords = None
        AuthModel.key = None

    def signup(self, name, username, password):
        signed_up = pm.signup(name, username, password)

        if signed_up is True:
            AuthModel.users = pm.get_json(AuthModel.master_file)
            AuthModel.logged_in = True
            AuthModel.user = self.users[username]
            AuthModel.current_user_fullname = name
            AuthModel.current_user = username
            AuthModel.current_id = int(self.user['user_id'])
            passwords = pm.get_json(AuthModel.passwords_file)
            AuthModel.user_passwords = passwords[AuthModel.current_id]
            AuthModel.key = pm.get_key(self.user['key_file'])
            return True
        else:
            return False

# Password model
class PasswordModel(AuthModel):
    '''
    class to handle the password data of the application
    '''
    def __init__(self):
        super().__init__()
        self.num_passwords = 0
        self.key = AuthModel.key
        self.passwords = AuthModel.user_passwords

    def add_password(self, website, username, password):
        passwords = pm.add_password(website, username, password, self.key, self.passwords)
        if passwords is None:
            return False
        else:
            self.passwords = passwords
            self.num_passwords += 1
            return True

    def get_password(self, website):
        pm.get_password(website, self.key, self.passwords)

    def change_password(self, website, old_password, new_password, confirm_password):
        changed = pm.change_password(website, old_password, new_password, confirm_password, self.key, self.passwords)
        if changed is None:
            return None
        elif changed is False:
            return False
        else:
            self.passwords = changed
            return True
        
    def get_websites(self):
        if self.passwords is None:
            return []
        else:
            return pm.get_websites(self.passwords)



