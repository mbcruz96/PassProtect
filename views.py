import tkinter as tk

# event listener
class EventListener:
    '''
    Class to handle event listeners and trigger events
    '''
    event_listeners = {}
  
    def add_listener(event, callback):
        '''
        Function adds a listener and callback function for a specific event 
        '''
        try:
            EventListener.event_listeners[event].append(callback)
        except KeyError:
            EventListener.event_listeners[event] = [callback,]

    def trigger_event(event, frame):
        '''
        Function triggers an event and transfers control to associated callback function
        '''
        if event not in EventListener.event_listeners.keys():
            return
        for callback in EventListener.event_listeners[event]:
            callback(frame)

# root window
class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        # initialing root window attributes
        start_width = 500
        min_width = 400
        start_height = 400
        min_height = 250

        self.geometry(f"{start_width}x{start_height}")
        self.minsize(width=min_width, height=min_height)
        self.title('PassProtect')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

# master view
class View:
    def __init__(self):
        super().__init__()
        self.root = Root()  # root window
        self.current_view = None    # currently active view
        # view functors
        self.frames = {
            'login' : LoginView,
            'signup' : SignUpView,
            'home' : HomeView,
            'add' : AddView,
            'change': ChangeView
        }

    def switch(self, view):
        '''
        Function destroys active view and raises the specified view
        '''
        # initializing new view
        frame = self.frames[view](self.root)
        # destroying active view if one exists
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = frame
        self.current_view.grid(row=0, column=0, sticky='nsew')
        return frame
    
    def start_loop(self):
        self.root.mainloop()

# login view
class LoginView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        # header
        self.header = tk.Label(self, text='Sign in with existing account').grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # input variables
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # input entries
        self.uname_label = tk.Label(self, text="Username").grid(row=1, column=0, padx=10, sticky='w')
        self.passw_label = tk.Label(self, text="Password").grid(row=2, column=0, padx=10, sticky='w')
        
        self.uname_entry = tk.Entry(self, textvariable=self.username, ).grid(row=1, column=1, padx=(0,20), sticky='ew')
        self.passw_entry = tk.Entry(self, textvariable=self.password, show='*').grid(row=2, column=1, padx=(0,20), sticky='ew')

        # signup button
        self.submit_btn = tk.Button(
            self, 
            text="Submit", 
            command=self.on_login
        ).grid(row=3, column=1, padx=0, pady=10, sticky='w')
        
        # signup label
        self.signup_label = tk.Label(self, text="Don't have an account?").grid(row=4, column=1, sticky='w')
        # signup button
        self.signup_btn = tk.Button(
            self, 
            text="Sign Up", 
            command=self.to_signup
        ).grid(row=5, column=1, padx=0, pady=10, sticky='w')
        
        # error messages
        self.password_err_msg = tk.Label(self, text='Incorrect username/password, try again.', fg='red')
        self.signup_err_msg = tk.Label(self, text='Sign up to continue', fg='red')
    
    # button event triggers
    def on_login(self):
        EventListener.trigger_event('on_login', self)
    
    def to_signup(self):
        EventListener.trigger_event('to_signup', self)

