from flask import Flask, render_template, request, redirect, url_for, session

from engine.pages.enums import PAGE_ID

class CPages:
    def __init__(self, cdebug):
        # templates
        self.__template_name_login = 'login'
        self.__template_name_logout = 'logout'
        self.__template_name_account_main = 'account_main'
        self.__template_name_account_config = 'account_config'

        self.__template_name_index = 'index'
        self.__template_name_about = 'about'
        self.__template_name_404 = '404'

        # routs
        self.__route_name_login = 'account/login'
        self.__route_name_logout = 'account/logout'
        self.__route_name_account_main = 'account/main'
        self.__route_name_account_config = 'account/config'

        self.__route_name_index = 'index'
        self.__route_name_about = 'about'
        self.__route_name_404 = '404'

        self.__debug_unit = cdebug

    def get_page_template_name_from_page_id(self, page_id: PAGE_ID) -> bool | str:
        match page_id:
            case PAGE_ID.LOGIN:
                name = self.__template_name_login
            case PAGE_ID.LOGOUT:
                name = self.__template_name_logout
            case PAGE_ID.ACCOUNT_MAIN:
                name = self.__template_name_account_main
            case PAGE_ID.ACCOUNT_CONFIG:
                name = self.__template_name_account_config
            case PAGE_ID.INDEX:
                name = self.__template_name_index
            case PAGE_ID.ABOUT:
                name = self.__template_name_about
            # case PAGE_ID.PAGE_NOT_FOUND:
            #     name = self.__template_name_404
            case _:
                return False
        return name

    def get_page_route_name_from_page_id(self, page_id: PAGE_ID) -> bool | str:
        match page_id:
            case PAGE_ID.LOGIN:
                name = self.__route_name_login
            case PAGE_ID.LOGOUT:
                name = self.__route_name_logout
            case PAGE_ID.ACCOUNT_MAIN:
                name = self.__route_name_account_main
            case PAGE_ID.ACCOUNT_CONFIG:
                name = self.__route_name_account_config
            case PAGE_ID.INDEX:
                name = self.__route_name_index
            case PAGE_ID.ABOUT:
                name = self.__route_name_about
            # case PAGE_ID.PAGE_NOT_FOUND:
            #     name = self.__route_name_404
            case _:
                return False
        return name

    def set_render_page(self, page_id: PAGE_ID, **variables):
        name = self.get_page_template_name_from_page_id(page_id)

        self.__debug_unit.debug_print(page_id, name)
        if name is not False:
            if len(name) > 0:
                self.__debug_unit.debug_print(f"Найден шаблон {name}. Прогружаю!")
                print(variables)
                return render_template(f"{name}.html", errors=variables)
        self.__debug_unit.debug_print(f"Не найден шаблон {name}. Прогружаю 404!")
        return render_template(f"{self.__template_name_404}.html")

    def redirect_on_page(self, page_id: PAGE_ID):
        name = self.get_page_route_name_from_page_id(page_id)
        self.__debug_unit.debug_print(page_id, name)
        if name is not False:
            if len(name) > 0:
                self.__debug_unit.debug_print(f"Найден роут {name}. Редиректую!")
                return redirect(f"/{name}")
        self.__debug_unit.debug_print(f"Не найден роут {name}. Редиректую 404!")
        return redirect(f"/{self.__route_name_404}")
