class CWindowBox
{
    #blockDiv = null;
    #blockText = null;
    #blockHeader = null;
    #Timer = undefined;
    #defaultBCKC = "lightgrey";
    constructor() {

        let myWindow = document.createDocumentFragment();
        let main_div = document.createElement("div");
        main_div.id = "box_window_message";
        main_div.className = "box-window-common";
        let me = this;
        main_div.onclick = function () {me.hide()};


        let header_div = document.createElement("div");
        header_div.className = "header";
        header_div.id = "message-header";
        main_div.append(header_div);

        let text_div = document.createElement("div");
        text_div.className = "message";
        text_div.id = "message-text";
        main_div.append(text_div);

        myWindow.append(main_div);
        document.body.append(myWindow);

        this.#blockDiv = main_div;
        this.#blockText = text_div;
        this.#blockHeader = header_div;
        main_div.style.display='none'

        let poxX = document.documentElement.ClientWidth/2;
        let poxY = document.documentElement.ClientHeight/2;
        main_div.style.left = poxX + myWindow.offsetWidth/2 + "px";
        main_div.style.top = poxY + myWindow.offsetHeight/2 + "px";

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
    show(header, message, style, showTime = 3000)
    {
        if(message.length > 0)
        {
            this.#blockText.innerText = message
            this.#blockHeader.innerText = header
            const styles = window.getComputedStyle(this.#blockDiv);
            let oldB = styles.backgroundColor;
            // if(style.length > 0)
            // {
            //     if(style !== oldB)
            //     {
            //         this.#blockDiv.style.backgroundColor = style;
            //     }
            // }
            // else
            // {
            //     if(this.#defaultBCKC !== oldB)
            //     {
            //         this.#blockDiv.style.backgroundColor = this.#defaultBCKC;
            //     }
            // }
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