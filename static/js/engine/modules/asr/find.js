
// Морда для обработчика ASR
// Редактирование, просмотр и удаление
// Рязанов НВ 12.03.2024
// ООО КВАНТ
// ЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫ


// ----------------------------------------------------------------- Imports

import {CMessBox} from "/static/js/engine/CMessBox.js"
import {CFieldsCheck} from "/static/js/engine/CFieldsCheck.js";


import {
    getTimestampInSeconds,
} from "/static/js/engine/common.js";

import {
    ResultWindow

} from "/static/js/engine/modules/asr/CResultWindow.js";

import {
    CASRFields,
    CASRArray,
} from "/static/js/engine/modules/asr/CASR.js";

import {
    CEditParameters
} from "/static/js/engine/CEditParameters.js";


import {
    CTable,
} from "/static/js/engine/modules/asr/CTable.js";

import {
    cButtons,
} from "/static/js/engine/modules/asr/cButtons.js";

import {
    BUTTOM_TYPE,
    TABLE_TYPE,
} from "/static/js/engine/modules/asr/common.js";

import {CForms} from "/static/js/engine/CForms.js";

import {
    CCaptha,
} from "/static/js/engine/CCaptha.js";

// ----------------------------------------------------------------- Imports END

// ----------------------------------------------------------------- VARS

let cmessBox = new CMessBox("error_box");

let casrField = new CASRFields(); // класс asr CASRFields
let casrArray = new CASRArray();
let cTable = new CTable(); // класс управления таблицей
let cButton = new cButtons(); // класс управления кнопками

let cresultBox = undefined; // класс результ бокса
let successAsrID = null;  // название полученного ASR если успех
let antiFlood = 0; // антифлуд
let responseProcess = false;  // отправка ajax

let inputFieldASR = undefined;  // инпат с ввода аср
let btnEdit = undefined; // кнопка редактировать в результ боксе
let btnDel = undefined; // кнопка удалить
let btnSave = undefined;  // кнопка сохранить
let btnCancel = undefined;  // кнопка отмена
let tableHTMLNameID = "result_table";
let tableHTMLPlaceID = "table_asr_id";
let assocArraySuccess = false;

// ----------------------------------------------------------------- VARS END
// ----------------------------------------------------------------- FUNC





