from flask import Flask, redirect, url_for, request, render_template
import json 
import pandas as pd
import hashlib
import pyperclip
import os
from cryptography.fernet import Fernet
'''
Password manager algorithm
- user login
    - if user already registered
        1. user inputs username a password 
        2. password is hashed with sha256
        3. hashed password is checked to see if it matches stored hashed password
        4. username is checked to see if it matches stored username 
        5. if both match, then user authenticated
        6. else display error message (3x max)

    - if user is not registered
        1. user enters new (possibly unique) username and password
        2. password is hashed using sha256
        3. username and hashed password stored in user data json file

- get user key
    1. check to see if there is a stored password in key.key file
        1. if key file does not exist (first time using program): generate the key, create the key.key
            file and save the uninitialized generated key
        2. if key file does exist: open the key.key file and extract the key 
    2. initialize the key

- add password
    1. user enters website name, username, and password to be stored
    2. check if the website exists in password json file 
        - if it does not exists: 
            1. encrypt password with the initialized key currently open in session
            2. save website, username, and encrypted password in passwords json file
        - if it does exist:
            1. print warning message that there is a password already stored for the website
    

- get password
    1. user enters the website name for the password
    2. open password json file
    3. check if the website exists in password json file 
        1. if it exists: decrypt the password using initialized key and copy to user clipboard
        2. if it does not exist: print warning message that no password is stored for the website
            
- change password
    1. user enters the website they wish to change the password to 
    2. check if the website exists in password json file
        - if it exists: 
            1. user enters username and new password for the website
            2. encrypt the new password with initialized key
            3. change the password for the website entry in the password json file
        - if it does not exist
            1. print warning message that no password is stored for the website
            

- delete password
     1. user enters the website they wish to delete the password for
     2. check if the website exists in password json file
        - if it exists: 
            1. print warning message asking if the user is sure they want to deleter
            2. delete website entry if user confirms
            3. leave entry if user does not confirm
        - if it does not exist
            1. print warning message that no password is stored for the website
'''

def generate_key():
    # generating a key for the first time
    key = Fernet.generate_key()
    return key

def hash_password(password : str):
    # hash master password
    hash = hashlib.sha256()
    hash.update(password.encode())
    return hash.hexdigest()
    
def initialize_key(key : bytes):
    # initializing key as cipher
    f = Fernet(key)
    return f 

def encrypt_password(password : str, key : Fernet) -> str:
    # encrypting password using initialized cipher and decoding encrypted message to plaintext
    enc_message = key.encrypt(password.encode()).decode()
    return enc_message

def decrypt_password(password : str, key : Fernet) -> str:
    # decrypting password using initialized cipher and decoding decrypted message to plaintext
    dec_message = key.decrypt(password).decode()
    return dec_message

def get_json(filename : str) -> dict:
    # checking if passwords json file already exists
    # if file does not exist, initialize empty password dictionary
    if not os.path.exists(filename):
        passwords = {}
        with open(filename, 'w') as file:
            json.dump(passwords, file)
    # if file already exists, open json file and load passwords dictionary
    else:
        try:
            with open(filename, 'r') as file:
                passwords = json.load(file)
        # exception for if json file not found
        except json.JSONDecodeError:
            passwords = {}
    return passwords

def write_json(filename : str, data : dict):
    # writing data to json file
    with open(filename, 'w') as file:
        json.dump(data, file)

def update_passwords(user_id: int, updated_passwords: dict):
    # getting full password file
    passwords_file = os.path.join('passwords', 'passwords.json')
    user_passwords = get_json(passwords_file)
    # saving new entry in full password file
    user_passwords[user_id] = updated_passwords
    write_json(passwords_file, user_passwords)

def get_key(file_path : str):
    '''
    Function checks if a key encryption file exists, if so it returns the key stored 
    in the file, if not, it generates a new key and stores it in the file key.key
    '''
    try:
        # reading key from key.key file
        with open(file_path, 'rb') as key_file:
            key = key_file.read()
        cipher = initialize_key(key)
        return cipher
    except FileNotFoundError:
        print('Key file can not be found')
    # initializing and returning encryption cipher
    
def add_password(website : str, username : str, password : str, user_id: int, key : Fernet, passwords : dict):
    '''
    - function adds a password to a dictionary of managed passwords
    - dictionary format passwords[user][website] = {'username': username, 'password': encrypted_password}
    '''
    site = website.lower().strip()
    '''
    # checking if user has an entry in the passwords file or not
    if user not in passwords.keys():
        passwords[user] = {}
    '''

    # checking if website entry already exists in password keys
    # if entry already exists in dictionary print warning message
    if site in passwords.keys():
        return None
    # if entry does not exist    
    else:
        # encrypting password
        enc_password = encrypt_password(password, key)
        # storing username and password to dictionary with lowercased website as key
        entry = {
            'username' : username,
            'password' : enc_password,
            'website' : website
        }
        
        # saving new entry in user's passwords
        passwords[site] = entry

        # getting full password file
        update_passwords(user_id, passwords)

    return passwords

