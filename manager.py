from flask_migrate import MigrateCommand
from flask_script import Manager

from App import create_app

app = create_app("settings/dicer2_config.py")

manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
