import re
import engine.asr.common as ccommon


class CASR:

    def __init__(self):
        pass

    @staticmethod
    def is_asr_valid(text: str) -> bool:
        if re.search(r'[^A-Z0-9]', text):
            return False
        return True

    @staticmethod
    def check_asr_text(asr: str) -> bool:
        if isinstance(asr, str):
            lenpass = len(asr)
            if ccommon.ASR_TEXT_LEN <= lenpass <= ccommon.ASR_TEXT_LEN:
                if asr.find("ASR") != -1:
                    if CASR.is_asr_valid(asr):
                        return True
        return False
