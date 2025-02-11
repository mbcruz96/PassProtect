import views
import tkinter as tk

view = views.View()
frame = view.frames['signup']
print(frame.__dict__)
print(type(frame.children['!button']))
view.switch('signup')
view.start_loop()