def import_passwords(file_path: str, user_id : int, key : Fernet, passwords: dict):
    '''
    Function imports passwords from a csv file and adds them to the user's password file
    '''
    # reading csv file
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # filling empty entries with 0
        df = df.fillna(0)

    # iterating over dataframe rows
    for index, row in df.iterrows():
        website = row['Name'].lower().strip()
        if row['Password'] != 0:
            password = encrypt_password(row['Password'], key)
        else:
            continue
        
        # creating password entry
        data = {
            'username' : row['Username'],
            'password' : password,
            'website' : row['Name'],
            'url' : row['Website'],
            'description' : row['Name'],
            'type' : row['Type'],
        }
        # saving entry in passwords dictionary
        passwords[website] = data

    # updating password file
    update_passwords(user_id, passwords)
    return passwords
    
def get_password(website : str, key : Fernet, passwords : dict):
    site = website.lower().strip()

    if site in passwords.keys():
        enc_password = passwords[site]['password']
        dec_password = decrypt_password(enc_password, key)
        pyperclip.copy(dec_password)
        print('Password saved to clipboard')
    else:
        print('A password does not exist for the given website')

def get_username(website: str, key : Fernet, passwords: dict):
    site = website.lower().strip()

    if site in passwords.keys():
        username = passwords[site]['username']
        pyperclip.copy(username)
        print('username copied')

def get_websites(passwords : dict):
    websites = []
    if len(passwords) == 0:
        return websites
    for website in passwords.keys():
        websites.append(passwords[website]['website'])
    return websites

def change_password(website : str, old_password : str, new_password : str, confirm_password : str, user_id : int, key : Fernet, passwords: dict):
    website = website.lower().strip()
    enc_password = passwords[website]['password']
    dec_password = decrypt_password(enc_password, key)
    if dec_password == old_password:
        if new_password == confirm_password:
            enc_new_password = encrypt_password(new_password, key)
            passwords[website]['password'] = enc_new_password
            
            # updating password file
            update_passwords(user_id, passwords)
        else:
            return False
    else:
        return None
    
    return passwords
    
def remove_password(website : str, user_id : int,  passwords : dict):
    website = website.lower().strip()
    try:
        del passwords[website]
        # updating password file
        update_passwords(user_id, passwords)

        return passwords
    except KeyError:
        return False
    
def login(username: str, password: str):
    '''
    Function accepts the username and password and authenticates a login attempt.
    '''
    master_file = os.path.join('master', 'master_passwords.json')
    stored_users = get_json(master_file)
    if len(stored_users) == 0:
        return None
    else:
        hashed_password = hash_password(password)
        if username in stored_users.keys():
            user = stored_users[username]
            if hashed_password == user['password']: 
                return True
            else:
                return False
        else:
            return False

def signup(fullname : str, username : str, password : str):
    '''
    Function allows a user to signup for the password manager. The username must be
    unique and the function returns true if the signup was successful and false 
    otherwise. 
    '''

    # building master passwords and user passwords file paths
    passwords_file = os.path.join('passwords', 'passwords.json')
    master_file = os.path.join('master', 'master_passwords.json')

    # retrieving or creating master password file
    if os.path.exists(master_file):
        stored_users = get_json(master_file) # retrieving currently stored users
    else:
        stored_users = {}

    # checking if the username is unique
    if username not in stored_users.keys():
        user_id = len(stored_users) # generating a user id
        hashed_password = hash_password(password)   # hashing the chosen password
        passwords = list()  # list to store all users passwords

        # building key file name for user
        key_dir = 'keys'
        key_filename = f'encryption_key_{user_id}.key'
        key_file = os.path.join(key_dir, key_filename)
        
        # creating user data for master passwords file
        user_data = {
            'user_id' : user_id, 
            'full_name' : fullname, 
            'password' : hashed_password,
            'key_file' : key_file, 
            } 
        # adding user to the list of known users
        stored_users[username] = user_data

        # making key directory if it doesn't exist
        if not os.path.exists(key_dir):
            os.makedirs(key_dir)
        # generating a key to encrypt passwords for this user
        key = generate_key()
        # writing key file for 
        with open(key_file, 'wb') as file:
            file.write(key)

        # making password directory if it doesn't exist
        if not os.path.exists('passwords'):
            os.makedirs("passwords")
        else:
            if os.path.exists(passwords_file):
                passwords = get_json(passwords_file)
        # adding new passwords entry for user
        passwords.append(dict())
        write_json(passwords_file, passwords)

        # making master password directory if it doesn't exist
        if not os.path.exists('master'):
            os.makedirs('master')
        # writing new dict of known users
        write_json(master_file, stored_users)

        return True
    else:
        return False
    
'''
app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__=="__main__":
    app.run()
'''