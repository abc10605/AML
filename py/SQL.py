import pathlib
import sqlite3
from sqlite3 import Error


class SQL():
    def __init__(self, file_name):  # Constructor -> 物件初始值
        # 資料庫路徑
        self.__db_file = f'{pathlib.Path(__file__).parent.parent}/data/'
        pathlib.Path(self.__db_file).mkdir(
            parents=True, exist_ok=True)  # 創建資料夾
        self.__create_connection(f'{self.__db_file}/{file_name}.db')  # 連結資料庫

        # 創建資料表SQL指令
        create_table_sdn = """CREATE TABLE IF NOT EXISTS SDN (
            QDi text PRIMARY KEY NOT NULL,
            Name text NOT NULL,
            OriginalScript text,
            Title text,
            Designation text,
            DOB datetime,
            POB text,
            GoodQuality text,
            LowQuality text,
            Nationality text,
            PassportNo text,
            IDNo text,
            Address text,
            ListedOn text
        )"""
        create_table_trans = """CREATE TABLE IF NOT EXISTS TRANS (
            TransID text PRIMARY KEY NOT NULL,
            Type text,
            OrigAcc text,
            DestAcc text,
            Amount interger,
            DT datetime,
            Flag integer
        )"""
        create_table_accounts = """CREATE TABLE IF NOT EXISTS ACCOUNTS (
            acc text PRIMARY KEY NOT NULL,
            name text,
            birthdate datetime,
            address text,
            mail text,
            company text,
            job text,
            nationality text,
            credit_score text
        )"""

        for i in create_table_accounts, create_table_trans, create_table_sdn:
            self.__create_table(i)

    def __create_connection(self, db_file):  # 連結資料庫函式
        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
        except Error as e:
            print(e)

    def __create_table(self, script):  # 建立資料表函式
        self.conn.cursor().execute(script)

    def insert_data(self, table, data):  # 插入資料函式
        try:
            # INSERT INTO TABLE VALUES (?, ?, ?, ?.......)
            self.__script = f"INSERT INTO {table} VALUES ({('?,' * len(data))[:-1]})"
            self.conn.cursor().execute(self.__script, data)
            self.conn.commit()
        except Error as e:
            print(e)

    def query(self, script):  # 查詢SQL
        try:
            return self.conn.cursor().execute(script).fetchall()
        except:
            return None

    def close(self):  # 關閉資料庫
        self.conn.close()
