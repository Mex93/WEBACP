
class CBSettings {
    cb_FieldType = {
        CB_TIMEOUT: 0,
    }
    #cbFieldValue = [];
    #cbFieldID = [];
    constructor()
    {
        for(let i = 0; i < this.cb_FieldType.length; i++)
        {
            this.#cbFieldValue.push(null);
            this.#cbFieldID.push(null);
        }
    }
    updateCBValue(cbType, cbValue)
    {
        this.#cbFieldValue[cbType.value] = cbValue;
    }
    updateCBFieldID(cbType, cbID)
    {
        this.#cbFieldID[cbType.value] = cbID;
    }
    deleteCBFieldID(cbType, cbID)
    {
        this.#cbFieldID[cbType.value] = null;
    }
    deleteCBValue(cbType, cbValue)
    {
        this.#cbFieldValue[cbType.value] = null;
    }
    getCBValue(cbType)
    {
        return this.#cbFieldValue[cbType.value];
    }
    getCBFieldID(cbType)
    {
        return this.#cbFieldID[cbType.value];
    }
}

export {
    CBSettings
}