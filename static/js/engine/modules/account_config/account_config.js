import {CForms} from "/static/js/engine/CForms.js";
import {CFieldsCheck} from "/static/js/engine/CFieldsCheck.js";
import {CMessBox} from "/static/js/engine/CMessBox.js";
import {CBSettings} from "./CCBSettings.js"

import {
    getTimestampInSeconds,
    } from "/static/js/engine/common.js";


let repassVisible = false;
let antiFlood = 0;
let responseProcess = false;

let inputFieldoldPass = null;
let inputFieldnewPass = null;
let inputFieldrePass = null;


function onUserHideRepass(element, form_repass)
{
    if(repassVisible)form_repass.style.display = "none";
    else form_repass.style.display = "";
    repassVisible = !repassVisible;
    return false;
}
let repassErrorUnit = new CMessBox("error_box_fields")

function clearAllRepassForm({ccNewPass, ccRePass, ccOldPass})
{
    if(ccNewPass)
        ccNewPass.clearField();
    if(ccRePass)
        ccRePass.clearField();
    if(ccOldPass)
        ccOldPass.clearField();
}
function onChangeRepass({oldPass, newPass, rePass})
{
    if(!oldPass || !newPass || !rePass)
    {
        return false;
    }

    if(antiFlood > getTimestampInSeconds())
    {
        repassErrorUnit.sendErrorMessage("Не флудите!");
        return false;  //(false - не отправляем форму на сервер)
    }
    if(responseProcess === true)
    {
        repassErrorUnit.sendErrorMessage("Ответ от сервера ещё не пришёл!");
        return false;  //(false - не отправляем форму на сервер)
    }

    antiFlood = getTimestampInSeconds() + 2;

    let cfield = new CFieldsCheck();
    let resultObj = {}
    // pass

    let ccOldPass = new CForms(inputFieldoldPass);
    let ccNewPass = new CForms(inputFieldnewPass);
    let ccRePass = new CForms(inputFieldrePass);

    let inputFieldsID = [
        ccOldPass, ccNewPass, ccRePass
    ];

    for(let arr of inputFieldsID)
    {
        resultObj = cfield.set_check_password(oldPass);
        if(!resultObj) return false
        if(resultObj.result === false)
        {
            arr.clearField();
            repassErrorUnit.sendErrorMessage(resultObj.errorText);
            return false;
        }
    }
    if(newPass !== rePass)
    {
        clearAllRepassForm({ccNewPass, ccRePass});
        repassErrorUnit.sendErrorMessage("Новый пароль и повтор пароля должны совпадать!");
        return false;
    }

    responseProcess = true;


    let completed_json = JSON.stringify({
        cold_pass: oldPass,
        cnew_pass: newPass,
        cre_pass: rePass,
    }); //$.parseJSON(json_text);

    $.ajax({
        data : completed_json,
        dataType: 'json',
        type : 'POST',
        url : './repass_ajax',
        contentType: "application/json",
        success: function(data) {
            responseProcess = false
            clearAllRepassForm({ccOldPass, ccNewPass, ccRePass});
            if(data.result === true)
            {
                repassErrorUnit.hide();
                repassErrorUnit.sendSuccessMessage("Пароль от аккаунта успешно изменён");
            }
            else
            {
                repassErrorUnit.sendErrorMessage(data.error_text);
            }
        },
        error: function(error) {
            // responseProcess = false
            repassErrorUnit.sendErrorMessage("Ошибка AJAX на стороне сервера!");
            clearAllRepassForm({ccOldPass, ccNewPass, ccRePass});
        }
    })
    return false;
}
let checkboxErrorUnit = new CMessBox("error_box_checkbox")


let ccbSettings = new CBSettings();

function onChangeCheckbox()
{

    if(antiFlood > getTimestampInSeconds())
    {
        checkboxErrorUnit.sendErrorMessage("Не флудите!");
        return false;  //(false - не отправляем форму на сервер)
    }

    if(responseProcess === true)
    {
        checkboxErrorUnit.sendErrorMessage("Ответ от сервера ещё не пришёл!");
        return false;  //(false - не отправляем форму на сервер)
    }

    // checkbox Автоматический выход при неактивности

    let cbTimeOutID = ccbSettings.getCBFieldID(ccbSettings.cb_FieldType.CB_TIMEOUT);
    let cbTimeoutCheckedStatus = cbTimeOutID.checked;
    antiFlood = getTimestampInSeconds() + 2;
    if(cbTimeoutCheckedStatus === ccbSettings.getCBValue(ccbSettings.cb_FieldType.CB_TIMEOUT))
    {
        checkboxErrorUnit.sendErrorMessage("Вы ничего не изменяли");
        return false;
    }
    checkboxErrorUnit.hide();

    ccbSettings.updateCBValue(ccbSettings.cb_FieldType.CB_TIMEOUT, cbTimeoutCheckedStatus);


    responseProcess = true;

    let completed_json = JSON.stringify({
        cb_timeout: cbTimeoutCheckedStatus,
    }); //$.parseJSON(json_text);

    $.ajax({
        data : completed_json,
        dataType: 'json',
        type : 'POST',
        url : './cb_settings_ajax',
        contentType: "application/json",
        success: function(data) {
            responseProcess = false;
            if(data.result === true)
            {
                checkboxErrorUnit.hide();
                checkboxErrorUnit.sendSuccessMessage("Настройки успешно сохранены");
            }
            else
            {
                checkboxErrorUnit.sendErrorMessage(data.error_text);
            }
        },
        error: function(error) {
            // responseProcess = false
            checkboxErrorUnit.sendErrorMessage("Ошибка AJAX на стороне сервера!");
        }
    })

    return false;
}



$(document).ready(function() {

    //let csrftoken = $('meta[name=csrf-token]').attr('content')
    let csrftoken = $('body input[name=csrf_token]').attr('value')

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })

    let btn_repass = document.getElementById("btn_change_pass");
    if(btn_repass !== null)
    {
        let form_repass = document.querySelector("#field_setting_container .setting_repass .border-common");
        if(form_repass !== null)
        {
            form_repass.style.display = "none";
            btn_repass.addEventListener("click", function (element) {
                onUserHideRepass(element, form_repass);
            })
        }
    }

    //
    repassVisible = false;
    // repass event
    $("#settings_change_pass").on("submit", function (event) {
        event.preventDefault(); // Отменяем стандартное поведение формы

        inputFieldoldPass = document.getElementById("old_pass")
        inputFieldnewPass = document.getElementById("new_pass")
        inputFieldrePass = document.getElementById("renew_pass")
        if(inputFieldoldPass && inputFieldnewPass && inputFieldrePass)
        {
            let oldPass = new CForms(inputFieldoldPass)
            let newPass = new CForms(inputFieldnewPass)
            let rePass = new CForms(inputFieldrePass)

            oldPass = oldPass.getInputValue();
            newPass = newPass.getInputValue();
            rePass = rePass.getInputValue();

            let obj = {
                oldPass, newPass, rePass
            }
            onChangeRepass(obj);
        }
    });

    // checkbox event
    $("#settings_form_checkbox").on("submit", function (event) {
        event.preventDefault(); // Отменяем стандартное поведение формы

        onChangeCheckbox();
    });

    let element = document.getElementById("cb_timeout");
    if(element !== null)
    {
        ccbSettings.updateCBFieldID(ccbSettings.cb_FieldType.CB_TIMEOUT, element);
        ccbSettings.updateCBValue(ccbSettings.cb_FieldType.CB_TIMEOUT, element.checked);
    }

}); // document ready