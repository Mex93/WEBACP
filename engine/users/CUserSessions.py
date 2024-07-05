from flask import session
from engine.users.enums import USER_SECTIONS_TYPE, USER_SECTION_ACCESS_TYPE


class CUserSessions:

    def __init__(self):
        self.__sname_acc_index = "acc_index"
        self.__sname_nickname = "nickname"
        self.__sname_firstname = "firstname"
        self.__sname_lastname = "lastname"

        self.__sname_last_login_date = "last_login_date"
        self.__sname_alevel = "alevel"
        self.__sname_account_timeout_exit = "account_timeout_exit"
        self.__sname_account_timeout_exit_time = "account_timeout_exit_time"

        self.__sname_account_save_me_time = "account_sme_time"
        self.__sname_account_check_sessions = "account_check_sess"

        self.__sname_account_disabled = "account_disabled"
        self.__sname_account_dis_aindex = "account_dis_aindex"
        self.__sname_account_dis_date = "account_dis_date"

        self.__sname_account_checker_time = "account_checker_time"

        self.__sname_access_scan_edit = "access_scan_edit"
        self.__sname_access_scan_add = "access_scan_add"
        self.__sname_access_scan_delete = "access_scan_delete"
        self.__sname_access_scan_find = "access_scan_find"

        self.__sname_access_sn_edit = "access_sn_edit"
        self.__sname_access_sn_add = "access_sn_add"
        self.__sname_access_sn_delete = "access_sn_delete"
        self.__sname_access_sn_find = "access_sn_find"

        self.__sname_access_asr_edit = "access_asr_edit"
        self.__sname_access_asr_add = "access_asr_add"
        self.__sname_access_asr_delete = "access_asr_delete"
        self.__sname_access_asr_find = "access_asr_find"

        self.__sname_access_pallet_delete_all = "access_pallet_delete_all"
        self.__sname_access_pallet_add_tv = "access_pallet_add_tv"
        self.__sname_access_pallet_delete_device = "access_pallet_delete_device"
        self.__sname_access_pallet_changed_info = "access_pallet_changed_info"
        self.__sname_access_pallet_changed_status = "access_pallet_changed_status"
        self.__sname_access_pallet_find = "access_pallet_find"

        self.__session_start_text = "session_start"

    def __get_session_var_name_from_type(self, session_type: USER_SECTIONS_TYPE) -> bool | str:
        match session_type:
            case USER_SECTIONS_TYPE.ACC_INDEX:
                return self.__sname_acc_index
            case USER_SECTIONS_TYPE.NICKNAME:
                return self.__sname_nickname
            case USER_SECTIONS_TYPE.FIRSTNAME:
                return self.__sname_firstname
            case USER_SECTIONS_TYPE.LASTNAME:
                return self.__sname_lastname
            case USER_SECTIONS_TYPE.LAST_LOGIN_DATE:
                return self.__sname_last_login_date
            case USER_SECTIONS_TYPE.ALEVEL:
                return self.__sname_alevel
            case USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT:
                return self.__sname_account_timeout_exit
            case USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT_TIME:
                return self.__sname_account_timeout_exit_time
            case USER_SECTIONS_TYPE.ACCOUNT_SAVE_ME_START_TIME:
                return self.__sname_account_save_me_time
            case USER_SECTIONS_TYPE.ACCOUNT_CHECKER_ACC_FIND_TIME:
                return self.__sname_account_checker_time
            case USER_SECTIONS_TYPE.ACCOUNT_CHECK_SESSIONS:
                return self.__sname_account_check_sessions
            case USER_SECTIONS_TYPE.ACCOUNT_DISABLED:
                return self.__sname_account_disabled
            case USER_SECTIONS_TYPE.ACCOUNT_DIS_AINDEX:
                return self.__sname_account_dis_aindex
            case USER_SECTIONS_TYPE.ACCOUNT_DIS_DATE:
                return self.__sname_account_dis_date

            case USER_SECTIONS_TYPE.ACCESS_SCAN_EDIT:
                return self.__sname_access_scan_edit
            case USER_SECTIONS_TYPE.ACCESS_SCAN_DELETE:
                return self.__sname_access_scan_delete
            case USER_SECTIONS_TYPE.ACCESS_SCAN_ADD:
                return self.__sname_access_scan_add
            case USER_SECTIONS_TYPE.ACCESS_SCAN_FIND:
                return self.__sname_access_scan_find

            case USER_SECTIONS_TYPE.ACCESS_SN_EDIT:
                return self.__sname_access_sn_edit
            case USER_SECTIONS_TYPE.ACCESS_SN_DELETE:
                return self.__sname_access_sn_delete
            case USER_SECTIONS_TYPE.ACCESS_SN_ADD:
                return self.__sname_access_sn_add
            case USER_SECTIONS_TYPE.ACCESS_SN_FIND:
                return self.__sname_access_sn_find

            case USER_SECTIONS_TYPE.ACCESS_ASR_EDIT:
                return self.__sname_access_asr_edit
            case USER_SECTIONS_TYPE.ACCESS_ASR_DELETE:
                return self.__sname_access_asr_delete
            case USER_SECTIONS_TYPE.ACCESS_ASR_ADD:
                return self.__sname_access_asr_add
            case USER_SECTIONS_TYPE.ACCESS_ASR_FIND:
                return self.__sname_access_asr_find

            case USER_SECTIONS_TYPE.ACCESS_PALLET_CHANGED_STATUS:
                return self.__sname_access_pallet_changed_status
            case USER_SECTIONS_TYPE.ACCESS_PALLET_CHANGED_INFO:
                return self.__sname_access_pallet_changed_info
            case USER_SECTIONS_TYPE.ACCESS_PALLET_ADD_TV:
                return self.__sname_access_pallet_add_tv
            case USER_SECTIONS_TYPE.ACCESS_PALLET_DELETE_ALL:
                return self.__sname_access_pallet_delete_all
            case USER_SECTIONS_TYPE.ACCESS_PALLET_DELETE_DEVICE:
                return self.__sname_access_pallet_delete_device
            case USER_SECTIONS_TYPE.ACCESS_PALLET_FIND:
                return self.__sname_access_pallet_find


        return False

    def is_sessions_start(self) -> bool:
        if self.__session_start_text in session:
            if session.get(self.__session_start_text) == 1:
                return True
        return False

    def sessions_start(self):
        session[self.__session_start_text] = 1
        session.modified = True

    def sessions_end(self) -> bool:
        if self.__session_start_text in session:
            if session.get(self.__session_start_text) == 1:
                session.pop(self.__session_start_text, None)
                session.modified = True
                return True
        return False

    def get_session_var(self, session_type: USER_SECTIONS_TYPE):
        sess_name = self.__get_session_var_name_from_type(session_type)
        if sess_name is not False:
            return session.get(sess_name)
        return False

    def set_session_var(self, session_type: USER_SECTIONS_TYPE, var) -> bool:
        sess_name = self.__get_session_var_name_from_type(session_type)
        if sess_name is not False:
            session[sess_name] = var
            session.modified = True
            return True
        return False

    def pop_session_var(self, session_type: USER_SECTIONS_TYPE):
        sess_name = self.__get_session_var_name_from_type(session_type)
        if sess_name in session:
            session.pop(sess_name, None)
            session.modified = True
            return True
        return False

    def delete_all_user_sessions(self):
        self.sessions_end()
        for enum_id in USER_SECTIONS_TYPE:
            sess_name = self.__get_session_var_name_from_type(enum_id)
            if sess_name is not False:
                session.pop(sess_name, None)
                session.modified = True