function onUserPressedOnDeleteBtn(btnType)  // если нажата кнопка удаления
{
    if(!assocArraySuccess)return
    switch(btnType)
    {
        case BUTTOM_TYPE.TYPE_EDIT:
        {
            if(cTable.getCurrentType() === TABLE_TYPE.TYPE_STANDART)
            {
                cTable.destroyTable();
                showTable(TABLE_TYPE.TYPE_EDITTING);
                return true;
            }
            else
            {
                cmessBox.sendErrorMessage("Ошибка определения типа таблицы!");
            }
            break;
        }
        case BUTTOM_TYPE.TYPE_SAVE:
        {
            if(responseProcess === true)
            {
                cmessBox.sendErrorMessage("Ответ от сервера ещё не пришёл!");
                return false;  //(false - не отправляем форму на сервер)
            }


            if(antiFlood > getTimestampInSeconds())
            {
                cmessBox.sendErrorMessage("Не флудите!");
                return false;  //(false - не отправляем форму на сервер)
            }
            antiFlood = getTimestampInSeconds() + 1;

            // сохранение редактирования

            let valuesTable = document.querySelectorAll(`table[id='${tableHTMLNameID}']`);
            let tableArray = valuesTable.item(0);

            let valuesOld = document.querySelectorAll(`span[class='value_current']`);
            let valuesNew = document.querySelectorAll(`input[class='value_new']`);

            let cOldValues = new CEditParameters();
            let cNewValues = new CEditParameters();

            valuesOld.values().forEach( (element) => {
                //console.log(element.id.split("|"))
                cOldValues.addData(String(element.id.split("|")[1]), element.innerText);
                //console.log(element.innerText)
            })

            valuesNew.values().forEach( (element) => {

                cNewValues.addData(String(element.id.split("|")[1]), element.value)
                //console.log(element.value)
            })
            let resultArray = cNewValues.isTotalAllSame(cOldValues); // сравнение коллекций
            /*
            * resultArray:
            * null = полностью одинаковые коллекции
            * false = расхождение ключей
            * если есть отличия - вернёт массив формата [ключ html, старое значение, новое значение]
            *
            * */

            if(resultArray === false)
            {
                cmessBox.sendErrorMessage("Ошибка определения значений таблицы! Перезагрузите страницу...");
            }
            else if(resultArray === null)
            {
                cmessBox.sendErrorMessage("Вы не вносили никаких изменений.");
            }
            else
            {

                let name = undefined;
                for(let arr of resultArray)
                {
                    let labelHTMLName = arr[cNewValues.ARRAY_INDEX.HTML_LABEL];
                    let index = casrArray.getArrIDFromHTMLFieldType(labelHTMLName)
                    if(index !== null)
                    {
                        // проверка на пустое поле
                        let currentValue = cNewValues.getValue(labelHTMLName);
                        name = casrArray.getValueName(index);
                        let isNonZero = casrArray.isTypeNonZeroValueEditting(labelHTMLName);
                        if(isNonZero)
                        {
                            if(!currentValue)
                            {
                                //console.log(`name ${name}`)
                                if(name)
                                {
                                    cmessBox.sendErrorMessage(`Оставлять поле '${name}' пустым запрещено!`);
                                }
                                return false;
                            }
                        }
                        // проверка на запрет редактирования
                        let JSTypeSTR = casrArray.getJSTypeFromHTMLType(labelHTMLName);
                        let JSTypeValue = casrArray.TYPE_ASR_FIELD[JSTypeSTR];
                        if(casrArray.isTypeNonEditting(labelHTMLName, JSTypeSTR))
                        {
                            if(currentValue !== cOldValues.getValue(labelHTMLName))
                            {
                                cmessBox.sendErrorMessage(`Редактирование поля '${name}' запрещено!`);
                                return false;
                            }
                        }

                        // проверка на на валидность ввода данных

                        if(JSTypeValue !== undefined)
                        {
                            // для даты
                            if(JSTypeValue === casrArray.TYPE_ASR_FIELD.ASR_SCAN_DATE)
                            {
                                const regex = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/;  //2024-03-06 10:36:56
                                if (!regex.test(currentValue))
                                {
                                    // дата может быть пустым полем, поэтому проверка
                                    if(currentValue)
                                    {
                                        if(name)
                                        {
                                            cmessBox.sendErrorMessage(`Ошибка в поле '${name}'! Некорректная дата!`);
                                        }
                                        return false;
                                    }
                                }
                            }
                            else if(!casrArray.isCorrectDate(JSTypeValue, currentValue))
                            {
                                if(name)
                                {
                                    cmessBox.sendErrorMessage(`Ошибка в поле '${name}'!`);
                                }
                                return false;
                            }
                        }
                    }
                }


                // Проверка даты

                let asrSqlID = casrField.getArrIDFromFieldType(casrArray.TYPE_ASR_FIELD.ASR_SQL_ID);
                let asrSqlValue = null;
                if(asrSqlID !== null)
                {
                    asrSqlValue = casrField.getValue(asrSqlID);
                }
                if(asrSqlValue !== null)
                {
                    let completed_json = JSON.stringify({
                        casrname: successAsrID,
                        editarray: resultArray,
                        cassyid: asrSqlValue,
                    }); //$.parseJSON(json_text);

                    $.ajax({
                        data : completed_json,
                        dataType: 'json',
                        type : 'POST',
                        url : './asr_replace_ajax',
                        contentType: "application/json",
                        success: function(data) {
                            responseProcess = false

                            if(data.result === true)
                            {
                                resultArray.forEach( (element, index) => {
                                    let cfieldArrayID = casrField.getArrIDFromFieldHTMLName(
                                        element[cOldValues.ARRAY_INDEX.HTML_LABEL]);
                                    if(cfieldArrayID !== null)
                                    {
                                        casrField.setValue(cfieldArrayID,
                                            element[cOldValues.ARRAY_INDEX.NEW_VALUE]);
                                    }
                                    else
                                    {
                                        cmessBox.sendErrorMessage("Ошибка обработки филдов из массива изменений!");
                                        return 1;
                                    }
                                })


                                cmessBox.sendSuccessMessage(`ASR: '${successAsrID}' успешно отредактирован!`);
                                cTable.destroyTable()
                                showTable(TABLE_TYPE.TYPE_EDITTING);
                            }
                            else
                            {
                                cmessBox.sendErrorMessage(data.error_text, "", 15000);
                            }
                        },
                        error: function(error) {
                            // responseProcess = false
                            cmessBox.sendErrorMessage("Ошибка AJAX на стороне сервера!");
                        }
                    })
                }
                else cmessBox.sendErrorMessage("Ошибка определения SQL ID.");


            }
            // for (let [incKeys, incValues] of cNewValues.getElementsArray().entries())
            // {
            //     console.log(incKeys, incValues);
            // }



            break;
        }
        case BUTTOM_TYPE.TYPE_CANCEL:
        {
            if(cTable.getCurrentType() === TABLE_TYPE.TYPE_EDITTING)
            {
                cTable.destroyTable();
                showTable(TABLE_TYPE.TYPE_STANDART);
                return true;
            }
            else
            {
                cmessBox.sendErrorMessage("Ошибка определения типа таблицы!");
            }
            break;
        }
        case BUTTOM_TYPE.TYPE_DEL:
        {
            // TODO Заменить на модальное окно с Да и Нет потом
            if (confirm(`"Вы действительно хотите удалить выбранную ASR '${successAsrID}' ?
            \nОтменить действие будет невозможно!"`)) // yes
            {
                if(successAsrID && !responseProcess)
                {
                    responseProcess = true;

                    inputFieldASR.value = "";

                    let asrSqlID = casrField.getArrIDFromFieldType(casrArray.TYPE_ASR_FIELD.ASR_SQL_ID);
                    // console.log("casr.getAssocArr()")
                    // console.log(casr.getAssocArr())
                    // console.log("casr.getFieldsArr()")
                    // console.log(casr.getFieldsArr())
                    let asrSqlValue = null;
                    if(asrSqlID !== null)
                    {
                        asrSqlValue = casrField.getValue(asrSqlID);
                    }
                    if(asrSqlValue !== null)
                    {
                        let completed_json = JSON.stringify({
                            casrname: successAsrID,
                            cassyid: asrSqlValue,
                        }); //$.parseJSON(json_text);

                        $.ajax({
                            data : completed_json,
                            dataType: 'json',
                            type : 'POST',
                            url : './asr_del_ajax',
                            contentType: "application/json",
                            success: function(data) {
                                responseProcess = false

                                if(data.result === true)
                                {
                                    cresultBox.showResultBox(false);
                                    cresultBox.showAnimBox(false);
                                    cresultBox.showResultTable(false)
                                    cmessBox.sendSuccessMessage(`ASR: '${successAsrID}' успешно удалён!`);
                                    successAsrID = null;
                                    clearResultBox();
                                    cTable.destroyTable()
                                    cButton.setShowForAll(false)
                                }
                                else
                                {
                                    cmessBox.sendErrorMessage(data.error_text, "", 15000);
                                }
                            },
                            error: function(error) {
                                // responseProcess = false
                                cmessBox.sendErrorMessage("Ошибка AJAX на стороне сервера!");
                            }
                        })
                    }
                    else
                    {
                        alert("Ошибка на странице!")
                    }
                }
            }
            else // no
            {

            }
            break;
        }
    }

    return false;
}

