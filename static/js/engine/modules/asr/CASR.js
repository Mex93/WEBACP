
let index = 0;

class CASRFields
{
    #fieldsArr = [];


    TYPE_ASR_FIELD = {
        ASR_SQL_ID: index++,
        ASR_NAME: index++,
        ASR_TV_FK: index++,
        ASR_LINE_ID: index++,
        ASR_WF: index++,
        ASR_BT: index++,
        ASR_MAC: index++,
        ASR_PANEL: index++,
        ASR_OC: index++,
        ASR_MB: index++,
        ASR_PB: index++,
        ASR_TCON: index++,
        ASR_SCAN_DATE: index++,
        ASR_OPS: index++,
        ASR_MODEL_NAME: index++,
        ASR_MODEL_TYPE_NAME: index++,
        ASR_VENDOR_CODE: index++,
    }
    index = 0;

    FIELD_POD_TYPE = {
        FIELD_TYPE: index++,
        KEY_NAME: index++,
        VALUE: index++,
        HTML_OBJECT_ID: index++,
    }
    #assocArray = undefined

    constructor(objData)
    {
        if(objData)
        {
            this.#assocArray = objData;
        }
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
            this.#fieldsArr[index][this.FIELD_POD_TYPE.FIELD_TYPE] = null;
            this.#reUpdateArr();
        }
        return false;
    }

    // get set values
    // values
    getValue(arrIndex)
    {
        if(this.isArrayIndexValid(arrIndex))
        {
            return this.#fieldsArr[index][this.FIELD_POD_TYPE.VALUE];
        }
        return null;
    }

    setValue(arrIndex, value)
    {
        if(this.isArrayIndexValid(arrIndex))
        {
           this.#fieldsArr[index][this.FIELD_POD_TYPE.VALUE] = value;
           return true;
        }
        return false;
    }
    // HTML
    setHTML(arrIndex, value)
    {
        if(this.isArrayIndexValid(arrIndex))
        {
            this.#fieldsArr[index][this.FIELD_POD_TYPE.HTML_OBJECT_ID] = value;
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
            this.#fieldsArr[index][this.FIELD_POD_TYPE.KEY_NAME] = value;
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
                        return miniArr[1];
                }
            }
        }
        return null;
    }
    isArrayIndexValid(arrIndex)
    {
        return arrIndex >= 0 && arrIndex <= this.#fieldsArr.length;
    }
}

export {
    CASRFields
}