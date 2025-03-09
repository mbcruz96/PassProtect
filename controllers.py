import passwordmanager as pm
import tkinter as tk
from tkinter import messagebox, filedialog
import views
from views import EventListener
import models

class Controller:
    def __init__(self, model:models.Model, view:views.View):
        self.view = view
        self.model = model
        self.frame = None
        self.prev_frame = None
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
        EventListener.add_listener('get_password', self.get_password)
        EventListener.add_listener('get_username', self.get_username)
        EventListener.add_listener('to_add', self.to_add)
        EventListener.add_listener('add_password', self.add_password)
        EventListener.add_listener('on_import', self.on_import)
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
        try:
            self._bind(self.frame)
        except KeyError:
            pass

    def on_logout(self, frame):
        self.frame = self.home_controller.logout(frame)

    def to_signup(self, frame):
        self.frame = self.login_controller.signup(frame)
        self.prev_frame = 'login'
    
    def on_signup(self, frame):
        self.frame = self.signup_controller.signup(frame)
        try:
            self._bind(self.frame)
            self.prev_frame = None
        except KeyError:
            pass

    def get_password(self, frame):
        self.frame = self.home_controller.get_password(frame)
        try:
            self._bind(self.frame)
        except KeyError:
            pass

    def get_username(self, frame):
        self.frame = self.home_controller.get_username(frame)
        try:
            self._bind(self.frame)
        except KeyError:
            pass

    def to_add(self, frame):
        self.frame = self.home_controller.add(frame)
        self.prev_frame = 'home'

    def add_password(self, frame):
        self.frame = self.add_controller.add(frame)
        self.prev_frame = 'home'
        try:
            self._bind(self.frame)
        except KeyError:
            pass

    def on_import(self, frame):
        # FINISH LINKING TO CHANGE CONTROLLER IMPORT_PASSWORDS FUNCTION
        self.frame = self.add_controller.import_passwords(frame)
        try:
            self._bind(self.frame)
            self.prev_frame = None
        except KeyError:
            pass

    def to_change(self, frame):
        self.frame, self.website = self.home_controller.change(frame)
        self.prev_frame = 'home'

    def on_change(self, frame):
        self.frame = self.change_controller.change(frame, self.website)
        try:
            self._bind(self.frame)
            self.website = None
            self.prev_frame = None
        except KeyError:
            pass

    def on_remove(self, frame):
        self.frame = self.home_controller.remove(frame)
        try:
            self._bind(self.frame)
        except KeyError:
            pass

    def on_back(self, frame):
        if self.prev_frame == 'home':
            self.frame = self.add_controller.back(frame)
            try:
                self._bind(self.frame)
            except KeyError:
                pass
        elif self.prev_frame == 'login':
            self.frame = self.signup_controller.back(frame)
        else:
            pass

        self.prev_frame = None

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
        # initializing model and view
        self.model = model
        self.view = view
      
    def signup(self, frame):
        # removing error messages from view
        frame.children['!label5'].grid_forget()
        frame.children['!label6'].grid_forget()
        # getting form entries
        name = frame.fullname.get()
        username = frame.username.get()
        password = frame.password.get()
        agreed = frame.agreed.get()

        # if agreed checkbox is checked block
        if agreed is True:
            # registering user in system
            signup = self.model.base_model.signup(name, username, password)
            # registration fail block
            if signup is False:
                frame.children['!label5'].grid(row=7, column=1, padx=0, pady=10, sticky='w')
           # registration success block
            else:
                websites = self.model.base_model.get_websites()
                new_frame = self.view.switch('home')
                for website in websites:
                    new_frame.children['!listbox'].insert(tk.END, website.title())
                return new_frame
        else:
            frame.children['!label6'].grid(row=7, column=1, padx=0, pady=10, sticky='w')
        return frame
    
    def back(self, frame):
        # clearing form entries
        frame.children['!entry'].delete(0, tk.END)
        frame.children['!entry2'].delete(0, tk.END)
        frame.children['!entry3'].delete(0, tk.END)

        # switching to home view
        new_frame = self.view.switch('login')
        return new_frame
    
