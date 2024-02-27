import {CForms} from "/static/js/engine/CForms.js";
import {CFieldsCheck} from "/static/js/engine/CFieldsCheck.js";
import {CMessBox} from "/static/js/engine/CMessBox.js"
import {CWindowBox} from "/static/js/engine/CWindowBox.js";
import {CBSettings} from "/static/js/engine/modules/account/settings/CCBSettings.js"

import {
    getTimestampInSeconds,
} from "/static/js/engine/common.js";




// import {
//     LineParams,
//     PARAMS_ID,
//     INCOMMING_ARR_TYPE,
//     MAX_VRN_LINES,
//     MAX_ALL_LINES,
//     CUpdatedLines,
//     CChartID,
//     CDebugger,
//     CLineShowType,
//     CHTMLBlocks
//
// } from './libs/dashboard/Classes.js';

let inputFieldPassID = null;
let inputFieldEmailID = null;
let inputFieldSaveMeID = null;
let antiFlood = 0;
let responseProcess = false;
let blockedForm = false;

let cmessBox = new CMessBox("error_box")
let cwindowBox = new CWindowBox()

function get_login({ email, password, savemy }) {

    if(!email || !password || blockedForm)
    {
        return false;
    }
    if(antiFlood > getTimestampInSeconds())
    {
        cmessBox.sendErrorMessage("Не флудите!");
        return false;  //(false - не отправляем форму на сервер)
    }
    if(responseProcess === true)
    {
        cmessBox.sendErrorMessage("Ответ от сервера ещё не пришёл!");
        return false;  //(false - не отправляем форму на сервер)
    }

    antiFlood = getTimestampInSeconds() + 2;

    let cfield = new CFieldsCheck();
    // pass
    let resultObj = cfield.set_check_password(password);
    let ccfPass = new CForms(inputFieldPassID)

    if(!resultObj) return false
    if(resultObj.result === false)
    {
        ccfPass.clearField()
        cmessBox.sendErrorMessage(resultObj.errorText);
        return false;
    }
    // email
    resultObj = cfield.set_check_email(email);
    if(!resultObj) return false
    if(resultObj.result === false)
    {
        cmessBox.sendErrorMessage(resultObj.errorText);
        return false;
    }
    responseProcess = true;


    let completed_json = JSON.stringify({
        cpassword: password,
        cnickname: email,
        csavemy: savemy
    }); //$.parseJSON(json_text);

    $.ajax({
        data : completed_json,
        dataType: 'json',
        type : 'POST',
        url : './login_ajax',
        contentType: "application/json",
        success: function(data) {
            responseProcess = false
            ccfPass.clearField()
            if(data.result === true)
            {
                blockedForm = true;
                // let formID = document.getElementById("login_form")
                // if(formID !== null)
                // {
                //     formID.style.display='none';
                // }
                cmessBox.hide();
                cwindowBox.show("Выполняется авторизация",
                    "Если ваш браузер не поддерживает автоматическую переадресацию, " +
                    "то просто обновите страницу", "rgb(4, 170, 109)", 0);
                setTimeout(function () {
                    window.location.href = './';
                }, 1500);
            }
            else
            {
                cmessBox.sendErrorMessage(data.error_text);
                return false
            }
        },
        error: function(error) {
            // responseProcess = false
            cmessBox.sendErrorMessage("Ошибка AJAX на стороне сервера!");
            return false
        }
    })
    return true
}



$(document).ready(function() {

    //let csrftoken = $('meta[name=csrf-token]').attr('content')
    let csrftoken = $('#login_form input[name=csrf_token]').attr('value')
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })

    inputFieldPassID = document.getElementById("user_pass")
    inputFieldEmailID = document.getElementById("user_name")
    inputFieldSaveMeID = document.getElementById("user_save_me")

    let c_name = new CForms(inputFieldEmailID)
    let c_pass = new CForms(inputFieldPassID)
    let c_savemy = new CForms(inputFieldSaveMeID)

    $("#login_form").on("submit", function (event) {
        event.preventDefault(); // Отменяем стандартное поведение формы

        // Получаем данные из полей формы
        const data = {
            email: c_name.getInputValue(),
            password: c_pass.getInputValue(),
            savemy: inputFieldSaveMeID.checked,
        }
        get_login(data)
    });

}); // document ready