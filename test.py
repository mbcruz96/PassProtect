import views
from views import SignUpView
import tkinter as tk
import passwordmanager as pm
from views import EventListener
import os

master_file = os.path.join('master', 'master_passwords.json')
password_file = os.path.join('passwords', 'passwords.json')
users = pm.get_json(master_file)
passwords = pm.get_json(password_file)
print(type(users['a']['user_id']))
print(type(passwords[users['a']['user_id']])) 