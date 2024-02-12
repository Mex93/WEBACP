
# Название всех таблиц скрипта
class SQL_TABLE_NAME:
    user_accounts = "acp_users"
    assembled_tv = "assembled_tv"
    user_logs = "acp_log"


# Название полей в конфиге готовых тв
class SQL_PLAN_SETT_FIELD_NAME_ASSEMBLED_TV:
    fd_assy_id = "assy_id"
    fd_tvfk = "tv_fk"
    fd_linefk = "line_fk"  # Линия вторичный ключ
    fd_tv_sn = "tv_sn"  # Линия вторичный ключ
    fd_completed_date = "timestamp_st100"  # Дата прохождения черезе упаковку


# Название полей в конфиге настройки аккаунта юзеров
class SQL_USERS_FIELDS:
    ufd_index = "user_index"
    ufd_nickname = "user_nickname"
    ufd_firtname = "user_firstname"
    ufd_lastname = "user_lastname"
    ufd_md5pass = "user_md5_pass"
    ufd_last_login_date = "user_last_login_date"
    ufd_admin_level = "user_alevel"
    ufd_account_timeout_exit = "user_timeout_exit"

    ufd_account_disabled = "user_account_disabled"
    ufd_account_dis_aindex = "user_account_dis_aindex"
    ufd_account_dis_date = "user_account_dis_date"

    ufd_user_access_scan_edit = "user_access_scan_edit"
    ufd_user_access_scan_delete = "user_access_scan_delete"
    ufd_user_access_scan_add = "user_access_scan_add"

    ufd_user_access_sn_edit = "user_access_sn_edit"
    ufd_user_access_sn_delete = "user_access_sn_delete"
    ufd_user_access_sn_add = "user_access_sn_add"

    ufd_user_access_asr_edit = "user_access_asr_edit"
    ufd_user_access_asr_delete = "user_access_asr_delete"
    ufd_user_access_asr_add = "user_access_asr_add"

class SQL_LOG_FIELDS:
    lfd_log_index = "log_pk"
    lfd_log_user_id = "user_id"
    lfd_log_object = "log_object"
    lfd_log_type = "log_type"
    lfd_log_sub_type = "log_sub_type"
    lfd_log_text = "log_text"
    lfd_log_date = "log_date"
    lfd_log_ip = "log_ip"
    lfd_log_mac = "log_mac"

