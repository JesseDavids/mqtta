#this is a main file which will initialise and execute the run method

#importing our application file
from core import MyApp

#while True:
if __name__ == "__main__":
    #initialising our application
    app = MyApp()
    app.run()