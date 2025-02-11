import passwordmanager as pm
import tkinter as tk
import views
from views import SignUpView, LoginView, HomeView
import models

class Controller:
    def __init__(self, model:models.Model, view:views.View):
        self.view = view
        self.model = model
        self.signup_controller = SignupController(model, view)
        self.login_controller = LoginController(model, view)
        self.home_controller = HomeController(model, view)

        self.model.auth_model.add_listener('on_login', self.on_login)
        self.model.auth_model.add_listener('on_logout', self.on_logout)
    
    def on_login(self):
        self.view.switch('home')

    def on_logout(self):
        self.view.switch('login')

    def start(self):
        self.view.switch('login')
        self.view.start_loop()

class LoginController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = view.frames['login']
        self._bind()

    def _bind(self):
        self.frame.children['!button'].config(command=self.login)
        self.frame.children['!button2'].config(command=self.signup)
        
    
    def signup(self):
        self.view.switch('signup')

    def login(self):
        username = self.frame.username.get()
        password = self.frame.password.get()
        login = self.model.auth_model.login(username, password)
        if login is True:
            self.view.switch('home')
        elif login is False:
            self.frame.children['!label5'].grid(row=4, column=1, padx=0, pady=10, sticky='w')
        else:
            self.frame.children['!label6'].grid(row=4, column=1, padx=0, pady=10, sticky='w')

class SignupController:
    def __init__(self, model:models.Model, view:views.View):
        self.model = model
        self.view = view
        self.frame = view.frames['signup']
        self._bind()
    # FINISH THE BIND METHOD AND CALLBACK FUNCTIONS

    def _bind(self):
        self.frame.children['!button'].config(command=self.signup)
    
    def signup(self):
        name = self.frame.fullname.get()
        username = self.frame.username.get()
        password = self.frame.password.get()
        agreed = self.frame.agreed

        if agreed:
            signup = self.model.auth_model.signup(name, username, password)
            if signup is True:
                self.view.switch('home')
            else:
                self.frame.children['!label5'].grid(row=6, column=1, padx=0, pady=10, sticky='w')
        else:
            self.frame.children['!label6'].grid(row=6, column=1, padx=0, pady=10, sticky='w')


class HomeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames['home']
        '''self._bind()

    def _bind(self):
        self.frame.select_btn.config(command=self.select)
    '''
    def select(self):
        # FINISH THE CALLBACK FUNCTION
        index = self.frame.listbox.curselection()
        item = self.frame.listbox.get(index[0])
    
    def logout(self):
        self.model.auth_model.logout()
        self.view.switch('login')
