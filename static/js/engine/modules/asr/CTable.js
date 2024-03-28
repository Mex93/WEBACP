import {TABLE_TYPE} from "/static/js/engine/modules/asr/common.js";




class CTable
{

    #tableID = undefined;
    #tableType = undefined;
    #headerID = undefined;
    #bodyArray = undefined;
    #tablePlaceID = undefined;
    #bodyCounts = 0;
    constructor() {

    }
    createTable(placeIDName) {
        let tablePlace = document.getElementById(placeIDName);
        if(tablePlace)
        {
            this.#tablePlaceID = tablePlace;

            this.#tableType = TABLE_TYPE.TYPE_NONE
            this.#headerID = undefined;
            this.#bodyArray = Array();


            let table = document.createElement("table");
            table.id = "result_table"
            table.className = "custom-table"
            this.#tableID = table;
            // tablePlace.innerHTML = table;
            tablePlace.append(table);
            return true;
        }
        return false;
    }
    setType(type)
    {
        if(type !== this.#tableType)
        {
            this.#tableType = type;
            console.log("успех тип задан")
            return true;
        }
        return false;
    }
    getCurrentType()
    {
        return (this.#tableType);
    }
    clearHeader()
    {
        if(this.#headerID !== null)
        {
            let current = document.getElementById(`${this.#headerID}`)
            if(current !== null)
            {
                current.remove();
            }
        }
        this.#headerID = undefined;
    }
    clearBody()
    {
        this.#bodyArray.forEach( (element, index) =>
        {
            if(element)
            {
                let current = document.getElementById(`${element}`)
                if(current !== null)
                {
                    current.remove();
                }
            }
        })
        this.#bodyArray = [];
        this.#bodyCounts = 0;
    }
    destroyTable()
    {
        if(this.#tableID !== undefined)
        {
            this.clearBody();
            this.clearHeader();
            this.#tableID.remove();
        }
    }
    addHeader(headerArr)
    {
        if(Array.isArray(headerArr))
        {
            // header
            let tr = document.createElement("tr");
            //
            headerArr.forEach((element) => {
                let th = document.createElement("th");
                th.innerText = `${element}:`;
                tr.append(th);
            })
            if(this.#tableType === TABLE_TYPE.TYPE_EDITTING)
            {
                let th = document.createElement("th");
                th.innerText = "Новое значение:";
                tr.append(th);
            }

            this.#tableID.append(tr);
            this.#headerID = tr;
            console.log("успех addHeader")
            return true;
        }
    }
    addBody(elementName, currentValue, isNonEdit)
    {
        if(typeof elementName === 'string' && currentValue)
        {
            this.#bodyCounts++;
            // body
            let tr = document.createElement("tr");

            let td = document.createElement("td");
            let span = document.createElement("span");
            span.className = "label";
            span.innerText = elementName;
            td.append(span);
            tr.append(td)

            td = document.createElement("td");
            span = document.createElement("span");
            span.className = "value";
            span.id = `table_element_old_value_${this.#bodyCounts}`;
            span.innerText = currentValue;
            td.append(span);
            tr.append(td)

            //
            if(this.#tableType === TABLE_TYPE.TYPE_EDITTING)
            {
                td = document.createElement("td");
                let input = document.createElement("input");
                input.id = `table_element_new_value_${this.#bodyCounts}`;
                input.name = `table_element_new_value_${this.#bodyCounts}`;  // обработчик формы
                input.type = "text";
                input.placeholder = currentValue;
                input.maxLength = 30;
                input.minLength = 1;
                input.value = currentValue;
                if(isNonEdit)
                {
                    input.disabled = true;
                }

                td.append(input)
                tr.append(td)
            }

            this.#tableID.append(tr)
            this.#bodyArray.push(tr);
            console.log("успех addBody")
            return true;
        }
    }
    isTypeValid(curType)
    {
        for(let val in Object.values(TABLE_TYPE))
        {
            if(val == curType)  // не изменять! тип не нужно сопоставлять в проверке
            {
                return true;
            }
        }
        return false;
    }
}

export {
    CTable
}