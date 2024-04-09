

class CEditParameters
{
    ARRAY_INDEX = {
        HTML_LABEL: 0,
        OLD_VALUE: 1,
        NEW_VALUE: 2
    }

    #arrayData = new Map();
    constructor() {
    }

    addData(htmlType, cValue)
    {
        if(this.#isHTMLValid(htmlType))
        {
            this.#arrayData.set(htmlType, cValue);
            return true;
        }
        return false;
    }
    getValue(htmlType)
    {
        if(this.#isHTMLValid(htmlType))
        {
            return this.#arrayData.get(htmlType); // undefined if key is not find
        }
        return undefined;
    }
    deleteValue(htmlType)
    {
        if(this.#isHTMLValid(htmlType))
        {
            if(this.#arrayData.has(htmlType))
            {
                this.#arrayData.delete(htmlType);
                return true;
            }
        }
        return false;
    }
    #isHTMLValid(htmlType)
    {
        return htmlType && typeof htmlType == 'string';
    }
    getElementsArray()
    {
        return this.#arrayData;
    }
    truncateArray()
    {
        this.#arrayData.clear();
    }
    isTotalAllSame(cParametersIncomingUnit)  // сравнить значения в объекте cParametersUnit с текущим юнитом
    {
        /*
        Сравнение значений двух объектов

        Сравниение двух множеств:
        1) Преобразуем множества пришедшего массива и текущего массива объекты в ключи и смотрим совпадение всех
        ключей в двух объектах
        2) Смотрим значения по тому же принципу и сравниваем.
        3) При расхождение ключей возвращаем false
        4) При расхождениях в значениях возвращаем массив html меток и  старое значени и новое
        5) Если коллекции полностью одинаковы, то вернём null
        */


        if(cParametersIncomingUnit instanceof CEditParameters)
        {
            let incomingKeys = Array.from(cParametersIncomingUnit.getElementsArray().keys());
            if(Array.isArray(incomingKeys))
            {
                if(incomingKeys.length > 0)
                {
                    let currentKeys = Array.from(this.#arrayData.keys());
                    if(Array.isArray(currentKeys))
                    {
                        if(currentKeys.length > 0)
                        {
                            // сравнение ключей
                            if(currentKeys.length !== incomingKeys.length)
                            {
                                return false;
                            }
                            for (let incKeys of incomingKeys)
                            {
                                let result = false;
                                for (let curKeys of currentKeys)
                                {
                                    if(incKeys !== curKeys)continue;
                                    result = true;
                                    break;
                                }
                                if(result === false) // ключи не совпали
                                {
                                    return false;
                                }
                            }
                            // сравнение значений
                            let returningArr = Array();

                            let incomingValues = cParametersIncomingUnit.getElementsArray().entries();
                            let currentValues = this.getElementsArray().entries();

                            let itsArraysNotSame = false; // если массивы не одинаковы, а именно значения
                            for (let [incKeys, incValues] of incomingValues)
                            {
                                for (let [curKeys, curValues] of currentValues)
                                {
                                    if(incKeys !== curKeys)continue;

                                    if(incValues !== curValues)
                                    {
                                        returningArr.push([incKeys, incValues, curValues])
                                        itsArraysNotSame = true;
                                    }
                                    break;
                                }
                            }
                            if(returningArr.length > 0)
                            {
                                return returningArr;
                            }
                            else
                            {
                                return null;
                            }
                        }
                    }
                }
            }
        }
        return false;
    }
}

export {
    CEditParameters
}