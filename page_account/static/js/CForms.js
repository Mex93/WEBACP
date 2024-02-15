
class CForms
{
    #FieldID = null
    constructor(FieldID)
    {
        if(typeof FieldID  == "object")
        {
            this.#FieldID = FieldID
        }
    }

    getInputValue()
    {
        console.log(this.#FieldID.value)
        return this.#FieldID.value
    }

    clearField()
    {
        this.#FieldID.value = ""
    }
}

export {
    CForms,
};