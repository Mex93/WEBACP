from engine_scripts.py.pages.enums import PAGE_ID
from flask import Flask, render_template, request, redirect, url_for, session


class CPages:
    def __init__(self, debug_unit):
        self.__page_name_login = 'login'
        self.__page_name_logout = 'logout'
        self.__page_name_account_main = 'account_main'
        self.__page_name_account_config = 'account_config'

        self.__page_name_index = 'index'
        self.__page_name_about = 'about'
        self.__page_name_404 = '404'

        self.__debug_unit = debug_unit

    def get_page_template_name_from_page_id(self, page_id: PAGE_ID) -> bool | str:
        match page_id:
            case PAGE_ID.LOGIN:
                name = self.__page_name_login
            case PAGE_ID.LOGOUT:
                name = self.__page_name_logout
            case PAGE_ID.ACCOUNT_MAIN:
                name = self.__page_name_account_main
            case PAGE_ID.ACCOUNT_CONFIG:
                name = self.__page_name_account_config
            case PAGE_ID.INDEX:
                name = self.__page_name_index
            case PAGE_ID.ABOUT:
                name = self.__page_name_about
            # case PAGE_ID.PAGE_NOT_FOUND:
            #     name = self.__page_name_404
            case _:
                return False
        return name

    def set_render_page(self, page_id: PAGE_ID, *kwargs):
        name = self.get_page_template_name_from_page_id(page_id)

        self.__debug_unit.debug_print(page_id, name)
        if name is not False:
            if len(name) > 0:
                self.__debug_unit.debug_print(f"Найден шаблон {name}. Прогружаю!")
                return render_template(f"{name}.html", kwargs)
        self.__debug_unit.debug_print(f"Не найден шаблон {name}. Прогружаю 404!")
        return render_template(f"{self.__page_name_404}.html")

    def redirect_on_page(self, page_id: PAGE_ID):
        name = self.get_page_template_name_from_page_id(page_id)
        self.__debug_unit.debug_print(page_id, name)
        if name is not False:
            if len(name) > 0:
                self.__debug_unit.debug_print(f"Найден шаблон {name}. Редиректую!")
                return redirect(f"/{name}")
        self.__debug_unit.debug_print(f"Не найден шаблон {name}. Редиректую 404!")
        return redirect(f"/{self.__page_name_404}")
