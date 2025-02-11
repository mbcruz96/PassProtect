import tkinter as tk

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        start_width = 500
        min_width = 400
        start_height = 300
        min_height = 250

        self.geometry(f"{start_width}x{start_height}")
        self.minsize(width=min_width, height=min_height)
        self.title('PassProtect')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

class View:
    def __init__(self):
        self.root = Root()
        self.current_view = None
        '''self.login_view = LoginView()
        self.signup_view = SignUpView()
        self.home_view = HomeView()
        self.frames = {
            'login' : self.login_view,
            'signup' : self.signup_view,
            'home' : self.home_view,
        }''' 
        self.frames = {}
         
        self.add_frame(LoginView, 'login')
        self.add_frame(SignUpView, 'signup')
        self.add_frame(HomeView, 'home')
        
        
    def add_frame(self, Frame, name):
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def switch(self, view):
        frame = self.frames[view]
        frame.tkraise()
        '''frame = self.frames[view](self.root)
        if self.current_view is not None:
            self.root.destroy()
        self.current_view = frame
        self.current_view.grid(row=0, column=0, sticky='nsew')''' 
        
        

    def start_loop(self):
        self.root.mainloop()

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
        self.submit_btn = tk.Button(self, text="Submit").grid(row=3, column=1, padx=0, pady=10, sticky='w')
        self.signup_label = tk.Label(self, text="Don't have an account?").grid(row=4, column=1, sticky='w')
        self.signup_btn = tk.Button(self, text="Sign Up").grid(row=5, column=1, padx=0, pady=10, sticky='w')
        
        # error messages
        self.password_err_msg = tk.Label(self, text='Incorrect username/password, try again.', fg='red') 
        self.signup_err_msg = tk.Label(self, text='Sign up to continue', fg='red')

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

        # input entries
        self.name_label = tk.Label(self, text='Full Name').grid(row=1, column=0, padx=10, sticky='w')
        self.uname_label = tk.Label(self, text='Username').grid(row=2, column=0, padx=10, sticky='w')
        self.passw_label = tk.Label(self, text='Password').grid(row=3, column=0, padx=10, sticky='w')
        self.name_entry = tk.Entry(self, textvariable=self.fullname).grid(row=1, column=1, padx=(0,20), sticky='ew')
        self.uname_entry = tk.Entry(self, textvariable=self.username).grid(row=2, column=1, padx=(0,20), sticky='ew')
        self.passw_entry = tk.Entry(self, textvariable=self.password, show='*').grid(row=3, column=1, padx=(0,20), sticky='ew')

        # terms and conditions checkbox
        self.agreed = False
        self.checkbox = tk.Checkbutton(
            self,   
            text='Agree to Terms and Conditions', 
            variable=self.agreed,
            onvalue=True,
            offvalue=False).grid(row=4, column=1, padx=0, pady=10, sticky='w')
        
        # sign up button
        self.signup_btn = tk.Button(self, text='Sign Up').grid(row=5, column=1, padx=0, pady=10, sticky='w')

        # error messages
        self.signup_err_msg = tk.Label(self, text='Username already exists, choose another.', fg='red')
        self.agree_err_msg = tk.Label(self, text='Accept terms and conditions to continue.', fg='red')

class HomeView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = tk.Label(self, text='Passprotect').grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.listbox = tk.Listbox(self).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        for website in args:
            self.children['!listbox'].insert(tk.END, website)
            
        self.select_btn = tk.Button(self, text='Select').grid(row=2, column=1, padx=0, pady=10, sticky='w')
        self.add_btn = tk.Button(self, text='Add Password').grid(row=3, column=1, padx=0, pady=10, sticky='w')

        
        
        