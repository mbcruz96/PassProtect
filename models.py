import passwordmanager as pm
import os
# Base model
class Model:
    '''
    class to handle the data of the application
    '''
    def __init__(self):
        self.base_model = PasswordModel()

# Authorization model
class AuthModel:
    '''
    class to handle the authentication of the application
    '''
    def __init__(self):
        self.master_file = os.path.join('master', 'master_passwords.json')
        self.passwords_file = os.path.join('passwords', 'passwords.json')
        self.logged_in = False
        self.current_user_fullname = None
        self.current_user = None
        self.current_id = None
        self.users = None
        self.user = None
        self.all_passwords = None
        self.current_user_passwords = None
        self.key = None
    
    def login(self, username, password):
        # checking if any users exist
        if os.path.exists(self.master_file) is False:
            return None
        logged_in = pm.login(username, password)
        if logged_in is True:
            self.logged_in = True
            self.users = pm.get_json(self.master_file)
            self.user = self.users[username]
            self.current_user_fullname = self.user['full_name']
            self.current_user = username
            self.current_id = self.user['user_id']
            self.all_passwords = pm.get_json(self.passwords_file)
            self.current_user_passwords = self.all_passwords[self.current_id]
            self.key = pm.get_key(self.user['key_file'])
        else:
            self.logged_in = False
            self.current_user_fullname = None
            self.current_user = None
        return logged_in

    def logout(self):
        self.logged_in = False
        self.current_user_fullname = None
        self.current_user = None
        self.current_id = None
        self.user = None
        self.users = None
        self.current_user_passwords = None
        self.key = None

    def signup(self, name, username, password):
        signed_up = pm.signup(name, username, password)

        if signed_up is True:
            self.users = pm.get_json(self.master_file)
            self.logged_in = True
            self.user = self.users[username]
            self.current_user_fullname = name
            self.current_user = username
            self.current_id = self.user['user_id']
            self.all_passwords = pm.get_json(self.passwords_file)
            self.current_user_passwords = self.all_passwords[self.current_id]
            self.key = pm.get_key(self.user['key_file'])
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
    
    def add_password(self, website, username, password, url):
        passwords = pm.add_password(website, username, password, url, self.current_id, self.key, self.current_user_passwords)
        if passwords is None:
            return False
        else:
            self.current_user_passwords = passwords
            self.all_passwords[self.current_id] = self.current_user_passwords
            pm.write_json(self.passwords_file, self.all_passwords)
            self.num_passwords += 1
            return True

    def import_passwords(self, file_path):
        self.passwords = pm.import_passwords(file_path, self.current_id, self.key, self.current_user_passwords)
        
    def get_password(self, website):
        pm.get_password(website, self.key, self.current_user_passwords)

    def get_username(self, website):
        pm.get_username(website, self.key, self.current_user_passwords)

    def change_password(self, website, old_password, new_password, confirm_password):
        changed = pm.change_password(website, old_password, new_password, confirm_password, self.current_id, self.key, self.current_user_passwords)
        if changed is None:
            return None
        elif changed is False:
            return False
        else:
            self.passwords = changed
            return True
        
    def remove_password(self, website):
        removed = pm.remove_password(website, self.current_id, self.current_user_passwords)
        if removed is False:
            return False
        else:
            self.current_user_passwords = removed
            return True

    def get_websites(self):
        return pm.get_websites(self.current_user_passwords)
    
    def open_url(self, website):
        return pm.open_url(website, self.current_user_passwords)