# controller for home view
class HomeController:
    def __init__(self, model, view):
        # initializing model and view
        self.model = model
        self.view = view
      
    def get_password(self, frame):
        # removing confirmation messages if present on view
        frame.children['!label2'].pack_forget()
        frame.children['!label3'].pack_forget()
        
        # retrieving active website
        website = frame.children['!listbox'].get(tk.ACTIVE)
        # copying password to clipboard
        self.model.base_model.get_password(website)
        # adding confirmation message to frame
        frame.children['!label2'].pack()
        return frame
    
    def get_username(self, frame):
        # removing confirmation messages if present on view
        frame.children['!label2'].pack_forget()
        frame.children['!label3'].pack_forget()
        
        # retrieving active website
        website = frame.children['!listbox'].get(tk.ACTIVE)
        # copying username to clipboard
        self.model.base_model.get_username(website)
        # adding confirmation message to frame
        frame.children['!label3'].pack()
        return frame
    
    def change(self, frame):
        # removing confirmation messages if present on view
        frame.children['!label2'].pack_forget()
        frame.children['!label3'].pack_forget()
        
        # retrieving active listbox selection
        website = frame.children['!listbox'].get(tk.ACTIVE)
        # switching to change password view
        new_frame = self.view.switch('change')
        # returning change password view and website thats password will be changed
        return(new_frame, website)

    
    def remove(self, frame):
        # removing confirmation messages if present on view
        frame.children['!label2'].pack_forget()
        frame.children['!label3'].pack_forget()
        
        # retrieving selected website
        website = frame.children['!listbox'].get(tk.ACTIVE)
        # displaying a confirmation window to remove window and storing return as flag
        confirm = messagebox.askyesno('Remove Password', f'Are you sure you want to remove the password for {website}?')

        # if confirmed block
        if confirm is True:
            # removing password and storing success flag
            removed = self.model.base_model.remove_password(website)
            # if website removed block
            if removed is True:
                # retrieving index of removed website
                index = frame.children['!listbox'].curselection()
                # removing website from lisbox of websites
                frame.children['!listbox'].delete(index)
        return frame
    
    def add(self, frame):
        # removing confirmation messages if present on view
        frame.children['!label2'].pack_forget()
        frame.children['!label3'].pack_forget()
        
        # switching to add password view
        new_frame = self.view.switch('add')
        return new_frame
    
    def logout(self, frame):
        # removing confirmation messages if present on view
        frame.children['!label2'].pack_forget()
        frame.children['!label3'].pack_forget()
        
        # switching to login view
        new_frame = self.view.switch('login')
        return new_frame
    
# controller for add password view
class AddController:
    def __init__(self, model, view):
        # initializing model and view
        self.model = model
        self.view = view
     
    def populate(self, frame):
        # getting list of current websites
        websites = self.model.base_model.get_websites()
        # populating listbox of websites
        for website in websites:
            frame.children['!listbox'].insert(tk.END, website.title())
        return frame
    
    def add(self, frame):
        # removing error label if added to view
        frame.children['!label5'].grid_forget()
        # getting form entries
        username = frame.username.get()
        password = frame.password.get()
        website = frame.website.get()
        # adding password and storing correctly added flag
        password_added = self.model.base_model.add_password(website, username, password)
        
        # if password was not added block
        if password_added is False:
            frame.children['!label5'].pack()
        # password added block
        else:
            # clearing entries in form
            frame.children['!entry'].delete(0, tk.END)
            frame.children['!entry2'].delete(0, tk.END)
            frame.children['!entry3'].delete(0, tk.END)

            # switching to home frame
            new_frame = self.view.switch('home')
            # populating listbox of websites
            new_frame = self.populate(new_frame)
            return new_frame
        
        return frame

    def import_passwords(self, frame):
        # starting file selection popup
        filename = filedialog.askopenfilename(
            title='Select a file',
            filetypes=(('CSV', "*.csv"),
                       ('Excel Workbook', "*.xlsx"))
        )

        if len(filename) > 0:
            # adding passwords from password csv file
            self.model.base_model.import_passwords(filename)

            # switching to home frame
            new_frame = self.view.switch('home')
            # populating listbox of websites
            new_frame = self.populate(new_frame)
            return new_frame
        else:
            # returning current frame if no file selected
            return frame
    
    def back(self, frame):
        # clearing form entries
        frame.children['!entry'].delete(0, tk.END)
        frame.children['!entry2'].delete(0, tk.END)
        frame.children['!entry3'].delete(0, tk.END)

        # switching to home view
        new_frame = self.view.switch('home')
        # populating listbox of websites
        new_frame = self.populate(new_frame)
        return new_frame
    
class ChangeController:
    def __init__(self, model, view):
        # initializing model and view 
        self.model = model
        self.view = view

    def populate(self, frame):
        # getting list of current websites
        websites = self.model.base_model.get_websites()
        # populating listbox of websites
        for website in websites:
            frame.children['!listbox'].insert(tk.END, website.title())
        return frame
    
    def change(self, frame, website):
        # removing error messages from view
        frame.children['!label5'].grid_forget()
        frame.children['!label6'].grid_forget()
        # retrieving form entries
        old_password = frame.old_password.get()
        new_password = frame.new_password.get()
        confirm_password = frame.confirm_password.get()

        # changing password for selected website and storing success flag
        password_changed = self.model.base_model.change_password(website, old_password, new_password, confirm_password)
        
        # block for if previous password is incorrect
        if password_changed is False:
            frame.children['!label5'].pack()
        # block for if new password and confirm password don't match
        elif password_changed is None:
            frame.children['!label6'].pack()
        # successful password change block
        else:
            # clearing form entries
            frame.children['!entry'].delete(0, tk.END)
            frame.children['!entry2'].delete(0, tk.END)
            frame.children['!entry3'].delete(0, tk.END)
            # switching to home view
            new_frame = self.view.switch('home')
            # populating listbox of websites
            new_frame = self.populate(new_frame)
            return new_frame
        return frame
    
    def back(self, frame):
        # clearing form entries
        frame.children['!entry'].delete(0, tk.END)
        frame.children['!entry2'].delete(0, tk.END)
        frame.children['!entry3'].delete(0, tk.END)
        # switching to home view
        new_frame = self.view.switch('home')
        # populating listbox of websites
        new_frame = self.populate(new_frame)
        return new_frame