
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


let cmessBox = new CMessBox("error_box");
let casr = undefined;

let cresultBox = undefined;
let successAsrID = 0;
let antiFlood = 0;
let responseProcess = false;

let inputFieldASR = undefined;

function getASRData(inputData)
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
                            console.log(`${key}: ${value}`)
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





                    // const entries = Object.entries(data.asr_data);
                    // entries.forEach(([key, value]) => {
                    //     if(value !== null)
                    //     {
                    //         let element = document.getElementById(key);
                    //         if(element !== null)
                    //         {
                    //             element.innerText = value;
                    //             resultCount ++;
                    //         }
                    //     }
                    //     console.log(`${key}: ${value}`)
                    // })
                    // if(resultCount)
                    // {
                    //     cresultBox.showAnimBox(false);
                    //     cresultBox.showResultTable(true)
                    // }








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



$(document).ready(function() {
    let blockID = {};

    blockID.resultBox = document.getElementById("all_result_block");
    blockID.loadAnimBlock = document.getElementById("load_anim_block");
    blockID.asrResultBlock = document.getElementById("asr_result_block");

    if(!blockID.resultBox || !blockID.loadAnimBlock || !blockID.asrResultBlock)
    {
        alert("Ошибка на странице!")
        return false;
    }
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

}); // document ready