import mysql.connector
from mysql.connector import pooling

class DatabasePool:
    _instance = None  # Class-level variable to store the singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabasePool, cls).__new__(cls)
            cls._instance._initialize_pool()
        return cls._instance

    def _initialize_pool(self):
        db_config = {
            "host": "10.95.136.128",
            "user": "fabricationuser",
            "password": "schueco&321",
            "database": "fabrication"
            # "host": "localhost",
            # "user": "fabuser",
            # "password": "fabuser&123",
            # "database": "fab"
        }
        self.db_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=15,pool_reset_session=True, **db_config)

    def get_db_connection(self):
        return self.db_pool.get_connection()


