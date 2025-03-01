import views
from views import SignUpView
import tkinter as tk
import passwordmanager as pm
from views import EventListener
#view = views.View()
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

EventListener.trigger_event('on_signup', None, None)
event='to_signup', frame=self, args=[]