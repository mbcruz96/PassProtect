from flask import Flask, redirect, url_for, request, render_template
import json 
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

def hash_password(password):
    # hash master password
    hash = hashlib.sha3_256()
    hash.update(password.encode)
    return hash.hexdigest()
    
def initialize_key(key):
    # initializing key as cipher
    f = Fernet(key)
    return f 

def encrypt_password(password, key) -> str:
    # encrypting password using initialized cipher and decoding encrypted message to plaintext
    enc_message = key.encrypt(password.encode()).decode()
    return enc_message

def decrypt_password(password, key) -> str:
    # decrypting password using initialized cipher and decoding decrypted message to plaintext
    dec_message = key.decrypt(password).decode()
    return dec_message

def get_json_file(filename) -> dict:
    # checking if passwords json file already exists
    # if file does not exist, initialize empty password dictionary
    if not os.path.exists(filename):
        passwords = {}
        with open(filename, 'w') as file:
            file.dump(passwords)
    # if file already exists, open json file and load passwords dictionary
    else:
        try:
            with open(filename, 'r') as file:
                passwords = json.load(file)
        # exception for if json file not found
        except json.JSONDecodeError:
            passwords = {}
    return passwords

def get_key_file():
    filename = 'encryption_key.key'
    if not os.path.exists('encryption_key.key'):
        key = generate_key()
        with open(filename, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(filename, 'rb') as key_file:
            key = key_file.read()
    cipher = initialize_key(key)
    return cipher

def add_password(website, username, password, key, passwords):
    '''
    - function adds a password to a dictionary of managed passwords
    - dictionary format passwords[website] = {'username': username, 'password': encrypted_password}
    '''

    # checking if website entry already exists in password keys
    # if entry does not exist
    if website not in passwords.keys():
        # encrypting password
        enc_password = encrypt_password(password, key)
        # storing username and password to dictionary with lowercased website as key
        passwords[website.to_lower()] = {'username': username, 'password': enc_password}
        print('Saved password successfully')
    # if entry already exists in dictionary print warning message
    else:
        print('A password already exists for this website')
    return passwords

def get_password(website, key, passwords):
    if website in passwords.keys():
        enc_password = passwords[website.to_lower()]['password']
        dec_password = decrypt_password(enc_password, key)
        pyperclip.copy(dec_password)
        print('Password saved to clipboard')
    else:
        print('A password does not exist for the given website')

def login(username, password):
    '''
    Function accepts the username and password and authenticates a login attempt.
    '''
    stored_users = get_json_file('master_passwords')
    if len(stored_users) == 0:
        return None
    else:
        hashed_password = hash_password(password)
        if username in stored_users.keys():
            if hashed_password == stored_users[username][password]: 
                return True
            else:
                return False
        else:
            return False

def signup(fullname, username, password):
    stored_users = get_json_file('master_passwords')
    hashed_password = hash_password(password)
    data = {'full_name': fullname, 'password': hashed_password}
    if username not in stored_users.keys():
        stored_users[username] = data
        key = generate_key()
        with open('master_passwords.json', 'w') as file:
            file.dump(data)
        with open('encryption_key.key', 'wb') as key_file:
            key_file.write(key)
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