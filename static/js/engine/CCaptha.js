class CCaptha {
    #textID = null;
    #hashID = null;
    constructor(hashSelector, textID) {

        hashSelector= document.querySelector(hashSelector);
        if(hashSelector !== undefined)
        {
            textID = document.getElementById(textID);
            if(textID !== null)
            {
                this.#hashID = hashSelector;
                this.#textID = textID;
            }
        }
    }

    getCorrentData()
    {
        if(this.#hashID !== null)
        {
            if(this.#textID !== null)
            {
                return true;
            }
        }
        return false;
    }
    getHash()
    {
       return this.#hashID.value;
    }
    clearHash()
    {
        this.#hashID.value = "";
    }
    getText()
    {
       return this.#textID.value;
    }
    clearText()
    {
        this.#textID.value = "";
    }

    validate(cmessBox)
    {
        if(!this.getCorrentData())
        {
            cmessBox.sendErrorMessage("Ошибка в обработке данных капчи");
            return false;
        }
        let captcha_hash = this.getHash();
        let captcha_text = this.getText();
        if(!captcha_text || !captcha_hash)
        {
            cmessBox.sendErrorMessage("Вы не ввели капчу");
            return false;
        }
        return {csuccess: true, captcha_hash, captcha_text};
    }

}

export {
    CCaptha
}