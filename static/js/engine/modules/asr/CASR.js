

class CASRArray
{
    // TODO Класс для обработки массива прихордящего из бэка, который содержит множество данных
    ASSOC_POD_TYPE = {
        LABEL_HTML_NAME: 0,
        BACK_SQL_NAME: 1,
        BACK_ENUM_TYPE: 2,
        JS_TYPES_NAME: 3,
        VALUE_NAME: 4
    }
    #assocArray = undefined
    TYPE_ASR_FIELD = {}


    constructor()
    {

    }
    addData(objData)
    {
        if(objData)
        {
            objData.forEach((element, index) =>
            {
                this.TYPE_ASR_FIELD[element[this.ASSOC_POD_TYPE.JS_TYPES_NAME]] = element[this.ASSOC_POD_TYPE.BACK_ENUM_TYPE];

                // console.log(`Инициализация ${element[this.ASSOC_POD_TYPE.LABEL_NAME]}\n
                // Тип BACK_TYPE ${element[this.ASSOC_POD_TYPE.BACK_TYPE]}
                // Тип в объекте JS_TYPES_NAME ${element[this.ASSOC_POD_TYPE.JS_TYPES_NAME]}`)
            })
            this.#assocArray = objData;
        }
    }
    isArrayIndexValid(arrIndex)
    {
        return (String(this.#assocArray[arrIndex][this.ASSOC_POD_TYPE.VALUE_NAME]).length > 0)

    }

    getArrIDFromJSFieldType(fieldType)
    {
        for(const [index, value] of this.#assocArray.entries())
        {
            if(value)
            {
                if(value[this.ASSOC_POD_TYPE.JS_TYPES_NAME] !== fieldType)continue;
                return index;
            }
        }
        return null;
    }
    getArrIDFromHTMLFieldType(fieldType)
    {
        for(const [index, value] of this.#assocArray.entries())
        {
            if(value)
            {
                if(value[this.ASSOC_POD_TYPE.LABEL_HTML_NAME] !== fieldType)continue;
                return index;
            }
        }
        return null;
    }

    getValueName(arrIndex)
    {
        if(this.isArrayIndexValid(arrIndex))
        {
            return this.#assocArray[arrIndex][this.ASSOC_POD_TYPE.VALUE_NAME]
        }
        return false;
    }

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
    getArrayHTMLNames() // получит все типы пришедшие с бека, нужно для обработки дальше CASRFields
    {
        let arr = [];
        for(let i = 0; i < this.#assocArray.length; i++)
        {
            if(!this.isArrayIndexValid(i))continue;
            arr.push(this.#assocArray[i][this.ASSOC_POD_TYPE.LABEL_HTML_NAME])
        }
        if(arr.length)
        {
            return arr;
        }
    }
}



class CASRFields
{
    /*
     TODO Класс обработки ASR: создание филдов с данными конфига конкретного ASR на основе данных пришедших с бэка
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

    FIELD_POD_TYPE = {
        FIELD_TYPE: 0,
        KEY_NAME: 1,
        VALUE: 2,
    }

    constructor()
    {

    }

    #initFieldTypeFromLabelName(lbName)
    {
        // switch(lbName)
        // {
        //     case ""
        // }
    }

    addField(fieldType, keyName, currentValue)
    {
        if(fieldType && keyName && currentValue)
        {
            if(this.getArrIDFromFieldType(fieldType) === null)
            {
                this.#fieldsArr.push([fieldType, keyName, currentValue])
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
    getArrIDFromFieldHTMLName(fieldType)
    {
        for(const [index, value] of this.#fieldsArr.entries())
        {
            if(value)
            {
                if(value[this.FIELD_POD_TYPE.KEY_NAME] !== fieldType)continue;
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
    ClearAllFields()
    {
        let count = 0;
        this.#fieldsArr.forEach((element, index) =>
        {
            if(this.isArrayIndexValid(index))
            {
                this.#fieldsArr[index][this.FIELD_POD_TYPE.FIELD_TYPE] = null;
                count++;
            }
        })
        if(count)
            this.#reUpdateArr();

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
    isArrayIndexValid(arrIndex)
    {
        return arrIndex >= 0 && arrIndex <= this.#fieldsArr.length;
    }

}

export {
    CASRFields, CASRArray
}