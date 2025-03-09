import views
from views import SignUpView
import tkinter as tk
import passwordmanager as pm
from views import EventListener
import os

#master_file = os.path.join('master', 'master_passwords.json')
#password_file = os.path.join('passwords', 'passwords.json')
#users = pm.get_json(master_file)
#passwords = pm.get_json(password_file)
#print(type(users['a']['user_id']))
#print(type(passwords[users['a']['user_id']])) 
#view = views.View()
#frame = view.switch('signup', None)
#print(frame.children)
#label = tk.Label()
#frame = view.frames['signup']
#for name, widget in frame.children.items():
    #print(f"Widget Name: {name}, Widget Type: {type(widget)}")
#print(SignUpView.children)
#print(frame.__dict__)
#print(type(frame.children['!button']))
#view.switch('signup')
#view.start_loop()
#users = pm.get_json('master_passwords.json')
#print(users['a']['key_file'])
#key = pm.get_key(users['a']['key_file'])
#print(type(key))

#EventListener.trigger_event('on_signup', None, None)
#event='to_signup', frame=self, args=[]
strng = 'https://google.com'
index = strng.find('//')
strng = strng[index+2:]
index = strng.find('.')
print(strng[:index])