import os

from flask_script import Manager


from App import create_app

app = create_app(os.getenv("DICER2_CONFIG_PATH", "settings/dicer2.config.py"))

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
