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
    CASRArray

} from "/static/js/engine/modules/asr/CASR.js";

import {CForms} from "/static/js/engine/CForms.js";

import {
    CCaptha,
} from "/static/js/engine/CCaptha.js";

// ----------------------------------------------------------------- Imports END

// ----------------------------------------------------------------- VARS

let cmessBox = new CMessBox("error_box");

let casr = new CASRFields(); // класс asr CASRFields
let casrArray = new CASRArray();

let cresultBox = undefined; // класс результ бокса
let successAsrID = null;  // название полученного ASR если успех
let antiFlood = 0; // антифлуд
let responseProcess = false;  // отправка ajax

let inputFieldASR = undefined;  // инпат с ввода аср
let btnEdit = undefined; // кнопка редактировать в результ боксе
let btnDel = undefined; // результ бокс удалить
let btnSave = undefined;  // результ бокс сохранить

let usedSourceType = false;  // если включено редактирование таблицы
// ----------------------------------------------------------------- VARS END
// ----------------------------------------------------------------- FUNC

function onUserPressedOnDeleteBtn()  // если нажата кнопка удаления
{
    // TODO Заменить на модальное окно с Да и Нет потом
    if (confirm(`"Вы действительно хотите удалить выбранную ASR '${successAsrID}' ?\\n"` +
        "Отменить действие будет невозможно!")) // yes
    {
        if(successAsrID && !responseProcess)
        {
            responseProcess = true;

            inputFieldASR.value = "";

            let asrSqlID = casr.getArrIDFromFieldType(casr.TYPE_ASR_FIELD.ASR_SQL_ID);
            // console.log("casr.getAssocArr()")
            // console.log(casr.getAssocArr())
            // console.log("casr.getFieldsArr()")
            // console.log(casr.getFieldsArr())
            if(asrSqlID !== null)
            {
                asrSqlID = casr.getValue(asrSqlID);
            }
            if(asrSqlID && asrSqlID)
            {
                let completed_json = JSON.stringify({
                    casrname: successAsrID,
                    cassyid: asrSqlID,
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
                            btnSave.style.display = "none";
                            successAsrID = null;
                            clearResultBox();
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
    return false;
}

function clearResultBox()
{
    let box = document.getElementById("result_table");
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


class CTable
{
    TABLE_TYPE = {
        TYPE_NONE: 0,
        TYPE_STANDART: 1,
        TYPE_EDITTING: 3
    }
    #tableID = undefined;
    #tableType = undefined;
    #headerID = undefined;
    #bodyArray = undefined;
    #tablePlaceID = undefined;
    #bodyCounts = 0;
    constructor(placeIDName) {
        let tablePlace = document.getElementById(placeIDName);
        if(tablePlace)
        {
            this.#tablePlaceID = tablePlace;

            this.#tableType = this.TABLE_TYPE.TYPE_NONE
            this.#headerID = undefined;
            this.#bodyArray = Array();


            let table = document.createElement("table");
            table.id = "result_table"
            table.className = "custom-table"
            this.#tableID = table;
            tablePlace.innerHTML = table;
        }
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
    clearHeader()
    {
        if(this.#headerID !== null)
        {
            this.#headerID.remove();
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
            if(this.#tableType === this.TABLE_TYPE.TYPE_EDITTING)
            {
                let th = document.createElement("th");
                th.innerText = "Новое значение:";
                tr.append(th);
            }

            this.#tableID.append(tr);
            this.#headerID = tr;
            console.log("успех addHeader")
        }
    }
    addBody(elementName, currentValue)
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
            if(this.#tableType === this.TABLE_TYPE.TYPE_EDITTING)
            {
                td = document.createElement("td");
                span = document.createElement("span");
                span.className = "value";
                span.id = `table_element_new_value_${this.#bodyCounts}`;
                span.innerText = currentValue;
                td.append(span);
                tr.append(td)
            }

            this.#tableID.append(tr)
            this.#bodyArray.push(tr);
            console.log("успех addBody")
        }
    }
}


function getASRData(inputData) // получение инфы о аср
{
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
        ccfPass.clearField()
        cmessBox.sendErrorMessage(resultObj.errorText);
        return false;
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
    antiFlood = getTimestampInSeconds() + 2;

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

            if(data.result === true)
            {
                successAsrID = inputData.asrName;

                if(data.asr_data && data.assoc_tup)
                {
                    //console.log(data.assoc_tup)
                    let resultCount = 0;
                    casrArray = new CASRArray()
                    casrArray.addData(data.assoc_tup)
                    const entries = Object.entries(data.asr_data);


                    // let table = document.createElement("table");
                    // table.id = "result_table"
                    // table.className = "custom-table"

                    // header
                    // let tr = document.createElement("tr");
                    // //
                    // let th = document.createElement("th");
                    // th.innerText = "Название параметра:"
                    // tr.append(th)
                    // th = document.createElement("th");
                    // th.innerText = "Текущее значение"
                    // tr.append(th)
                    // table.append(tr)  // Добавление header in table
                    //
                    let table = new CTable("table_asr_id");
                    table.setType(table.TABLE_TYPE.TYPE_STANDART)
                    table.addHeader(["Название параметра", "Текущее значение"])

                    entries.forEach(([key, value]) => {
                        if(value !== null)
                        {
                            //console.log(`${key}: ${value}`)

                            let fieldType = casrArray.getFieldTypeFromKeyName(key);
                            let assocArrayIndex = casrArray.getArrIDFromHTMLFieldType(key);
                            if(fieldType != null && assocArrayIndex !== null)
                            {
                                //console.log(`${key}: ${value}`)
                                let result = casr.addField(fieldType, key, value);
                                if(result)
                                {
                                    table.addBody(`${casrArray.getValueName(assocArrayIndex)}:`, value);
                                    // // body
                                    // tr = document.createElement("tr");
                                    //
                                    // let td = document.createElement("td");
                                    // let span = document.createElement("span");
                                    // span.className = "label";
                                    // span.innerText = `${casrArray.getValueName(assocArrayIndex)}:`;
                                    // td.append(span);
                                    // tr.append(td)
                                    //
                                    // td = document.createElement("td");
                                    // span = document.createElement("span");
                                    // span.className = "value";
                                    // span.id = key;
                                    // span.innerText = value;
                                    // td.append(span);
                                    // tr.append(td)
                                    // table.append(tr)
                                    resultCount ++;
                                }
                            }
                        }
                        //console.log(`${key}: ${value}`)
                    })
                    if(resultCount)
                    {
                        let elementTableID = document.getElementById("table_asr_id")
                        if(elementTableID !== null)
                        {
                            // elementTableID.append(table);
                            cresultBox.showAnimBox(false);
                            cresultBox.showResultTable(true)
                        }
                        else cmessBox.sendErrorMessage("Ошибка в построении таблицы результата [2]");
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

// ----------------------------------------------------------------- FUNC END

$(document).ready(function() {
    let blockID = {};

    blockID.resultBox = document.getElementById("all_result_block");
    blockID.loadAnimBlock = document.getElementById("load_anim_block");
    blockID.asrResultBlock = document.getElementById("asr_result_block");

    btnEdit = document.getElementById("btn_edit");
    btnDel = document.getElementById("btn_del");
    btnSave = document.getElementById("btn_save");

    if(!blockID.resultBox || !blockID.loadAnimBlock || !blockID.asrResultBlock ||
        !btnEdit || !btnDel || !btnSave)
    {
        alert("Ошибка на странице!")
        return false;
    }
    btnSave.style.display = "none";


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


        btnDel.addEventListener("click", (event) =>
        {
            event.preventDefault(); // Отменяем стандартное поведение формы
            onUserPressedOnDeleteBtn();
        })
    }

}); // document ready
