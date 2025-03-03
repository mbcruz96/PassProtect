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
        self.website = None

        # initializing controllers
        self.signup_controller = SignupController(model, view)
        self.login_controller = LoginController(model, view)
        self.home_controller = HomeController(model, view)
        self.add_controller = AddController(model, view)

        # creating event listeners
        EventListener.add_listener('on_login', self.on_login)
        EventListener.add_listener('on_logout', self.on_logout)
        EventListener.add_listener('to_signup', self.to_signup)
        EventListener.add_listener('on_signup', self.on_signup)
        EventListener.add_listener('to_add', self.to_add)
        EventListener.add_listener('add_password', self.add_password)
        EventListener.add_listener('to_change', self.to_change)
        EventListener.add_listener('on_change', self.on_change)
        EventListener.add_listener('on_back', self.on_back)

    # binding event listeners to their respective functions
    def on_login(self, frame):
        self.frame = self.login_controller.login(frame)

    def on_logout(self, frame):
        self.frame = self.home_controller.logout(frame)

    def to_signup(self, frame):
        self.frame = self.login_controller.signup(frame)
    
    def on_signup(self, frame):
        self.frame = self.signup_controller.signup(frame)

    def to_add(self, frame):
        self.frame = self.home_controller.add(frame)

    def add_password(self, frame):
        self.frame = self.add_controller.add(frame)

    def to_change(self, frame):
        self.frame, self.website = self.home_controller.change(frame)
                                                 
    def on_change(self, frame):
        self.frame = self.home_controller.change(frame, self.website)
        self.website = None

    def on_back(self, frame):
        self. frame = self.add_controller.back(frame)

    # starting the application
    def start(self):
        self.frame = self.view.switch('login')
        self.view.start_loop()

# controller for login view
class LoginController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def signup(self, frame):
        new_frame = self.view.switch('signup')
        return new_frame
    
    def login(self, frame):
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
           websites = self.model.password_model.get_websites()
           new_frame = self.view.switch('home')
           for website in websites:
               new_frame.children['!listbox'].insert(tk.END, website.title())
           return new_frame
        return frame

# controller for signup view
class SignupController:
    def __init__(self, model:models.Model, view:views.View):
        self.model = model
        self.view = view
      
    def signup(self, frame):
        print(frame.children)
        frame.children['!label5'].grid_forget()
        frame.children['!label6'].grid_forget()
        name = frame.fullname.get()
        username = frame.username.get()
        password = frame.password.get()
        agreed = frame.agreed.get()

        if agreed is True:
            signup = self.model.auth_model.signup(name, username, password)
            if signup is False:
                frame.children['!label5'].grid(row=6, column=1, padx=0, pady=10, sticky='w')
            else:
                websites = self.model.password_model.get_websites()
                new_frame = self.view.switch('home')
                for website in websites:
                    new_frame.children['!listbox'].insert(tk.END, website.title())
                return new_frame
        else:
            frame.children['!label6'].grid(row=6, column=1, padx=0, pady=10, sticky='w')
        return frame
    
# controller for home view
class HomeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
      
    def select(self, frame):
        # FINISH THE CALLBACK FUNCTION
        index = frame.children['!listbox'].curselection()
        item = frame.children['!listbox'].get(index[0])

    def change(self, frame):
        new_frame = self.view.switch('change')
        return new_frame
    
    def add(self, frame):
        new_frame = self.view.switch('add')
        return new_frame
    
    def logout(self, frame):
        new_frame = self.view.switch('login')
        return new_frame
    
# controller for add password view
class AddController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
     
    def add(self, frame):
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
            websites = self.model.password_model.get_websites()
            new_frame = self.view.switch('home')
            for website in websites:
               new_frame.children['!listbox'].insert(tk.END, website.title())
            return new_frame
        return frame

    def change(self, frame):
        website = frame.children['!listbox'].get(tk.ACTIVE)
        self.switch('change')
        return(frame, website)

    def back(self, frame):
        frame.children['!entry'].delete(0, tk.END)
        frame.children['!entry2'].delete(0, tk.END)
        frame.children['!entry3'].delete(0, tk.END)
        websites = self.model.password_model.get_websites()
        new_frame = self.view.switch('home')
        for website in websites:
            new_frame.children['!listbox'].insert(tk.END, website.title())
        return new_frame
    
class ChangeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def change(self, frame, website):
        frame.children['!label5'].grid_forget()
        frame.children['!label6'].grid_forget()
        username = frame.old_password.get()
        password = frame.new_password.get()
        website = frame.confirm_password.get()
        password_changed = self.model.password_model.add_password(website, username, password)
        
        if password_changed is False:
            frame.children['!label5'].pack()
        elif password_changed is None:
            frame.children['!label6'].pack()
        else:
            frame.children['!entry'].delete(0, tk.END)
            frame.children['!entry2'].delete(0, tk.END)
            frame.children['!entry3'].delete(0, tk.END)
            websites = self.model.password_model.get_websites()
            new_frame = self.view.switch('home')
            for website in websites:
               new_frame.children['!listbox'].insert(tk.END, website.title())
            return new_frame
        return frame

    def back(self, frame):
        frame.children['!entry'].delete(0, tk.END)
        frame.children['!entry2'].delete(0, tk.END)
        frame.children['!entry3'].delete(0, tk.END)
        websites = self.model.password_model.get_websites()
        new_frame = self.view.switch('home')
        for website in websites:
            new_frame.children['!listbox'].insert(tk.END, website.title())
        return new_frame