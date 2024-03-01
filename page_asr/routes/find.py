from flask import json
from engine.pages.enums import PAGE_ID
from page_account.account import bp_page_account

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser
from engine.debug.CDebug import CDebug

from engine.users.enums import USER_SECTIONS_TYPE, USER_SECTION_ACCESS_TYPE

from engine.users.CSQLUserQuerys import CSQLUserQuerys
from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_OBJECT_TYPE, LOG_SUBTYPE
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData

from engine.common import get_current_unix_time
from engine.users.common import MAX_ACTIVITY_TIME_LEFT

cdebug = CDebug()
cdebug.debug_system_on(True)
cpages = CPages(cdebug)

cuser_access = CUserAccess()
cuser = CUser()