function clearResultBox()
{
    let box = document.getElementById(tableHTMLNameID);
    if(box !== null)
    {
        let arrSpans = box.querySelectorAll("tr span[class='value']");
        if(arrSpans !== undefined)
        {
            for(let item of arrSpans)
            {
                item.innerText = "-"
            }
        }
    }
}



function getASRData(inputData) // получение инфы о аср
{
    if(!assocArraySuccess)return false;
    if(!inputData.asrName)
    {
        return false;
    }
    if(responseProcess === true)
    {
        cmessBox.sendErrorMessage("Ответ от сервера ещё не пришёл!");
        return false;  //(false - не отправляем форму на сервер)
    }
    if(successAsrID === inputData.asrName)
    {
        cmessBox.sendErrorMessage("Вы уже запросили указанный ASR!");
        return false;  //(false - не отправляем форму на сервер)
    }
    if(antiFlood > getTimestampInSeconds())
    {
        cmessBox.sendErrorMessage("Не флудите!");
        return false;  //(false - не отправляем форму на сервер)
    }
    let cfield = new CFieldsCheck();
    let resultObj = cfield.set_check_asr(inputData.asrName);
    let ccfPass = new CForms(inputFieldASR)

    if(!resultObj) return false
    if(resultObj.result === false)
    {
        resultObj = cfield.set_check_mac(inputData.asrName);
        if(resultObj.result === false)
        {
            resultObj = cfield.set_check_ms_sn(inputData.asrName);
            if(resultObj.result === false)
            {
                ccfPass.clearField()
                cmessBox.sendErrorMessage("Ошибка в названии ASR, SN МП или MAC");
                return false;
            }
        }
    }

    // класс должен быть объявлен тут для капчи, иначе значение блока не будед перезаписываться
    let cCaptha = new CCaptha('div input[name=captcha-hash]', "captcha-text");
    let cresult = cCaptha.validate(cmessBox);
    if(!cresult)
    {
        return false;
    }

    //
    responseProcess = true;
    antiFlood = getTimestampInSeconds() + 1;

    let completed_json = JSON.stringify({
        captcha_hash: cresult.captcha_hash,
        captcha_text: cresult.captcha_text,
        casrname: inputData.asrName
    }); //$.parseJSON(json_text);

    cresultBox.showResultBox(true);
    cresultBox.showAnimBox(true);
    cresultBox.showResultTable(false)
    if(successAsrID !== null)
    {
        clearResultBox();
    }

    $.ajax({
        data : completed_json,
        dataType: 'json',
        type : 'POST',
        url : './asr_find_ajax',
        contentType: "application/json",
        success: function(data) {
            responseProcess = false

            if(data.new_captha)
            {
                // update captha
                let capthaID = document.getElementById("captha_block_id");

                if(capthaID !== null)
                {
                    capthaID.innerHTML = data.new_captha
                }
            }

            if(data.result === true)  // загрузка ASR
            {
                successAsrID = data.asr_name;

                if(data.asr_data)
                {
                    let resultCount = 0;
                    const entrie = Object.entries(data.asr_data);
                    casrField.ClearAllFields()
                    cTable.destroyTable()
                    entrie.forEach(([key, value]) => {
                        if(key)
                        {
                            //console.log(`${key}: ${value}`)
                            let fieldType = casrArray.getFieldTypeFromKeyName(key);
                            let assocArrayIndex = casrArray.getArrIDFromHTMLFieldType(key);
                            if(fieldType !== null && assocArrayIndex !== null)
                            {
                                //console.log(`${key}: ${value}`)
                                // console.log(key, fieldType, )
                              //console.log(fieldType, key, value)
                                let result = casrField.addField(fieldType, key, value);
                                if(result)
                                {
                                    //console.log("В результате" + key, fieldType, assocArrayIndex, value)
                                    resultCount ++;
                                }
                            }
                        }
                        //console.log(`${key}: ${value}`)
                    })
                    if(resultCount)
                    {
                        showTable(TABLE_TYPE.TYPE_STANDART);
                        cresultBox.showAnimBox(false);
                        cresultBox.showResultTable(true)

                        //console.log(casrField.getArray())

                    }
                    else
                    {
                        cmessBox.sendErrorMessage("Ошибка в построении таблицы результата [1]");
                    }
                }
            }
            else
            {
                cresultBox.showResultBox(false);

                cmessBox.sendErrorMessage(data.error_text);
                return false
            }
        },
        error: function(error) {
            // responseProcess = false
            cresultBox.showResultBox(false);
            cmessBox.sendErrorMessage("Ошибка AJAX на стороне сервера!");
            return false
        }
    })
    return true
}


