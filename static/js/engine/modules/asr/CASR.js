

class CASRFields
{
    /*
     TODO Класс обработки ASR: полей, динамический тип из бэка для использования
    Доступные типы для филдов:
    ASR_NAME: 0,
    ASR_SQL_ID: 0,
    ASR_TV_FK: 0,
    ASR_LINE_ID: 0,
    ASR_WF: 0,
    ASR_BT: 0,
    ASR_MAC: 0,
    ASR_PANEL: 0,
    ASR_OC: 0,
    ASR_MB: 0,
    ASR_PB: 0,
    ASR_TCON: 0,
    ASR_SCAN_DATE: 0,
    ASR_OPS: 0,
    ASR_MODEL_NAME: 0,
    ASR_MODEL_TYPE_NAME: 0,
    ASR_VENDOR_CODE: 0
    */

    #fieldsArr = [];

    TYPE_ASR_FIELD = {}

    FIELD_POD_TYPE = {
        FIELD_TYPE: 0,
        KEY_NAME: 1,
        VALUE: 2,
        HTML_OBJECT_ID: 3,
    }
    ASSOC_POD_TYPE = {
        LABEL_NAME: 0,
        BACK_NAME: 1,
        BACK_TYPE: 2,
        JS_TYPES_NAME: 3,
    }
    #assocArray = undefined

    constructor(objData)
    {
        if(objData)
        {
            objData.forEach((element, index) =>
            {
                this.TYPE_ASR_FIELD[element[this.ASSOC_POD_TYPE.JS_TYPES_NAME]] = element[this.ASSOC_POD_TYPE.BACK_TYPE];

                // console.log(`Инициализация ${element[this.ASSOC_POD_TYPE.LABEL_NAME]}\n
                // Тип BACK_TYPE ${element[this.ASSOC_POD_TYPE.BACK_TYPE]}
                // Тип в объекте JS_TYPES_NAME ${element[this.ASSOC_POD_TYPE.JS_TYPES_NAME]}`)
            })
            this.#assocArray = objData;
        }
    }

    #initFieldTypeFromLabelName(lbName)
    {
        // switch(lbName)
        // {
        //     case ""
        // }
    }

    addField(fieldType, keyName, currentValue, htmlID)
    {
        if(fieldType && keyName && currentValue && htmlID)
        {
            if(this.getArrIDFromFieldType(fieldType) === null)
            {
                this.#fieldsArr.push([fieldType, keyName, currentValue, htmlID])
                return this.#fieldsArr.length;
            }
        }
        return null;
    }
    getArrIDFromFieldType(fieldType)
    {
        for(const [index, value] of this.#fieldsArr.entries())
        {
            if(value)
            {
                if(value[this.FIELD_POD_TYPE.FIELD_TYPE] !== fieldType)continue;
                return index;
            }
        }
        return null;
    }
    #reUpdateArr() {

        const newArr = this.#fieldsArr.filter((value) => {
            if(value[this.FIELD_POD_TYPE.FIELD_TYPE] !== null)
            {
                return value;
            }
        });
        if(newArr)
        {
            this.#fieldsArr = newArr;
            return true;
        }
        return false;
    }
    deleteField(arrIndex)
    {
        if(this.isArrayIndexValid(arrIndex))
        {
            this.#fieldsArr[arrIndex][this.FIELD_POD_TYPE.FIELD_TYPE] = null;
            this.#reUpdateArr();
        }
        return false;
    }
    isValidField(fieldType)
    {
        for(const arr of this.#fieldsArr)
        {
            if(arr)
            {
                if(arr[this.FIELD_POD_TYPE.FIELD_TYPE] === fieldType)
                {
                    return true;
                }
            }
        }
        return false;
    }

    // get set values
    // values
    getValue(arrIndex)
    {
        if(this.isArrayIndexValid(arrIndex))
        {
            return this.#fieldsArr[arrIndex][this.FIELD_POD_TYPE.VALUE];
        }
        return null;
    }

    setValue(arrIndex, value)
    {
        if(this.isArrayIndexValid(arrIndex))
        {
           this.#fieldsArr[arrIndex][this.FIELD_POD_TYPE.VALUE] = value;
           return true;
        }
        return false;
    }
    // HTML
    setHTML(arrIndex, value)
    {
        if(this.isArrayIndexValid(arrIndex))
        {
            this.#fieldsArr[arrIndex][this.FIELD_POD_TYPE.HTML_OBJECT_ID] = value;
            return true;
        }
        return false;
    }
    getHTMLID(arrIndex)
    {
        if(this.isArrayIndexValid(arrIndex))
        {
            return this.#fieldsArr[arrIndex][this.FIELD_POD_TYPE.HTML_OBJECT_ID];
        }
        return null;
    }
    //keys

    getKey(arrIndex)
    {
        if(this.isArrayIndexValid(arrIndex))
        {
            return this.#fieldsArr[arrIndex][this.FIELD_POD_TYPE.KEY_NAME];
        }
        return null;
    }

    setKey(arrIndex, value)
    {
        if(this.isArrayIndexValid(arrIndex))
        {
            this.#fieldsArr[arrIndex][this.FIELD_POD_TYPE.KEY_NAME] = value;
            return true;
        }
        return false;
    }

    //
    getFieldTypeFromKeyName(keyName)
    {
        if(keyName)
        {
            for(const miniArr of this.#assocArray)
            {
                if(miniArr)
                {
                    if(miniArr[0].indexOf(keyName) !== -1)
                        return miniArr[2];
                }
            }
        }
        return null;
    }
    isArrayIndexValid(arrIndex)
    {
        return arrIndex >= 0 && arrIndex <= this.#fieldsArr.length;
    }
    getFieldsArr()
    {
        return this.#fieldsArr
    }
    getAssocArr()
    {
        return this.#assocArray
    }
}

export {
    CASRFields
}