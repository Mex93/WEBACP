from engine.tv_models.enums import MODELS_TYPE


class CModels:
    def __init__(self):
        pass

    @staticmethod
    def get_model_typename_for_type(model_id: MODELS_TYPE) -> str:
        match model_id:
            case MODELS_TYPE.TVS:
                return "Телевизор"
            case MODELS_TYPE.MONITORS:
                return "Монитор"
            case MODELS_TYPE.INTERACTIV_PANEL:
                return "Интерактивная панель"

        return "Неизвестно"

    @staticmethod
    def get_model_type_from_model_name(model_name: str) -> MODELS_TYPE:
        if model_name.find("MNT ") != -1:
            return MODELS_TYPE.MONITORS
        elif model_name.find("TV ") != -1:
            return MODELS_TYPE.TVS
        elif model_name.find("IPANEL ") != -1:
            return MODELS_TYPE.INTERACTIV_PANEL
        return MODELS_TYPE.NONE

    @staticmethod
    def get_model_type_name_prefics(model_id: MODELS_TYPE) -> str:
        match model_id:
            case MODELS_TYPE.TVS:
                return "TV "
            case MODELS_TYPE.MONITORS:
                return "MNT "
            case MODELS_TYPE.INTERACTIV_PANEL:
                return "IPANEL "

        return "-"

    @staticmethod
    def get_parced_name_and_type(tv_name: str) -> tuple:

        device_type = CModels.get_model_type_from_model_name(tv_name)

        if device_type == MODELS_TYPE.MONITORS:  # Мониторы
            tv_name = tv_name.replace(CModels.get_model_type_name_prefics(device_type), "")

        elif device_type == MODELS_TYPE.TVS:  # TV
            tv_name = tv_name.replace(CModels.get_model_type_name_prefics(device_type), "")

        elif device_type == MODELS_TYPE.INTERACTIV_PANEL:  # TV
            tv_name = tv_name.replace(CModels.get_model_type_name_prefics(device_type), "")

        else:
            tv_name = tv_name.replace(CModels.get_model_type_name_prefics(device_type), "")

        result_tup = (tv_name, CModels.get_model_typename_for_type(device_type))
        return result_tup


