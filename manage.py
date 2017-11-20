#!/usr/bin/env python
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate

from app import create_app, db, models

app = create_app('default')

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, models=models)


@manager.command
def test():
    """Запускает модульные тесты"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
