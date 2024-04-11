import re
import engine.asr.common as ccommon


class CASR:

    def __init__(self):
        # TODO Возможно сломана проверка регулярок
        pass

    @staticmethod
    def is_asr_valid(text: str) -> bool:
        if re.search(r'[^A-Z0-9]', text):
            return False
        return True

    @staticmethod
    def check_asr_text(asr: str) -> bool:
        if isinstance(asr, str):
            if (CASR.check_asr(asr) is True or
                    CASR.check_mac(asr) is True or
                    CASR.check_sn(asr) is True):
                return True
        return False

    @classmethod
    def check_asr(cls, asr: str) -> bool:
        lenpass = len(asr)

        if ccommon.ASR_TEXT_LEN <= lenpass <= ccommon.ASR_TEXT_LEN:
            if asr.find("ASR") != -1:
                if re.search(r'[^A-Z0-9]', asr) is None:
                    return True
        return False

    @classmethod
    def check_mac(cls, text) -> bool:
        if text.find(":") != -1:
            lenpass = len(text)
            if 16 <= lenpass <= 18:
                if re.search(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', text) is None:
                    return True
        return False

    @classmethod
    def check_sn(cls, text) -> bool:
        lenpass = len(text)
        if 17 <= lenpass <= 50:
            return True
        return False