function showTable(tableType)
{
    if(cTable.isTypeValid(tableType))
    {
        let arrJSTypes = casrArray.getArrayHTMLNames();
        if(arrJSTypes && arrJSTypes.length > 1)
        {
            if(cTable.createTable(tableHTMLPlaceID))
            {
                cTable.setType(tableType);  // строго до add header and addbody
                if(cTable.addHeader(["Название параметра", "Текущее значение"]))
                {
                    let count = 0;
                    for(let htmlName of arrJSTypes.values())
                    {
                        let fieldIndex = casrField.getArrIDFromFieldHTMLName(htmlName); // fieldIndex
                        if(fieldIndex !== null)
                        {
                            let assocArrayIndex = casrArray.getArrIDFromHTMLFieldType(htmlName);
                            if(assocArrayIndex !== null)
                            {
                                //console.log(htmlName)
                                let isNonEdit = casrArray.isTypeNonEditting(htmlName);

                                if(cTable.addBody(htmlName,`${casrArray.getValueName(assocArrayIndex)}:`,
                                    casrField.getValue(fieldIndex), isNonEdit))
                                {
                                    count++;
                                }
                            }
                        }
                    }
                    if(count)
                    {
                        cButton.switchBTNStatus(tableType)
                        return true;
                    }
                    else
                    {
                        cTable.destroyTable()
                    }
                }
            }
        }
    }
    cmessBox.sendErrorMessage("Возникла ошибка в обработке структуры таблицы!");

    return false;
}

