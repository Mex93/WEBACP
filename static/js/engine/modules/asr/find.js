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
    CASRFields

} from "/static/js/engine/modules/asr/CASR.js";

import {CForms} from "/static/js/engine/CForms.js";

import {
    CCaptha,
} from "/static/js/engine/CCaptha.js";

// ----------------------------------------------------------------- Imports END

// ----------------------------------------------------------------- VARS

let cmessBox = new CMessBox("error_box");

let casr = undefined; // класс asr CASRFields

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
                    casr = new CASRFields(data.assoc_tup);
                    const entries = Object.entries(data.asr_data);

                    entries.forEach(([key, value]) => {
                        if(value !== null)
                        {
                            //console.log(`${key}: ${value}`)
                            let elementID = document.getElementById(`${key}`);
                            if(elementID !== null)
                            {
                                let fieldType = casr.getFieldTypeFromKeyName(key);
                                if(fieldType != null)
                                {
                                    //console.log(`${key}: ${value}`)
                                    let result = casr.addField(fieldType, key, value, elementID);
                                    if(result)
                                    {
                                        elementID.innerText = value;
                                        resultCount ++;
                                    }
                                }

                            }
                        }
                        //console.log(`${key}: ${value}`)
                    })
                    if(resultCount)
                    {
                        cresultBox.showAnimBox(false);
                        cresultBox.showResultTable(true)
                    }
                    else
                    {
                        cmessBox.sendErrorMessage("Ошибка в построении таблицы результата");
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
