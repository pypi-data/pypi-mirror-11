# -*- coding: utf-8 -*-

from os.path import dirname, abspath, join, exists
from shutil import rmtree

from unittest import TestCase

from raw_sql_migrate import Config
from raw_sql_migrate.api import Api
from raw_sql_migrate.engines import database_api


__all__ = (
    'BaseTestCase',
    'DatabaseTestCase',
)


class BaseTestCase(TestCase):

    file_system_path_to_test_package = join(dirname(abspath(__file__)), 'test_package')
    file_system_test_migrations_path = join(file_system_path_to_test_package, 'migrations')
    file_system_path_to_init_py_in_migrations_directory = join(file_system_test_migrations_path, '__init__.py')
    python_path_to_test_package = 'tests.test_package'
    config = None
    api = None

    def _remove_test_migrations_directory(self):
        if exists(self.file_system_test_migrations_path):
            rmtree(self.file_system_test_migrations_path)

    def tearDown(self):
        self._remove_test_migrations_directory()


class DatabaseTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = Config()
        cls.config.init_from_file()
        cls.api = Api(cls.config)

    def tearDown(self):
        try:
            database_api.execute(
                '''
                DROP TABLE %s;
                ''' % self.config.history_table_name
            )
            database_api.commit()
        except:
            pass
        super(DatabaseTestCase, self).tearDown()