///////////////////////

function LoadAssocArray()
{
    responseProcess = true;
    antiFlood = getTimestampInSeconds() + 1;

    $.ajax({
        data : {},
        dataType: 'json',
        type : 'POST',
        url : './asr_load_assoc_ajax',
        contentType: "application/json",
        success: function(data) {
            responseProcess = false

            if(data.result === true && data.assoc_tup)
            {
                casrArray.addData(data.assoc_tup)
                assocArraySuccess = true;
            }
            //console.log(casrArray.getArrayHTMLNames())
        },
        error: function(error) {
            // responseProcess = false
            cresultBox.showResultBox(false);
            cmessBox.sendErrorMessage("Ошибка AJAX на стороне сервера!");
            return false
        }
    })
}


// ----------------------------------------------------------------- FUNC END

$(document).ready(function() {
    let blockID = {};
    assocArraySuccess = false;
    blockID.resultBox = document.getElementById("all_result_block");
    blockID.loadAnimBlock = document.getElementById("load_anim_block");
    blockID.asrResultBlock = document.getElementById("asr_result_block");

    btnEdit = document.getElementById("btn_edit");
    btnDel = document.getElementById("btn_del");
    btnSave = document.getElementById("btn_save");
    btnCancel = document.getElementById("btn_cancel");

    if(!blockID.resultBox || !blockID.loadAnimBlock || !blockID.asrResultBlock)
    {
        alert("Ошибка на странице!")
        return false;
    }

    if(btnEdit !== null)
    {
        cButton.addBTN(btnEdit, "Редактировать", BUTTOM_TYPE.TYPE_EDIT);
        btnEdit.addEventListener("click", (event) =>
        {
            event.preventDefault(); // Отменяем стандартное поведение формы
            onUserPressedOnDeleteBtn(BUTTOM_TYPE.TYPE_EDIT);
        })
    }
    if(btnDel !== null)
    {
        cButton.addBTN(btnDel, "Удалить", BUTTOM_TYPE.TYPE_DEL);
        btnDel.addEventListener("click", (event) =>
        {
            event.preventDefault(); // Отменяем стандартное поведение формы
            onUserPressedOnDeleteBtn(BUTTOM_TYPE.TYPE_DEL);
        })
    }
    if(btnSave !== null)
    {
        cButton.addBTN(btnSave, "Сохранить", BUTTOM_TYPE.TYPE_SAVE);
        btnSave.addEventListener("click", (event) =>
        {
            event.preventDefault(); // Отменяем стандартное поведение формы
            onUserPressedOnDeleteBtn(BUTTOM_TYPE.TYPE_SAVE);
        })
    }
    if(btnCancel !== null)
    {
        cButton.addBTN(btnCancel, "Отменить редактирование", BUTTOM_TYPE.TYPE_CANCEL);
        btnCancel.addEventListener("click", (event) =>
        {
            event.preventDefault(); // Отменяем стандартное поведение формы
            onUserPressedOnDeleteBtn(BUTTOM_TYPE.TYPE_CANCEL);
        })
    }
    cButton.setShowForAll(false)


    cresultBox = new ResultWindow(blockID);

    cresultBox.showResultBox(false);

    //let csrftoken = $('meta[name=csrf-token]').attr('content')
    let csrftoken = $('.container-common input[name=csrf_token]').attr('value')

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
    clearResultBox();
    //
    inputFieldASR = document.getElementById("asr_name")
    if(inputFieldASR !== undefined)
    {
        let c_name = new CForms(inputFieldASR);

        $("#asr_find").on("submit", function (event) {
            event.preventDefault(); // Отменяем стандартное поведение формы

            // Получаем данные из полей формы
            const inputData = {
                asrName: c_name.getInputValue(),
            }
            getASRData(inputData)
        });
    }
    // загрузка ассоциативного массива
    setTimeout(LoadAssocArray, 1000)

}); // document ready
