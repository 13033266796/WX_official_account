from flask_script import Manager

from main.app import create_app

application = create_app("main")
application.config['DEBUG'] = True

manager = Manager(application)


@manager.command
def hello():
    print("hello")


if __name__ == "__main__":
    manager.run()
