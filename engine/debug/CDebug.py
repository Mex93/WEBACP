from engine.debug.CExcelLog import CExcelLog


class CDebug:
    __debug_system = False

    def debug_system_on(self, enabled: bool):
        self.__debug_system = enabled

    def debug_print(self, *args):
        if self.__debug_system is True:
            print(args)
            CExcelLog.print_user_log(str(args))

    @staticmethod
    def debug_sql_print(user: str, action: str, data: str):
        CExcelLog.print_sql_log(user, action, data)
