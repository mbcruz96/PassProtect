import passwordmanager as pm
import tkinter as tk
from tkinter import messagebox, filedialog
import views
from views import EventListener
import models

# master controller
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
        EventListener.add_listener('open_url', self.open_url)
        EventListener.add_listener('to_add', self.to_add)
        EventListener.add_listener('add_password', self.add_password)
        EventListener.add_listener('to_import', self.to_import)
        EventListener.add_listener('on_import', self.on_import)
        EventListener.add_listener('select_path', self.select_path)
        EventListener.add_listener('on_about', self.on_about)
        EventListener.add_listener('to_change', self.to_change)
        EventListener.add_listener('on_change', self.on_change)
        EventListener.add_listener('on_remove', self.on_remove)
        EventListener.add_listener('on_back', self.on_back)

    # binding event listeners to their respective functions
    def _bind(self, frame):
        frame.children['!listbox'].bind('<ButtonRelease-1>', self.on_popup)

    def _unbind(self, frame):
        frame.children['!listbox'].unbind('<ButtonRelease-1>')

    # event listener callback functions
    def on_popup(self, event):
        # binds clicking on a website with the popup menu appearing by the selected website
        try:
            self.frame.children['!menu2'].post(event.x_root, event.y_root)
        finally:
            self.frame.children['!menu2'].grab_release()

    def on_login(self, frame):
        # triggered when user attempts to login
        self.frame, passwords_available = self.login_controller.login(frame)
        if passwords_available is False:
            pass
        else:
            try:
                self._bind(self.frame)
            except KeyError:
                pass

    def on_logout(self, frame):
        # triggered when user logs out
        self.frame = self.home_controller.logout(frame)
        try:
            self._unbind(self.frame)
        except KeyError:
            pass

    def to_signup(self, frame):
        # triggered when user hits signup button on login view
        self.frame = self.login_controller.signup(frame)
        self.prev_frame = 'login'
    
    def on_signup(self, frame):
        # triggered when user hits signup button on signup view
        self.frame, passwords_available = self.signup_controller.signup(frame)
        if passwords_available is False:
            pass
        else:
            try:
                self._bind(self.frame)
                self.prev_frame = None
            except KeyError:
                pass

    def get_password(self, frame):
        # triggered when get password option selected from popup menu
        self.frame = self.home_controller.get_password(frame)
        try:
            self._bind(self.frame)
        except KeyError:
            pass

    def get_username(self, frame):
        # triggered when get username option selected from popup menu
        self.frame = self.home_controller.get_username(frame)
        try:
            self._bind(self.frame)
        except KeyError:
            pass
    
    def open_url(self, frame):
        # triggered when open url option selected from popup menu
        self.frame = self.home_controller.open_url(frame)
        try:
            self._bind(self.frame)
        except KeyError:
            pass

    def to_add(self, frame):
        # triggered when add password button is hit on home view
        self.frame = self.home_controller.add(frame)
        self.prev_frame = 'home_to_add'

    def add_password(self, frame):
        # triggered when add button hit on add view
        self.frame, passwords_available = self.add_controller.add(frame)
        self.prev_frame = 'home_to_add'
        if passwords_available is False:
            pass
        else:
            try:
                self._bind(self.frame)
            except KeyError:
                pass

    def to_import(self, frame):
        # triggered when import passwords button hit on add view
        self.frame = self.add_controller.to_import(frame)
        self.prev_frame = 'add'
        
    def on_import(self, frame):
        self.frame, passwords_available = self.add_controller.import_passwords(frame)
        self.prev_frame = None
        if passwords_available is False:
            pass
        else:
            try:
                self._bind(self.frame)
            except KeyError:
                pass

    def select_path(self, frame):
        self.frame = self.add_controller.select_path(frame)

    def on_about(self, frame):
        self.frame = self.add_controller.about_import(frame)

    def to_change(self, frame):
        # triggered when change password option selected from popup menu
        self.frame, self.website = self.home_controller.change(frame)
        self.prev_frame = 'home_to_change'

    def on_change(self, frame):
        # triggered when confirm button hit on change view
        self.frame = self.change_controller.change(frame, self.website)
        try:
            self._bind(self.frame)
            self.website = None
            self.prev_frame = None
        except KeyError:
            pass

    def on_remove(self, frame):
        # triggered when remove password option selected from popup menu
        self.frame, passwords_available = self.home_controller.remove(frame)
        if passwords_available is False:
            try:
                self._unbind(self.frame)
            except KeyError:
                pass
        else:
            try:
                self._bind(self.frame)
            except KeyError:
                pass

    def on_back(self, frame):
        # triggered when any back buttons are hit
        if self.prev_frame == 'home_to_add':
            self.frame, passwords_available = self.add_controller.back_home(frame)
            self.prev_frame = None
            if passwords_available is False:
                try:
                    self._unbind(self.frame)
                except KeyError:
                    pass
            else:
                try:
                    self._bind(self.frame)
                except KeyError:
                    pass
        elif self.prev_frame == 'home_to_change':
            self.frame = self.change_controller.back(frame)
            self.prev_frame = None
            try:
                self._bind(self.frame)
            except KeyError:
                pass
        elif self.prev_frame == 'login':
            self.frame = self.signup_controller.back(frame)
            self.prev_frame = None
        elif self.prev_frame == 'add':
            self.frame = self.add_controller.back_add(frame)
            self.prev_frame = 'home_to_add'
        else:
            pass

    # starting the application
    def start(self):
        self.frame = self.view.switch('login')
        self.view.start_loop()

