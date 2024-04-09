from engine.users.CUserSessions import CUserSessions
from engine.users.enums import USER_SECTIONS_TYPE, USER_SECTION_ACCESS_TYPE


class CUserAccess(CUserSessions):

    def __init__(self):
        super().__init__()

    def is_access_for_panel(self, session_type: USER_SECTIONS_TYPE):
        current_var = self.get_session_var(session_type)
        if current_var is not False:
            if current_var in (False, 0, None):
                return False
            return True

        return False

    def is_avalible_any_access_field(self, session_type: USER_SECTION_ACCESS_TYPE):
        li = list()
        match session_type:
            case USER_SECTION_ACCESS_TYPE.ACCOUNT:
                return self.is_sessions_start()
            case USER_SECTION_ACCESS_TYPE.SN:
                li = (self.get_session_var(USER_SECTIONS_TYPE.ACCESS_SN_ADD),
                      self.get_session_var(USER_SECTIONS_TYPE.ACCESS_SN_EDIT),
                      self.get_session_var(USER_SECTIONS_TYPE.ACCESS_SN_DELETE))
            case USER_SECTION_ACCESS_TYPE.SCAN_TEMPLATES:
                li = (self.get_session_var(USER_SECTIONS_TYPE.ACCESS_SCAN_ADD),
                      self.get_session_var(USER_SECTIONS_TYPE.ACCESS_SCAN_EDIT),
                      self.get_session_var(USER_SECTIONS_TYPE.ACCESS_SCAN_DELETE))
            case USER_SECTION_ACCESS_TYPE.ASR:
                li = (self.get_session_var(USER_SECTIONS_TYPE.ACCESS_ASR_ADD),
                      self.get_session_var(USER_SECTIONS_TYPE.ACCESS_ASR_EDIT),
                      self.get_session_var(USER_SECTIONS_TYPE.ACCESS_ASR_DELETE))

        if len(li) > 0:
            for value in li:
                if value in (True, 1):
                    return True

        return False
