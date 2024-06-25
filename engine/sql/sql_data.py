# Название всех таблиц скрипта
class SQL_TABLE_NAME:
    user_accounts = "acp_users"
    assembled_tv = "assembled_tv"
    asr_tv = "unfinished_tv"
    tv_model_info_tv = "tv"
    user_logs = "acp_log"
    tv_scan_type = "public.tv_scan_type"


# Название полей в конфиге готовых тв
class SQL_ASSEMBLED_TV_FIELDS:
    fd_assy_id = "assy_id"
    fd_tvfk = "tv_fk"
    fd_linefk = "line_fk"  # Линия вторичный ключ
    fd_tv_sn = "tv_sn"
    fd_tv_mac = "ethernet_mac"
    fd_tv_mb_sn = "mainboard_sn"
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


class SQL_ASR_FIELDS:
    asr_fd_tv_asr_id = "tv_asr_id"
    asr_fd_tv_asr_name = "tv_asr"
    asr_fd_tv_fk = "tv_fk"
    asr_fd_line_fk = "line_fk"
    asr_fd_wifi_module_sn = "wifi_module_sn"
    asr_fd_bt_module_sn = "bt_module_sn"
    asr_fd_ethernet_mac = "ethernet_mac"
    asr_fd_lcm_sn = "lcm_sn"
    asr_fd_oc_sn = "oc_sn"
    asr_fd_mainboard_sn = "mainboard_sn"
    asr_fd_powerboard_sn = "powerboard_sn"
    asr_fd_tcon_sn = "tcon_sn"
    asr_fd_timestamp_st10 = "timestamp_st10"
    asr_fd_ops_sn = "ops_sn"


class SQL_TV_MODEL_INFO_FIELDS:
    tvmi_fd_tv_id = "tv_id"
    tvmi_fd_tv_name = "tv_name"
    tvmi_fd_vendor_code = "vendor_code"
    tvmi_fd_tv_platform_fk = "tv_platform_fk"
    tvmi_fd_scan_type_fk = "scan_type_fk"
    tvmi_fd_software_type_fk = "software_type_fk"
    tvmi_fd_tv_serial_number_template = "tv_serial_number_template"
    tvmi_fd_last_update_time = "last_updated_time"

    tvmi_fd_tv_model_type_name = "model_type_name"  # фальш филды. в бд таких нет. нужно для расчёта


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


class SQL_MASK_FIELDS:

    mfd_scan_type_id = 'scan_type_id'
    mfd_scan_name = 'type_name'

    mfd_scan_wifi_module_sn = 'scan_wifi_module_sn'
    mfd_wifi_module_sn_template = 'wifi_module_sn_template'

    mfd_scan_bt_module_sn = 'scan_bt_module_sn'
    mfd_bt_module_sn_template = 'bt_module_sn_template'

    mfd_scan_ethernet_mac = 'scan_ethernet_mac'
    mfd_ethernet_mac_sn_template = 'ethernet_mac_sn_template'

    mfd_scan_lcm_sn = 'scan_lcm_sn'
    mfd_lcm_sn_template = 'lcm_sn_template'

    mfd_scan_oc_sn = 'scan_oc_sn'
    mfd_oc_sn_template = 'oc_sn_template'

    mfd_scan_mainboard_sn = 'scan_mainboard_sn'
    mfd_mainboard_sn_template = 'mainboard_sn_template'

    mfd_scan_powerboard_sn = 'scan_powerboard_sn'
    mfd_powerboard_sn_template = 'powerboard_sn_template'

    mfd_scan_tcon_sn = 'scan_tcon_sn'
    mfd_tcon_sn_template = 'tcon_sn_template'

    mfd_scan_ops_sn = 'scan_ops_sn'
    mfd_ops_sn_template = 'ops_sn_template'

    mfd_scan_ops_mac = 'scan_ops_mac'
    mfd_ops_mac_template = 'ops_mac_template'

    mfd_scan_mac_usbc = 'scan_mac_usbc'
    mfd_mac_usbc_template = 'mac_usbc_template'

    mfd_scan_storage_sn = 'scan_storage_sn'
    mfd_storage_template = 'storage_template'