# controller for login view
class LoginController:
    def __init__(self, model, view):
        # initializing model and view
        self.model = model
        self.view = view
    
    def signup(self, frame):
        # switiching to signup view
        new_frame = self.view.switch('signup')
        return new_frame
    
    def login(self, frame):
        # removing error messages from view
        frame.children['!label5'].grid_forget()
        frame.children['!label6'].grid_forget()
        # retrieving user form entries
        username = frame.username.get()
        password = frame.password.get()
        # authorizing user
        login = self.model.base_model.login(username, password)
        # username/password incorrect block
        if login is False:
            frame.children['!label5'].grid(row=6, column=1, padx=0, pady=10, sticky='w')
        # user not registered block
        elif login is None:
            frame.children['!label6'].grid(row=6, column=1, padx=0, pady=10, sticky='w')
        # successful user authorization block
        else:
            # removing user entries from forms
            frame.children['!entry'].delete(0, tk.END)
            frame.children['!entry2'].delete(0, tk.END)
            # retrieving stored website for current user
            websites = self.model.base_model.get_websites()
            # switching to home view
            new_frame = self.view.switch('home')
            # populating listbox with the users stored websites
            if len(websites) > 0:
                for website in websites:
                    new_frame.children['!listbox'].insert(tk.END, website.title())
                return (new_frame, True)
            else:
               return (frame, False)

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
                if len(websites) > 0:
                    for website in websites:
                        new_frame.children['!listbox'].insert(tk.END, website.title())
                    return (new_frame, True)
                else:
                    return(new_frame, False)
        else:
            frame.children['!label6'].grid(row=7, column=1, padx=0, pady=10, sticky='w')
        return (frame, False)
    
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
        frame.children['!label4'].pack_forget()

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
        frame.children['!label4'].pack_forget()

        # retrieving active website
        website = frame.children['!listbox'].get(tk.ACTIVE)
        # copying username to clipboard
        self.model.base_model.get_username(website)
        # adding confirmation message to frame
        frame.children['!label3'].pack()
        return frame
    
    def open_url(self, frame):
        # removing confirmation messages if present on view
        frame.children['!label2'].pack_forget()
        frame.children['!label3'].pack_forget()
        frame.children['!label4'].pack_forget()

        # retrieving active website
        website = frame.children['!listbox'].get(tk.ACTIVE)
        # copying username to clipboard
        opened = self.model.base_model.open_url(website)
        if opened == False:
            frame.children['!label4'].pack()
        return frame
    
    def change(self, frame):
        # removing confirmation messages if present on view
        frame.children['!label2'].pack_forget()
        frame.children['!label3'].pack_forget()
        frame.children['!label4'].pack_forget()

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
        frame.children['!label4'].pack_forget()
        
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
                num_items = frame.children['!listbox'].size()
                if num_items > 0:
                    return (frame, True)
                else:
                    return (frame, False)
        else:
            return (frame, True)
        
    def add(self, frame):
        # removing confirmation messages if present on view
        frame.children['!label2'].pack_forget()
        frame.children['!label3'].pack_forget()
        frame.children['!label4'].pack_forget()

        # switching to add password view
        new_frame = self.view.switch('add')
        return new_frame
    
    def logout(self, frame):
        # removing confirmation messages if present on view
        frame.children['!label2'].pack_forget()
        frame.children['!label3'].pack_forget()
        frame.children['!label4'].pack_forget()

        # switching to login view
        new_frame = self.view.switch('login')
        return new_frame
    
