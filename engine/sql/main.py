from engine.sql.CSQL import csql_eng, ErrorSQLData, ErrorSQLQuery, NotConnectToDB
import engine.sql.enums as cenum
from engine.sql.config import db_standart_connect_params, db_assembly_connect_params

# from engine_scripts.py.sql.sql_data import

PROGRAM_TIME_TYPE = "0300"  # Russia


class SqlAgent_Main(csql_eng):
    def __init__(self):
        super().__init__()

        self.__connect_handle = False
        self.__sql_object = None

        self.__sql_data_line = db_assembly_connect_params
        self.__sql_data_local = db_standart_connect_params
        self.__sql_time = PROGRAM_TIME_TYPE

    def get_sql_handle(self):
        return self.__connect_handle

    def connect_to_db(self, connect_db_type: cenum.CONNECT_DB_TYPE) -> bool:
        if self.__connect_handle is False:

            if connect_db_type == cenum.CONNECT_DB_TYPE.LINE:
                self.set_connect_data(self.__sql_data_line)
            if connect_db_type == cenum.CONNECT_DB_TYPE.LOCAL:
                self.set_connect_data(self.__sql_data_local)
            else:
                raise ErrorSQLData("Error SQL | db changed connect type!")
            if self.is_valid_saved_connect_data() is False:  # Saved in config data is NOT correct
                raise ErrorSQLData("Error SQL | incomming connections data!")

            connect_handle = self.sql_connect(self.__sql_time)
            if connect_handle is False:  # Connecting not successful
                raise NotConnectToDB("Error SQL | db not connect!")

            self.__connect_handle = connect_handle
            self.__sql_object = self
            return True

        return False

    def disconnect_from_db(self) -> bool:
        if self.__connect_handle is not False:
            self.__sql_object.sql_disconnect()
            self.__connect_handle = False
            self.__sql_object = None
            return True
        return False
