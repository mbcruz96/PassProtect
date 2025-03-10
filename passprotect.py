import views
import models
import controllers

'''
TODO: allow excel files to be imported of websites with usernames and passwords
'''
def main():
    # initializing MVC model
    model = models.Model()
    view = views.View()
    controller = controllers.Controller(model, view)
    
    # starting the app
    controller.start()

if __name__ == '__main__':
    main()
