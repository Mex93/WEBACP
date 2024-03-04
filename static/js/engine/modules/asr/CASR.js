
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

    // constructor(objData)
    // {
    //     if(objData)
    //     {
    //
    //     }
    // }
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
            if(keyName.indexOf("asr_id") !== -1) return this.TYPE_ASR_FIELD.ASR_SQL_ID;
            else if(keyName.indexOf("asr_name") !== -1) return this.TYPE_ASR_FIELD.ASR_NAME;
            else if(keyName.indexOf("tv_fk") !== -1) return this.TYPE_ASR_FIELD.ASR_TV_FK;
            else if(keyName.indexOf("line_id") !== -1) return this.TYPE_ASR_FIELD.ASR_LINE_ID;
            else if(keyName.indexOf("wf") !== -1) return this.TYPE_ASR_FIELD.ASR_WF;
            else if(keyName.indexOf("bt") !== -1) return this.TYPE_ASR_FIELD.ASR_BT;
            else if(keyName.indexOf("mac") !== -1) return this.TYPE_ASR_FIELD.ASR_MAC;
            else if(keyName.indexOf("panel") !== -1) return this.TYPE_ASR_FIELD.ASR_PANEL;
            else if(keyName.indexOf("oc") !== -1) return this.TYPE_ASR_FIELD.ASR_OC;
            else if(keyName.indexOf("mb") !== -1) return this.TYPE_ASR_FIELD.ASR_MB;
            else if(keyName.indexOf("pb") !== -1) return this.TYPE_ASR_FIELD.ASR_PB;
            else if(keyName.indexOf("tcon") !== -1) return this.TYPE_ASR_FIELD.ASR_TCON;
            else if(keyName.indexOf("scan_date") !== -1) return this.TYPE_ASR_FIELD.ASR_SCAN_DATE;
            else if(keyName.indexOf("ops") !== -1) return this.TYPE_ASR_FIELD.ASR_OPS;
            else if(keyName.indexOf("model_name") !== -1) return this.TYPE_ASR_FIELD.ASR_MODEL_NAME;
            else if(keyName.indexOf("model_type") !== -1) return this.TYPE_ASR_FIELD.ASR_MODEL_TYPE_NAME;
            else if(keyName.indexOf("code") !== -1) return this.TYPE_ASR_FIELD.ASR_VENDOR_CODE;
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