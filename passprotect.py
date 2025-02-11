import views
import models
import controllers

def main():
    model = models.Model()
    view = views.View()
    controller = controllers.Controller(model, view)
    
    controller.start()

if __name__ == '__main__':
    main()
