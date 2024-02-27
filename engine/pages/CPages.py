from flask import Flask, render_template, request, redirect, url_for, session

from engine.pages.enums import PAGE_ID
from engine.users.CUserAccess import CUserAccess
from engine.users.enums import USER_SECTIONS_TYPE, USER_SECTION_ACCESS_TYPE
from engine.users.enums import USER_ALEVEL

class CPages:
    def __init__(self, cdebug):
        # templates
        path_to_accounts_module = "page_account"
        path_to_based_module = ""
        # templates name
        self.__template_name_login = 'login'
        self.__template_name_logout = 'logout'
        self.__template_name_account_main = 'main'
        self.__template_name_account_config = 'config'
        self.__template_name_index = 'index'
        self.__template_name_about = 'about'
        self.__template_name_404 = '404'

        # templates path
        self.__template_path_account_login = f'{path_to_accounts_module}/login'
        self.__template_path_account_logout = f'{path_to_accounts_module}/logout'
        self.__template_path_account_main = f'{path_to_accounts_module}/main'
        self.__template_path_account_config = f'{path_to_accounts_module}/config'
        self.__template_path_404 = '404'
        self.__template_path_about = 'about'
        self.__template_path_index = 'index'


        # url routs
        self.__route_name_login = 'account/login'
        self.__route_name_logout = 'account/logout'
        self.__route_name_account_main = 'account/'
        self.__route_name_account_config = 'account/config'

        self.__route_name_index = 'index'
        self.__route_name_about = 'about'
        self.__route_name_404 = '404'

        self.__debug_unit = cdebug

    @staticmethod
    def is_url_in_modules(url: str) -> bool:
        url_path = url.strip("/")
        if len(url_path) > 1:
            for item in url_path:
                if item is False:
                    return False
        return True

    def get_template_path_from_page_id(self, page_id: PAGE_ID):
        match page_id:
            case PAGE_ID.LOGIN:
                name = self.__template_path_account_login
            case PAGE_ID.LOGOUT:
                name = self.__template_path_account_logout
            case PAGE_ID.ACCOUNT_MAIN:
                name = self.__template_path_account_main
            case PAGE_ID.ACCOUNT_CONFIG:
                name = self.__template_path_account_config
            case PAGE_ID.INDEX:
                name = self.__template_path_index
            case PAGE_ID.ABOUT:
                name = self.__template_path_about
            # case PAGE_ID.PAGE_NOT_FOUND:
            #     name = self.__template_path_404
            case _:
                return False
        return name

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
        name = self.get_template_path_from_page_id(page_id)

        self.__debug_unit.debug_print(page_id, name)
        if name is not False:
            if len(name) > 0:
                self.__debug_unit.debug_print(f"Найден шаблон {name}. Прогружаю!")
                print(variables)
                access_unit = CUserAccess()
                return render_template(f"{name}.html", access_unit=access_unit,
                                       access_section=USER_SECTION_ACCESS_TYPE,
                                       alevel=USER_ALEVEL,
                                       access_type=USER_SECTIONS_TYPE,
                                       var_values=variables)
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
