import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()

SOURCE_DB_USER = os.getenv('SOURCE_DB_USER')
SOURCE_DB_PASSWORD = os.getenv('SOURCE_DB_PASSWORD')
SOURCE_DB_HOST = os.getenv('SOURCE_DB_HOST')
SOURCE_DB_PORT = os.getenv('SOURCE_DB_PORT')
SOURCE_DB_FILENAME = os.getenv('SOURCE_DB_FILENAME')

TARGET_DB_USER = os.getenv('TARGET_DB_USER')
TARGET_DB_PASSWORD = os.getenv('TARGET_DB_PASSWORD')
TARGET_DB_HOST = os.getenv('TARGET_DB_HOST')
TARGET_DB_PORT = os.getenv('TARGET_DB_PORT')
TARGET_DB_FILENAME = os.getenv('TARGET_DB_FILENAME')


class DBSync:
    def __init__(self):
        """Создаём движки и сессии для обеих баз"""
        self.source_engine = create_engine(
            f'mysql+mysqlconnector://{SOURCE_DB_USER}:{SOURCE_DB_PASSWORD}@'
            f'{SOURCE_DB_HOST}:{SOURCE_DB_PORT}/{SOURCE_DB_FILENAME}'
        )
        self.target_engine = create_engine(
            f'mysql+mysqlconnector://{TARGET_DB_USER}:{TARGET_DB_PASSWORD}@'
            f'{TARGET_DB_HOST}:{TARGET_DB_PORT}/{TARGET_DB_FILENAME}'
        )
        self.source_session = Session(self.source_engine)
        self.target_session = Session(self.target_engine)

    def get_tables(self):
        """Получаем список таблиц из базы-образца"""
        tables = self.source_session.execute(
            "SHOW TABLES"
        ).all()
        return [i[0] for i in tables]

    def sync_table(self, table):
        """Синхронизируем данные по конкретной таблице"""
        target_table_exists_check = self.target_session.execute(
            f'SHOW TABLES LIKE "{table}"').all()
        if len(target_table_exists_check) == 0:
            self.target_session.execute(
                f'CREATE TABLE {table} LIKE {SOURCE_DB_FILENAME}.{table}'
            )
            self.target_session.execute(
                f'INSERT INTO {table} '
                f'SELECT * FROM {SOURCE_DB_FILENAME}.{table}'
            )
            self.target_session.commit()
        else:
            source_table_columns = set(self.source_session.execute(
                f'SHOW COLUMNS FROM {table}').all()
            )
            target_table_columns = set(self.target_session.execute(
                f'SHOW COLUMNS FROM {table}').all()
            )
            columns_difference = source_table_columns - target_table_columns
            if len(columns_difference) > 0:
                for column in columns_difference:
                    self.target_session.execute(
                        f'ALTER TABLE {table}'
                        f'ADD COLUMN {column[0]} {column[1]}'
                    )
                    self.target_session.commit()
            target_table_columns = [
                col[0] for col in self.target_session.execute(
                    f'DESCRIBE {table}').all()
            ]
            source_table_data = self.source_session.execute(
                f'SELECT * FROM {table}').all()
            for row in source_table_data:
                update_query = (
                    f"REPLACE INTO {table} "
                    f"({', '.join(target_table_columns)}) VALUES {row}"
                )
                self.target_session.execute(update_query)
                self.target_session.commit()

    def sync_all(self):
        """Синхронизируем все таблицы"""
        for table in self.get_tables():
            self.sync_table(table)


if __name__ == '__main__':
    sync = DBSync()
    sync.sync_all()
