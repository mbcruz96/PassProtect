import passwordmanager as pm
import tkinter as tk
from tkinter import messagebox
import views
from views import EventListener
import models

class Controller:
    def __init__(self, model:models.Model, view:views.View):
        self.view = view
        self.model = model
        self.frame = None
        self.website = None

        # initializing controllers
        self.signup_controller = SignupController(model, view)
        self.login_controller = LoginController(model, view)
        self.home_controller = HomeController(model, view)
        self.add_controller = AddController(model, view)
        self.change_controller = ChangeController(model, view)

        # creating event listeners
        EventListener.add_listener('on_login', self.on_login)
        EventListener.add_listener('on_logout', self.on_logout)
        EventListener.add_listener('to_signup', self.to_signup)
        EventListener.add_listener('on_signup', self.on_signup)
        EventListener.add_listener('on_select', self.on_select)
        EventListener.add_listener('to_add', self.to_add)
        EventListener.add_listener('add_password', self.add_password)
        EventListener.add_listener('to_change', self.to_change)
        EventListener.add_listener('on_change', self.on_change)
        EventListener.add_listener('on_remove', self.on_remove)
        EventListener.add_listener('on_back', self.on_back)

    # binding event listeners to their respective functions
    def _bind(self, frame):
        frame.children['!listbox'].bind('<ButtonRelease-1>', self.on_popup)

    def on_popup(self, event):
            try:
                self.frame.children['!menu'].post(event.x_root, event.y_root)
            finally:
                self.frame.children['!menu'].grab_release()

    def on_login(self, frame):
        self.frame = self.login_controller.login(frame)
        self._bind(self.frame)

    def on_logout(self, frame):
        self.frame = self.home_controller.logout(frame)

    def to_signup(self, frame):
        self.frame = self.login_controller.signup(frame)
    
    def on_signup(self, frame):
        self.frame = self.signup_controller.signup(frame)
        self._bind(self.frame)

    def on_select(self, frame):
        self.frame = self.home_controller.select(frame)

    def to_add(self, frame):
        self.frame = self.home_controller.add(frame)


    def add_password(self, frame):
        self.frame = self.add_controller.add(frame)

    def to_change(self, frame):
        self.frame, self.website = self.home_controller.change(frame)
                                                 
    def on_change(self, frame):
        self.frame = self.change_controller.change(frame, self.website)
        self.website = None
        self._bind(self.frame)


    def on_remove(self, frame):
        self.frame = self.home_controller.remove(frame)
        self._bind(self.frame)

    def on_back(self, frame):
        self. frame = self.add_controller.back(frame)
        self._bind(self.frame)

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
        login = self.model.base_model.login(username, password)
        if login is False:
            frame.children['!label5'].grid(row=6, column=1, padx=0, pady=10, sticky='w')
        elif login is None:
            frame.children['!label6'].grid(row=6, column=1, padx=0, pady=10, sticky='w')
        else:
           frame.children['!entry'].delete(0, tk.END)
           frame.children['!entry2'].delete(0, tk.END)
           websites = self.model.base_model.get_websites()
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
        frame.children['!label5'].grid_forget()
        frame.children['!label6'].grid_forget()
        name = frame.fullname.get()
        username = frame.username.get()
        password = frame.password.get()
        agreed = frame.agreed.get()

        if agreed is True:
            signup = self.model.base_model.signup(name, username, password)
            if signup is False:
                frame.children['!label5'].grid(row=6, column=1, padx=0, pady=10, sticky='w')
            else:
                websites = self.model.base_model.get_websites()
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
        index = frame.children['!listbox'].curselection()
        item = frame.children['!listbox'].get(index[0])
        self.model.base_model.get_password(item)
        return frame
    
    def change(self, frame):
        new_frame = self.view.switch('change')
        return new_frame
    
    def remove(self, frame):
        index = frame.children['!listbox'].curselection()
        website = frame.children['!listbox'].get(index[0])
        confirm = messagebox.askyesno('Remove Password', f'Are you sure you want to remove the password for {website}?')
        if confirm is True:
            removed = self.model.base_model.remove_password(website)
            if removed is True:
                frame.children['!listbox'].delete(index)
        return frame
    
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
        password_added = self.model.base_model.add_password(website, username, password)
        
        if password_added is False:
            frame.children['!label5'].pack()
        else:
            frame.children['!entry'].delete(0, tk.END)
            frame.children['!entry2'].delete(0, tk.END)
            frame.children['!entry3'].delete(0, tk.END)
            websites = self.model.base_model.get_websites()
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
        websites = self.model.base_model.get_websites()
        new_frame = self.view.switch('home')
        for website in websites:
            new_frame.children['!listbox'].insert(tk.END, website.title())
        return new_frame
    
class ChangeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def change(self, frame, website):
        # FIX FUNCTION, FUNCTION ADDS PASSWORD TO WEBSITES INSTEAD OF CHANGING PASSWORD
        frame.children['!label5'].grid_forget()
        frame.children['!label6'].grid_forget()
        username = frame.old_password.get()
        password = frame.new_password.get()
        website = frame.confirm_password.get()
        password_changed = self.model.base_model.change_password(website, username, password)
        
        if password_changed is False:
            frame.children['!label5'].pack()
        elif password_changed is None:
            frame.children['!label6'].pack()
        else:
            frame.children['!entry'].delete(0, tk.END)
            frame.children['!entry2'].delete(0, tk.END)
            frame.children['!entry3'].delete(0, tk.END)
            websites = self.model.base_model.get_websites()
            new_frame = self.view.switch('home')
            for website in websites:
               new_frame.children['!listbox'].insert(tk.END, website.title())
            return new_frame
        return frame

    def back(self, frame):
        frame.children['!entry'].delete(0, tk.END)
        frame.children['!entry2'].delete(0, tk.END)
        frame.children['!entry3'].delete(0, tk.END)
        websites = self.model.base_model.get_websites()
        new_frame = self.view.switch('home')
        for website in websites:
            new_frame.children['!listbox'].insert(tk.END, website.title())
        return new_frame