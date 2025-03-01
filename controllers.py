import passwordmanager as pm
import tkinter as tk
import views
from views import EventListener
import models

class Controller:
    def __init__(self, model:models.Model, view:views.View):
        self.frame = None
        self.view = view
        self.model = model

        # initializing controllers
        self.signup_controller = SignupController(model, view)
        self.login_controller = LoginController(model, view)
        self.home_controller = HomeController(model, view)
        self.add_controller = AddController(model, view)

        # adding all event listeners
        EventListener.add_listener('on_login', self.on_login)
        EventListener.add_listener('on_logout', self.on_logout)
        EventListener.add_listener('to_signup', self.to_signup)
        EventListener.add_listener('on_signup', self.on_signup)
        EventListener.add_listener('to_add', self.to_add)
        EventListener.add_listener('add_password', self.add_password)
        EventListener.add_listener('on_back', self.on_back)

    def on_login(self, frame, args):
        self.login_controller.login(frame, args)

    def on_logout(self, frame, args):
        self.home_controller.logout(frame, args)

    def to_signup(self, frame, args):
        self.login_controller.signup(frame, args)
    
    def on_signup(self, frame, args):
        self.signup_controller.signup(frame, args)

    def to_add(self, frame, args):
        self.home_controller.add(frame, args)

    def add_password(self, frame, args):
        self.add_controller.add(frame, args)

    def on_back(self, frame, args):
        self.add_controller.back(frame, args)

    def start(self):
        self.view.switch('login')
        self.view.start_loop()

# controller for login view
class LoginController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        #self.frame = view.frames['login']
    
    def signup(self, frame, args):
        self.view.switch('signup')

    def login(self, frame, args):
        frame.children['!label5'].grid_forget()
        frame.children['!label6'].grid_forget()
        username = frame.username.get()
        password = frame.password.get()
        login = self.model.auth_model.login(username, password)
        if login is False:
            frame.children['!label5'].grid(row=6, column=1, padx=0, pady=10, sticky='w')
        elif login is None:
            frame.children['!label6'].grid(row=6, column=1, padx=0, pady=10, sticky='w')
        else:
           frame.children['!entry'].delete(0, tk.END)
           frame.children['!entry2'].delete(0, tk.END)
           self.view.switch('home')

# controller for signup view
class SignupController:
    def __init__(self, model:models.Model, view:views.View):
        self.model = model
        self.view = view
        #self.frame = view.frames['signup']
      
    def signup(self, frame, args):
        frame.children['!label5'].grid_forget()
        frame.children['!label6'].grid_forget()
        name = frame.fullname.get()
        username = frame.username.get()
        password = frame.password.get()
        agreed = frame.agreed.get()

        if agreed is True:
            signup = self.model.auth_model.signup(name, username, password)
            if signup is False:
                self.frame.children['!label5'].grid(row=6, column=1, padx=0, pady=10, sticky='w')
            else:
                self.view.switch('home')
        else:
            self.frame.children['!label6'].grid(row=6, column=1, padx=0, pady=10, sticky='w')

# controller for home view
class HomeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        #self.frame = self.view.frames['home']
      
    def select(self, frame, args):
        # FINISH THE CALLBACK FUNCTION
        index = frame.children['!listbox'].curselection()
        item = frame.children['!listbox'].get(index[0])

    def add(self, frame, args):
        self.view.switch('add')

    def logout(self, frame, args):
        self.view.switch('login')

# controller for add password view
class AddController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        #self.frame = self.view.frames['add']
     
    def add(self, frame, args):
        frame.children['!label5'].grid_forget()
        username = frame.username.get()
        password = frame.password.get()
        website = frame.website.get()
        password_added = self.model.password_model.add_password(website, username, password)
        
        if password_added is False:
            frame.children['!label5'].pack()
        else:
            frame.children['!entry'].delete(0, tk.END)
            frame.children['!entry2'].delete(0, tk.END)
            frame.children['!entry3'].delete(0, tk.END)
            self.view.switch('home')

    def back(self, frame, args):
        frame.children['!entry'].delete(0, tk.END)
        frame.children['!entry2'].delete(0, tk.END)
        frame.children['!entry3'].delete(0, tk.END)
        self.view.switch('home')