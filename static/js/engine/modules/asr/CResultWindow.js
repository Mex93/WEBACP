

class ResultWindow
{
    #blockID = undefined;
    constructor(blockID)
    {
        if(blockID && blockID.loadAnimBlock && blockID.asrResultBlock)
        {
            this.#blockID = {...blockID};
        }
    }
    showResultBox(status)
    {
        Object.values(this.#blockID).forEach(function(values) {
            if(values !== null)
            {
                if(status)
                {
                    values.style.display = "block";
                }
                else values.style.display = "none";
            }
        });
    }
    showResultTable(status)
    {
        if(this.#blockID.asrResultBlock)
        {
            if(status)
            {
                this.#blockID.asrResultBlock.style.display = "block";
            }
            else this.#blockID.asrResultBlock.style.display = "none";
        }
    }
    showAnimBox(status)
    {
        if(this.#blockID.loadAnimBlock)
        {
            if(status)
            {
                this.#blockID.loadAnimBlock.style.display = "block";
            }
            else this.#blockID.loadAnimBlock.style.display = "none";
        }
    }
}



export {
    ResultWindow,
}