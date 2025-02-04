from flask import Flask, redirect, url_for, request, render_template
import sqlite3
import json 
import tkinter
import hashlib
import pyperclip
import sys
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
    2. encrypt password with the initialized key currently open in session
    3. save website, username, and encrypted password in passwords json file

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
    key = Fernet.generate_key()
    return key

def initialize_key(key):
    f = Fernet(key)
    return f 

def encrypt_pass(password, key):
    enc_message = key.encrypt(password.encode()).decode()
    return enc_message

def decrypt_pass(password, key):
    dec_message = key.decrypt(password).decode()
    return dec_message

#def add_password(username, password)

key = generate_key()
print("The key is: ")
print(key)

key = initialize_key(key)
print("Initialized key: ")
print(key)

message = 'suck my dick'
print('Message: ' + message)

enc_message = encrypt_pass(message, key)
print('Encrypted message: ')
print(enc_message)

dec_message = decrypt_pass(enc_message, key)
print('Decrypted message: ')
print(dec_message)
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