# signup view
class SignUpView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        # header
        self.header = tk.Label(self, text='Sign up').grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # input variables
        self.fullname = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.agreed = tk.BooleanVar()

        # input entries
        self.name_label = tk.Label(self, text='Full Name').grid(row=1, column=0, padx=10, sticky='w')
        self.uname_label = tk.Label(self, text='Username').grid(row=2, column=0, padx=10, sticky='w')
        self.passw_label = tk.Label(self, text='Password').grid(row=3, column=0, padx=10, sticky='w')
        
        self.name_entry = tk.Entry(self, textvariable=self.fullname).grid(row=1, column=1, padx=(0,20), sticky='ew')
        self.uname_entry = tk.Entry(self, textvariable=self.username).grid(row=2, column=1, padx=(0,20), sticky='ew')
        self.passw_entry = tk.Entry(self, textvariable=self.password, show='*').grid(row=3, column=1, padx=(0,20), sticky='ew')

        # terms and conditions checkbox
        self.checkbox = tk.Checkbutton(
            self,   
            text='Agree to Terms and Conditions', 
            variable=self.agreed
        ).grid(row=4, column=1, padx=0, pady=10, sticky='w')
        
        # sign up button
        self.signup_btn = tk.Button(
            self, 
            text='Sign Up', 
            command=self.on_signup
        ).grid(row=5, column=1, padx=0, pady=10, sticky='w')
       
       # back button
        self.back_btn = tk.Button(
           self, 
            text='Back',
            command=self.on_back
       ).grid(row=6, column=1, padx=0, pady=10, sticky='w')
        
        # error messages
        self.signup_err_msg = tk.Label(self, text='Username already exists, choose another.', fg='red')
        self.agree_err_msg = tk.Label(self, text='Accept terms and conditions to continue.', fg='red')

    # button event triggers
    def on_signup(self):
        EventListener.trigger_event('on_signup', self)
    
    def on_back(self):
        EventListener.trigger_event('on_back', self)

# home view
class HomeView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        #self.header = tk.Label(self, text='Websites').pack()

        # logout menu
        self.menu_bar = tk.Menu(self,tearoff=1)
        self.logout_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.logout_menu.add_command(label='Logout', command=self.on_logout)
        self.menu_bar.add_cascade(label='Exit', menu=self.logout_menu)
        args[0].config(menu=self.menu_bar)
        
        # user website listbox
        self.listbox = tk.Listbox(self).pack(expand=True, fill='both')
        self.scrollbar = tk.Scrollbar(self.listbox)

        # website event popup menu
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label='Get Username', command=self.get_username)
        self.popup_menu.add_command(label='Get Password', command=self.get_password)
        self.popup_menu.add_command(label='Change Password', command=self.to_change)
        self.popup_menu.add_command(label='Open URL', command=self.open_url)
        self.popup_menu.add_command(label='Remove', command=self.on_remove)

        '''
        self.select_btn = tk.Button(
            self, 
            text='Get Password', 
            command=self.on_select
        ).pack(padx=0, pady=10)

        self.change_btn = tk.Button(
            self,
            text='Change Password',
            command=self.to_change
        ).pack(padx=0, pady=10)
        '''
        # add password button
        self.add_btn = tk.Button(
            self, 
            text='Add Password', 
            command=self.to_add
        ).pack(padx=0, pady=10)

        # logout of account button
        self.logout_btn = tk.Button(
            self, 
            text='Logout', 
            command=self.on_logout
            ).pack(padx=0, pady=10)
        
        # confirmation messages
        self.password_copied = tk.Label(self, text='Password copied to clipboard')
        self.username_copied = tk.Label(self, text='Username copied to clipboard')

        # error messages 
        self.url_err = tk.Label(self, text='No URL available for website', fg='red')

    # event triggers for popup menu and buttons
    def get_username(self):
        EventListener.trigger_event('get_username', self)

    def get_password(self):
        EventListener.trigger_event('get_password', self)

    def to_change(self):
        EventListener.trigger_event('to_change', self)

    def open_url(self):
        EventListener.trigger_event('open_url', self)

    def on_remove(self):
        EventListener.trigger_event('on_remove', self)

    '''
    de8f on_popup(self, event):
        try:
            self.popup_menu.post(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()
    '''

    def to_add(self):   
        EventListener.trigger_event('to_add', self)

    def on_logout(self):
        EventListener.trigger_event('on_logout', self)

        '''
        self.header = tk.Label(self, text='Passprotect').grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.listbox = tk.Listbox(self).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        for website in args:
            self.children['!listbox'].insert(tk.END, website)
            
        self.select_btn = tk.Button(self, text='Select').grid(row=2, column=1, padx=0, pady=10, sticky='nsew')
        self.add_btn = tk.Button(self, text='Add Password').grid(row=3, column=1, padx=0, pady=10, sticky='nsew')
        self.logout_btn = tk.Button(self, text='Logout').grid(row=4, column=1, padx=0, pady=10, sticky='nsew')
        '''
        
