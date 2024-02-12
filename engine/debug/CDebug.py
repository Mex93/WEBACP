class CDebug:
    __debug_system = False

    def debug_system_on(self, enabled: bool):
        self.__debug_system = enabled

    def debug_print(self, *args):
        if self.__debug_system is True:
            print(args)


