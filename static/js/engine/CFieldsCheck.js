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

    #re_Password = new RegExp(/[^a-zA-Z0-9]/);
    #re_Nickname = new RegExp(/[^a-zA-Z0-9]/);
    #re_Email = new RegExp(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/);
    #re_Lastname = new RegExp(/[^а-яА-Я]/);

    constructor() {

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
        if (text && field && maxLen && minLen && rePattern && textPattern)
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
                    if(!rePattern.test(field))
                    {
                        errorObj.result = true
                        errorObj.errorText = `Validator Success !`
                    }
                    else errorObj.errorText = `${text} должен состоять из символов ${textPattern}`
                }
                else errorObj.errorText = `Размер ${text} от ${minLen} до ${maxLen}`
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