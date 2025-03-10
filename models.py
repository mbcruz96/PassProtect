import passwordmanager as pm
import os
# Base model
class Model:
    '''
    class to handle the data of the application
    '''
    def __init__(self):
        # initializing base model
        self.base_model = PasswordModel()

# Authorization model
class AuthModel:
    '''
    class to handle the authentication of the application
    '''
    def __init__(self):
        self.master_file = os.path.join('master', 'master_passwords.json')  # path to registered user data file
        self.passwords_file = os.path.join('passwords', 'passwords.json')   # path to all users passwords file
        self.logged_in = False  # logged in flag
        self.current_user_fullname = None   # current user full name
        self.current_user = None    # current user username
        self.current_id = None  # current user id
        self.users = None   # all user data from registered users data file
        self.user = None    # current user entry from registered users data file
        self.all_passwords = None   # all password entries for all users from password file
        self.current_user_passwords = None  # current user entry from password file
        self.key = None # current user key
    
    def login(self, username, password):
        # checking if any users exist
        if os.path.exists(self.master_file) is False:
            return None
        logged_in = pm.login(username, password)
        # initializing data for current user
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
        # login attempt failed
        else:
            self.logged_in = False
            self.current_user_fullname = None
            self.current_user = None
        return logged_in

    def logout(self):
        # removing data for current user
        self.logged_in = False
        self.current_user_fullname = None
        self.current_user = None
        self.current_id = None
        self.user = None
        self.users = None
        self.current_user_passwords = None
        self.key = None

    def signup(self, name, username, password):
        # signing up current user
        signed_up = pm.signup(name, username, password)

        if signed_up is True:
            # initializing data for signed up user
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
        # signup attemp failed
        else:
            return False

# Password model
class PasswordModel(AuthModel):
    '''
    class to handle the password data of the application
    '''
    def __init__(self):
        super().__init__()
        self.num_passwords = 0  # number of stored password for current user
    
    def add_password(self, website, username, password, url):
        # adding a password for the current user
        passwords = pm.add_password(website, username, password, url, self.current_id, self.key, self.current_user_passwords)
        # password not added block
        if passwords is None:
            return False
        # password successfully added block
        else:
            # updating password data for current user
            self.all_passwords = pm.get_json(self.passwords_file)
            self.current_user_passwords = self.all_passwords[self.current_id]
            self.num_passwords += 1
            return True

    def import_passwords(self, file_path):
        # importing CSV of password data
        self.passwords = pm.import_passwords(file_path, self.current_id, self.key, self.current_user_passwords)
        
    def get_password(self, website):
        # retrieving password for specified website
        pm.get_password(website, self.key, self.current_user_passwords)

    def get_username(self, website):
        # retrieving username for specified website
        pm.get_username(website, self.key, self.current_user_passwords)

    def change_password(self, website, old_password, new_password, confirm_password):
        # changing password for specified website
        changed = pm.change_password(website, old_password, new_password, confirm_password, self.current_id, self.key, self.current_user_passwords)
        # previous password incorrect block
        if changed is None:
            return None
        # new passwords do not match block
        elif changed is False:
            return False
        # password successfully changed block
        else:
            self.passwords = changed
            return True
        
    def remove_password(self, website):
        # removing website from list of managed passwords
        removed = pm.remove_password(website, self.current_id, self.current_user_passwords)
        # website not found in passwords file block
        if removed is False:
            return False
        # website successfully removed block
        else:
            self.current_user_passwords = removed
            return True

    def get_websites(self):
        # retrieving list of all stored websites for current user
        return pm.get_websites(self.current_user_passwords)
    
    def open_url(self, website):
        # opening url for specified user in web browser
        return pm.open_url(website, self.current_user_passwords)