# add password view
class AddView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # header
        self.header = tk.Label(self, text='Add Password').grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # input variables
        self.website = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.url = tk.StringVar()

        # input entries
        self.website_label = tk.Label(self, text='Website').grid(row=1, column=0, padx=10, sticky='w')
        self.uname_label = tk.Label(self, text='Username').grid(row=2, column=0, padx=10, sticky='w')
        self.passw_label = tk.Label(self, text='Password').grid(row=3, column=0, padx=10, sticky='w')
        self.url_label = tk.Label(self, text='URL (optional)').grid(row=4, column=0, padx=10, sticky='w')
        
        self.website_entry = tk.Entry(self, textvariable=self.website).grid(row=1, column=1, padx=(0,20), sticky='ew')
        self.uname_entry = tk.Entry(self, textvariable=self.username).grid(row=2, column=1, padx=(0,20), sticky='ew')
        self.passw_entry = tk.Entry(self, textvariable=self.password, show='*').grid(row=3, column=1, padx=(0,20), sticky='ew')
        self.url_entry = tk.Entry(self, textvariable=self.url).grid(row=4, column=1, padx=(0,20), sticky='ew')

        # add website/password button
        self.add_btn = tk.Button(
            self, 
            text='Add',
            command=self.on_add
        ).grid(row=5, column=1, padx=0, pady=10, sticky='w')

        # import CSV of passwords button
        self.import_btn = tk.Button(
            self, 
            text='Import Passwords',
            command=self.on_import
        ).grid(row=6, column=1, padx=0, pady=10, sticky='w')

        # back button
        self.back_btn = tk.Button(
            self, 
            text='Back', 
            command=self.on_back
        ).grid(row=7, column=1, padx=0, pady=10, sticky='w')
        
        # error message
        self.err_msg = tk.Label(self, text='A password already exists for this website', fg='red')

    # button event triggers
    def on_add(self):
        EventListener.trigger_event('add_password', self)

    def on_import(self):
        EventListener.trigger_event('on_import', self)

    def on_back(self):
        EventListener.trigger_event('on_back', self)

# change password viw
class ChangeView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # header
        self.header = tk.Label(self, text='Change Password').grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # input variables
        self.old_password = tk.StringVar()
        self.new_password = tk.StringVar()
        self.confirm_password = tk.StringVar()

        # input entries
        self.old_password_label = tk.Label(self, text='Previous Password').grid(row=1, column=0, padx=10, sticky='w')
        self.new_password_label = tk.Label(self, text='New Password').grid(row=2, column=0, padx=10, sticky='w')
        self.confirm_password_label = tk.Label(self, text='Confirm Password').grid(row=3, column=0, padx=10, sticky='w')
        
        self.website_entry = tk.Entry(self, textvariable=self.old_password, show='*').grid(row=1, column=1, padx=(0,20), sticky='ew')
        self.uname_entry = tk.Entry(self, textvariable=self.new_password, show='*').grid(row=2, column=1, padx=(0,20), sticky='ew')
        self.passw_entry = tk.Entry(self, textvariable=self.confirm_password, show='*').grid(row=3, column=1, padx=(0,20), sticky='ew')

        # confirm change button
        self.confirm_btn = tk.Button(
            self, 
            text='Confirm',
            command=self.on_change
        ).grid(row=4, column=1, padx=0, pady=10, sticky='w')

        # back button
        self.back_btn = tk.Button(
            self, 
            text='Back', 
            command=self.on_back
        ).grid(row=6, column=1, padx=0, pady=10, sticky='w')

        # error messages
        self.incorrect_err_msg = tk.Label(self, text='Previous password incorrect', fg='red')
        self.mismatch_err_msg = tk.Label(self, text='New passwords do not match', fg='red')

    # button event triggers
    def on_change(self):
        EventListener.trigger_event('on_change', self)

    def on_back(self):
        EventListener.trigger_event('on_back', self)
