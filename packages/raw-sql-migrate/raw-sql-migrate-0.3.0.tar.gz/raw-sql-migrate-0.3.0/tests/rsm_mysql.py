# -*- coding: utf-8 -*-

RSM_CONFIG = {
    'database': {
        'engine': 'raw_sql_migrate.engines.mysql',
        'host': '',
        'port': '',
        'name': 'rsm_test',
        'user': 'root',
        'password': '',
    },
    'history_table_name': 'migration_history',
    'packages': [
        'tests.test_package',
    ],
}
