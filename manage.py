from flask_script import Manager, Server
from app.main import create_app

app = create_app()
manager = Manager(app)

manager.add_command('runserver', Server(port=7012, use_debugger=True))

@manager.command
def hello():
    print('Hello World ...')


if __name__ == '__main__':
    manager.run()