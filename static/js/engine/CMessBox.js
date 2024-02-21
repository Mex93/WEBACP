class CMessBox
{
    #success_message = false;
    #blockID = null;
    #textHeaderID = null;
    #textErrorID = null;
    #allertBlock = null;
    #timerHideMessageBox = undefined;
    constructor(placeClassID)
    {
        if (typeof placeClassID === 'string')
        {
            if(placeClassID.indexOf("error") !== -1)
            {
                this.#success_message = true;

                let form_place = document.getElementById(placeClassID);
                if(form_place != null)
                {
                    let main_div = document.createElement("div");
                    main_div.className = "error_form_box";
                    let allert_div = document.createElement("div");
                    allert_div.className = "alert";
                    this.#allertBlock = allert_div;
                    main_div.append(allert_div);
                    form_place.append(main_div);

                    let span_btn = document.createElement("span");
                    span_btn.className = "closebtn";
                    span_btn.onclick = function () {form_place.style.display='none';};
                    span_btn.innerHTML = "&times;";
                    allert_div.append(span_btn);
                    //

                    let strong_alert = document.createElement("strong");
                    let span_header_strong  = document.createElement("span");
                    span_header_strong.id = "error_header";
                    span_header_strong.className = "header_text";
                    strong_alert.append(span_header_strong)
                    allert_div.append(strong_alert)

                    let span_text_strong  = document.createElement("span");
                    span_text_strong.id = "error_text";
                    span_text_strong.className = "main_text";
                    allert_div.append(span_text_strong)

                    form_place.style.display='none'
                    this.#blockID = form_place
                    this.#textHeaderID = span_header_strong;
                    this.#textErrorID = span_text_strong;

                }
            }
        }
    }

    #isMessageShow()
    {
        if(this.#timerHideMessageBox !== undefined)
        {
            return true;
        }
        return false;
    }

    #hideMessage()
    {
        this.#timerHideMessageBox = undefined;
        this.#blockID.style.display='none';
    }
    hide()
    {
        if(this.#isMessageShow())
        {
            clearTimeout(this.#timerHideMessageBox);
            this.#hideMessage();
        }
    }

    #startTimer()
    {
        if(this.#isMessageShow())
        {
            clearTimeout(this.#timerHideMessageBox);
        }
        let me = this;  // иначе ссылаться будет на глобальный объект а не класс
        this.#timerHideMessageBox = setTimeout(function () {
            me.#hideMessage()
        }, 3000);
    }


    #sendMessage(header, text = "")
    {
        this.#startTimer();
        let onlyMessage = false;
        if(text === '' && header !== "")
        {
            onlyMessage = true;
        }
        this.#textHeaderID.innerText = header;
        if(onlyMessage === false)
        {
            this.#textHeaderID.innerHTML = header + "<br>";
            this.#textErrorID.innerText = text;
        }
        else
        {
            this.#textErrorID.innerText = text;
        }
        this.#blockID.style.display='';
    }


    sendErrorMessage(header, text = "")
    {
        if(this.isMessageCreated())
        {
            this.#allertBlock.className = "alert error";
            this.#sendMessage(header, text);
        }
    }
    sendSuccessMessage(header, text = "")
    {
        if(this.isMessageCreated())
        {
            this.#allertBlock.className = "alert success";
            this.#sendMessage(header, text);
        }
    }
    sendInfoMessage(header, text = "")
    {
        if(this.isMessageCreated())
        {
            this.#allertBlock.className = "alert info";
            this.#sendMessage(header, text);
        }
    }
    sendWarningMessage(header, text = "")
    {
        if(this.isMessageCreated())
        {
            this.#allertBlock.className = "alert warning";
            this.#sendMessage(header, text);
        }
    }
    isMessageCreated()
    {
        return this.#success_message;
    }

}

export {
    CMessBox
}