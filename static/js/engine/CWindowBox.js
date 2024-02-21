class CWindowBox
{
    #blockDiv = null;
    #blockText = null;
    #Timer = undefined;
    #defaultBCKC = "lightgrey";
    constructor(beforeElementName) {

        if (typeof beforeElementName === 'string')
        {
            let id_div = document.createElement("div");
            id_div.id = "box_window_message";
            id_div.className = "box-window-common";
            let me = this;
            id_div.onclick = function () {me.hide()};

            let span = document.createElement("span")
            span.id = "message-text";
            id_div.append(span);


            this.#blockDiv = id_div;
            this.#blockText = span;
            id_div.style.display='none'


            let formID = document.getElementById(beforeElementName)
            if(formID !== null)
            {
                formID.append(id_div);
            }
            else
            {
                document.body.append(id_div);
            }
        }


    }
    #stopTimer()
    {
        if(this.#Timer !== undefined)
        {
            clearTimeout(this.#Timer);
            this.#Timer = undefined;
        }
    }
    hide()
    {
        this.#stopTimer();
        this.#blockDiv.style.display='none'
    }
    show(message, style, showTime = 3000)
    {
        if(message.length > 0)
        {
            this.#blockText.innerText = message
            const styles = window.getComputedStyle(this.#blockDiv);
            let oldB = styles.backgroundColor;
            if(style.length > 0)
            {
                if(style !== oldB)
                {
                    this.#blockDiv.style.backgroundColor = style;
                }
            }
            else
            {
                if(this.#defaultBCKC !== oldB)
                {
                    this.#blockDiv.style.backgroundColor = this.#defaultBCKC;
                }
            }
            this.#blockDiv.style.display='block'
            this.#stopTimer();
            if(showTime !== 0)
            {
                let me = this;  // иначе ссылаться будет на глобальный объект а не класс
                this.#Timer = setTimeout(function () {
                    me.hide()
                }, showTime);
            }
        }
    }
}

export {
    CWindowBox
}