# controller for add password view
class AddController:
    def __init__(self, model, view):
        # initializing model and view
        self.model = model
        self.view = view
        self.file_path = None

    def populate(self, frame):
        # getting list of current websites
        websites = self.model.base_model.get_websites()
        # populating listbox of websites
        for website in websites:
            frame.children['!listbox'].insert(tk.END, website.title())
        return frame
    
    def add(self, frame):
        # removing error label if added to view
        frame.children['!label7'].grid_forget()
        frame.children['!label8'].grid_forget()
        frame.children['!label2'].config(fg='black')
        frame.children['!label3'].config(fg='black')
        frame.children['!label4'].config(fg='black')
        # getting form entries
        website = frame.website.get()
        username = frame.username.get()
        password = frame.password.get()
        url = frame.url.get()
        # form entries completed flag
        complete_form = True

        # ensuring required form entries are full
        if len(website) == 0:
            frame.children['!label8'].grid(row=9, column=1, padx=0, pady=10, sticky='w')
            frame.children['!label2'].config(fg='red')
            complete_form = False
        if len(username) == 0:
            frame.children['!label8'].grid(row=9, column=1, padx=0, pady=10, sticky='w')
            frame.children['!label3'].config(fg='red')
            complete_form = False
        if len(password) == 0:
            frame.children['!label8'].grid(row=9, column=1, padx=0, pady=10, sticky='w')
            frame.children['!label4'].config(fg='red')
            complete_form = False
        if complete_form is False:
            return(frame, False)
        
        # adding password and storing correctly added flag
        password_added = self.model.base_model.add_password(website, username, password, url)
        
        # if password was not added block
        if password_added is False:
            frame.children['!label7'].grid(row=9, column=1, padx=0, pady=10, sticky='w')
            return(frame, False)
        # password added block
        else:
            # clearing entries in form
            frame.children['!entry'].delete(0, tk.END)
            frame.children['!entry2'].delete(0, tk.END)
            frame.children['!entry3'].delete(0, tk.END)
            frame.children['!entry4'].delete(0, tk.END)
            frame.children['!entry5'].delete(0, tk.END)

            # switching to home frame
            new_frame = self.view.switch('home')
            # populating listbox of websites
            new_frame = self.populate(new_frame)
            return (new_frame, True)

    def to_import(self, frame):
        new_frame = self.view.switch('import')
        return(new_frame)
    
    def import_passwords(self, frame):
        if self.file_path is not None:
            self.model.base_model.import_passwords(self.file_path)

            # switching to home frame
            new_frame = self.view.switch('home')
            # populating listbox of websites
            new_frame = self.populate(new_frame)
            self.file_path = None
            frame.children['!entry'].delete(0, tk.END)
            return (new_frame, True)
        else:
            # returning current frame if no file selected
            return (frame, False)

    def select_path(self, frame):
        # starting file selection popup
        filename = filedialog.askopenfilename(
            title='Select a file',
            filetypes=(('CSV', "*.csv"),
                       ('Excel Workbook', "*.xlsx"))
        )

        if len(filename) > 0:
            # adding passwords from password csv file
            frame.children['!entry'].insert(0, filename)
            self.file_path = filename
        return frame
    
    def about_import(self, frame):
        # starting import file information popup message
        message = """PassProtect import files must be in CSV format and contain the following case sensitive column names:\n 
        Username: Username associated with the password\n
        Password: Password to be managed\n
        Name: The name/nickname for the password source\n
        Website: (optionl) URL associated with password\n
        Type: (optional) type of institution\n"""

        messagebox.showinfo(title='About Import File', message=message)
        return frame
    
    def back_home(self, frame):
        # clearing form entries
        frame.children['!entry'].delete(0, tk.END)
        frame.children['!entry2'].delete(0, tk.END)
        frame.children['!entry3'].delete(0, tk.END)
        frame.children['!entry4'].delete(0, tk.END)
        frame.children['!entry5'].delete(0, tk.END)

        # switching to home view
        new_frame = self.view.switch('home')

        # getting list of current websites
        websites = self.model.base_model.get_websites()
        if len(websites) > 0:
            # populating listbox of websites
            for website in websites:
                new_frame.children['!listbox'].insert(tk.END, website.title())
            return (new_frame, True)
        else:
            return(new_frame, False)

    def back_add(self, frame):
        self.file_path = None
        new_frame = self.view.switch('add')
        return new_frame
        
# controller for change password
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