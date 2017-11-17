#!/usr/bin/env python
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

from app import create_app, db, models

app = create_app('default')

manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, models=models)


manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def test():
    """Запускает модульные тесты"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
