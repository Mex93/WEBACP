class CFieldsCheck
{
    #MAX_USER_NICKNAME_LEN = 35;
    #MIN_USER_NICKNAME_LEN = 4;

    #MAX_USER_FIRSTNAME_LASTNAME_LEN = 20;
    #MIN_USER_FIRSTNAME_LASTNAME_LEN = 4;

    #MAX_USER_EMAIL_LEN = 35;
    #MIN_USER_EMAIL_LEN = 4;

    #MAX_USER_PASSWORD_LEN = 16;
    #MIN_USER_PASSWORD_LEN = 6;

    #re_ASR = new RegExp(/[^A-Z0-9]/);
    #re_Password = new RegExp(/[^a-zA-Z0-9]/);
    #re_Nickname = new RegExp(/[^a-zA-Z0-9]/);
    #re_Email = new RegExp(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/);
    #re_Lastname = new RegExp(/[^а-яА-Я]/);
    #re_MAC = new RegExp(/^\d{2}:\d{2}:\d{2}:\d{2}:\d{2}:\d{2}$/);  //04:06:DD:9A:48:22/^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/
    // TODO придумать как написать эту ебучую регулярку на проверку asr + in python
    #re_MBSN =  null;

    #ASR_TEXT_LEN = 8;

    constructor() {

    }
    set_check_asr(field)
    {
        if (typeof field === 'string')
        {
            let errorObj = {
                result: false,
                errorText: ""
            }

            if(field.indexOf("ASR") !== -1)
            {
                let dataObj = {
                    field: field,
                    text: "ASR",
                    textPattern: "A-Z,0-9",
                    maxLen: this.#ASR_TEXT_LEN,
                    minLen: this.#ASR_TEXT_LEN,
                    rePattern: this.#re_ASR
                }
                return this.#set_check_validator(dataObj)
            }
            else errorObj.errorText = `Название должно начинаться с 'ASR...'!`
            return errorObj
        }
        return false
    }
    set_check_mac(field)
    {
        if (typeof field === 'string')
        {
            let errorObj = {
                result: false,
                errorText: ""
            }
            if(field.indexOf(":") !== -1)
            {
                let dataObj = {
                    field: field,
                    text: "MAC",
                    textPattern: "XX:XX:XX:XX:XX:XX",
                    maxLen: 18,
                    minLen: 16,
                    rePattern: this.#re_MAC
                }
                return this.#set_check_validator(dataObj)
            }
            else errorObj.errorText = `MAC должен быть формата 'XX:XX:XX:XX:XX:XX'!`
            return errorObj
        }
        return false
    }
    set_check_ms_sn(field)
    {
        if (typeof field === 'string')
        {
            let errorObj = {
                result: false,
                errorText: ""
            }

            let dataObj = {
                field: field,
                text: "MB SN",
                textPattern: "-",
                maxLen: 50,
                minLen: 17,
                rePattern: this.#re_MBSN
            }
            return this.#set_check_validator(dataObj)
        }
        return false
    }
    set_check_password(field)
    {
        if (typeof field === 'string')
        {
            let dataObj = {
                field: field,
                text: "Пароль",
                textPattern: "A-Z,a-z,0-9",
                maxLen: this.#MAX_USER_PASSWORD_LEN,
                minLen: this.#MIN_USER_PASSWORD_LEN,
                rePattern: this.#re_Password
            }
            return this.#set_check_validator(dataObj)
        }
        return false
    }
    set_check_nickname(field)
    {
        if (typeof field === 'string')
        {
            let dataObj = {
                field: field,
                text: "Логин",
                textPattern: "A-Z,a-z,0-9",
                maxLen: this.#MAX_USER_NICKNAME_LEN,
                minLen: this.#MIN_USER_NICKNAME_LEN,
                rePattern: this.#re_Nickname
            }
            return this.#set_check_validator(dataObj)
        }
        return false
    }
    set_check_email(field)
    {
        if (typeof field === 'string')
        {
            let dataObj = {
                field: field,
                text: "Email",
                textPattern: "A-Z,a-z,0-9,@",
                maxLen: this.#MAX_USER_EMAIL_LEN,
                minLen: this.#MIN_USER_EMAIL_LEN,
                rePattern: this.#re_Email
            }
            return this.#set_check_validator(dataObj)
        }
        return false
    }

    set_check_last_first_name(field)
    {
        if (typeof field === 'string')
        {
            let dataObj = {
                field: field,
                text: "Имя или фамилия",
                textPattern: "а-я,А-Я",
                maxLen: this.#MAX_USER_FIRSTNAME_LASTNAME_LEN,
                minLen: this.#MIN_USER_FIRSTNAME_LASTNAME_LEN,
                rePattern: this.#re_Lastname
            }
            return this.#set_check_validator(dataObj)
        }
        return false
    }

    #set_check_validator({ field, text, textPattern, maxLen, minLen, rePattern })
    {
        if (text && field && maxLen && minLen && textPattern)
        {
            let errorObj = {
                result: false,
                errorText: ""
            }
            if (typeof field === 'string')
            {
                let len = field.length
                if(len >= minLen && len <= maxLen)
                {
                    if(rePattern !== null)
                    {
                        if(rePattern.test(field))
                        {
                            errorObj.errorText = `${text} должен состоять из символов ${textPattern}`
                            return false;
                        }
                    }

                    errorObj.result = true
                    errorObj.errorText = `Validator Success !`
                }
                else errorObj.errorText = `Размер ${text} от ${minLen} до ${maxLen} символов`
            }
            else errorObj.errorText = `Филда не строка!`
            return errorObj
        }
        return false
    }
}


export {
    CFieldsCheck,
}