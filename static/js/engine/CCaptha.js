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
}

export {
    CCaptha
}