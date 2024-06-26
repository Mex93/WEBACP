
// Морда для просмотра и редактирования собранных устройств в базе
// Удаление, просмотр и редактирование
// Рязанов НВ ..2024
// ООО КВАНТ
// ЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫ


import {CMessBox} from "/static/js/engine/CMessBox.js"
import {
    CCaptha,
} from "/static/js/engine/CCaptha.js";
import {BUTTOM_TYPE, TABLE_TYPE} from "../asr/common";

import {
    cButtons,
} from "/static/js/engine/modules/asr/cButtons.js";


let query = false;
let cmessBoxMain = new CMessBox("error_box_main");
let cmessBoxBlock = new CMessBox("error_box_block");
let cButton = new cButtons(); // класс управления кнопками
let accessDelete, accessEdit, accessCreate = null;
let isEdit = false;
let isFindSuccess = false;
let SuccessFindSN = null;


class HTMLBlocks
{
    static BLOCK_TYPE = {
        ANIM_BLOCK: 0,
        RESULT_BLOCK: 1,
    }
    htmlID = undefined;
    blockType = undefined;
    static units = [];
    showStatus = undefined;
    htmlName = undefined;

    constructor(htmlID, blockType) {

        let html = document.getElementById(htmlID);

        if(html !== null)
        {
            this.htmlName = htmlID;
            this.htmlID = html;
            this.blockType = blockType;
            this.showStatus = true;

            this.constructor.units.push(this);
        }

    }
    // static isValidNonUnit(blockType)
    // {
    //     let unitID = this.getUnitIDFromBlockType(blockType);
    //     return unitID.htmlID !== null;
    // }
    isValidWithUnit()
    {
        return this.htmlID !== undefined;
    }

    static getUnitIDFromBlockType(blockType)
    {
        for(let item of this.units)
        {
            if(item.blockType !== blockType)
                continue;
            return item;
        }
        return null;
    }
    static showBlock(blockType, showStatus)
    {
        let unitID = this.getUnitIDFromBlockType(blockType);
        if(unitID !== null)
        {
            if(showStatus)
            {
                unitID.showStatus = true;
                unitID.htmlID.style.display = "block";
            }
            else
            {
                unitID.showStatus = false;
                unitID.htmlID.style.display = "none";
            }
            return true;
        }
    }
    // static getHTMLName(blockType)
    // {
    //     let unitID = this.getUnitIDFromBlockType(blockType);
    //     if(unitID !== null)
    //     {
    //         return unitID.htmlName;
    //     }
    // }
    static getHTMLID(blockType)
    {
        let unitID = this.getUnitIDFromBlockType(blockType);
        if(unitID !== null)
        {
            return unitID.htmlID;
        }
    }
    // static isBlockShow(blockType)
    // {
    //     let unitID = this.getUnitIDFromBlockType(blockType);
    //     if(unitID !== null)
    //     {
    //        return unitID.showStatus;
    //     }
    // }
}

function destroyTableBlock()
{
    isEdit = false;
    isFindSuccess = false;
    SuccessFindSN = null;
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, false);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, false);
    cButton.setShowForAll(false);
}



function getSerialNumberInfoData(snNumber)
{
    console.log(snNumber)
    if(!accessEdit)
    {
        return;
    }
    if(!snNumber || typeof snNumber !== 'string')
    {
        return;
    }

    if(query)
    {
        cmessBoxMain.sendErrorMessage("Запрос от сервера ещё не пришёл!")
        return;
    }

    // класс должен быть объявлен тут для капчи, иначе значение блока не будед перезаписываться
    let cCaptha = new CCaptha('div input[name=captcha-hash]', "captcha-text");
    let cresult = cCaptha.validate(cmessBoxMain);
    if(!cresult)
    {
        return false;
    }
    query = true;
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, true);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, false);

    let completed_json = JSON.stringify({
        captcha_hash: cresult.captcha_hash,
        captcha_text: cresult.captcha_text,
        csn_device: snNumber
    }); //$.parseJSON(json_text);


    $.ajax({
        data : completed_json,
        dataType: 'json',
        type : 'POST',
        url : './dsn_find_ajax',
        contentType: "application/json",
        success: function(data) {
            query = false;

            if(data.new_captha)
            {
                // update captha
                let capthaID = document.getElementById("captha_block_id");

                if(capthaID !== null)
                {
                    capthaID.innerHTML = data.new_captha
                }
            }

            HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, false);

            if(data.result === true)  // загрузка ASR
            {
                console.log(data.arr)

                if(isFindSuccess !== false)
                {
                    destroyTableBlock()
                }

                isEdit = false;
                isFindSuccess = true;
                SuccessFindSN = snNumber;
                HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, true);
                cButton.switchBTNStatus(TABLE_TYPE.TYPE_STANDART);
            }
            else
            {
                cmessBoxMain.sendErrorMessage(data.error_text);
            }
        },
        error: function(error) {
            // responseProcess = false
            if(isFindSuccess !== false)
            {
                destroyTableBlock()
            }
            cmessBoxMain.sendErrorMessage("Ошибка AJAX на стороне сервера!");
            return false
        }
    })


    return false;
}

function onUserPressedOnBTN(btnType)
{
    if(btnType === BUTTOM_TYPE.TYPE_EDIT)
    {

    }
    else if(btnType === BUTTOM_TYPE.TYPE_CANCEL)
    {

    }
    else if(btnType === BUTTOM_TYPE.TYPE_DEL)
    {

    }
    else if(btnType === BUTTOM_TYPE.TYPE_SAVE)
    {

    }
}

// ----------------------------------------------------------------- FUNC END

$(document).ready(function()
{
    let isValid = (numb) => (numb === 0 || numb === 1)

    accessDelete = document.getElementById("access_del");
    if(accessDelete)
    {
        accessDelete = +accessDelete.innerText;
        if(!isValid(accessDelete))
        {
            accessDelete = false;
        }
    }
    else
        accessDelete = false;

    accessEdit = document.getElementById("access_edit");
    if(accessEdit)
    {
        accessEdit = +accessEdit.innerText;
        if(!isValid(accessEdit))
        {
            accessEdit = false;
        }
    }

    else
        accessEdit = false;


    accessCreate = document.getElementById("access_create");
    if(accessCreate)
    {
        accessCreate = +accessCreate.innerText;
        if(!isValid(accessCreate))
        {
            accessCreate = false;
        }
    }
    else
        accessCreate = false;

    if(!accessEdit && !accessCreate && !accessDelete)
    {
        alert("Ошибка доступа!!!!")
        return;
    }

    let inputFieldSN = document.getElementById("dsn_name")
    if(inputFieldSN !== null)
    {
        $("#dsn_find").on("submit", function (event) {
            event.preventDefault(); // Отменяем стандартное поведение формы

            // Получаем данные из полей формы
            getSerialNumberInfoData(inputFieldSN.value);
        });
    }
    else
    {
        alert("Ошибка!!!!")
        return;
    }


    let units = [];
    units.push(new HTMLBlocks('load_anim_block',   HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK));
    units.push(new HTMLBlocks('dsn_result_block',   HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK));

    for(let item of units)
    {
        if(!item.isValidWithUnit())
        {
            alert("Ошибка!!!!")
            return;
        }
    }
    let btnEdit = document.getElementById("btn_edit");
    let btnDel = document.getElementById("btn_del");
    let btnSave = document.getElementById("btn_save");
    let btnCancel = document.getElementById("btn_cancel");

    if(
        !btnEdit ||
    !btnDel ||
    !btnSave ||
    !btnCancel)
    {
        alert("Ошибка!!!!")
        return;
    }

    if(btnEdit)
    {
        cButton.addBTN(btnEdit, "Редактировать", BUTTOM_TYPE.TYPE_EDIT);
        btnEdit.addEventListener("click", (event) =>
        {
            event.preventDefault(); // Отменяем стандартное поведение формы
            onUserPressedOnBTN(BUTTOM_TYPE.TYPE_EDIT);
        })
    }
    if(btnDel)
    {
        cButton.addBTN(btnDel, "Удалить", BUTTOM_TYPE.TYPE_DEL);
        btnDel.addEventListener("click", (event) =>
        {
            event.preventDefault(); // Отменяем стандартное поведение формы
            onUserPressedOnBTN(BUTTOM_TYPE.TYPE_DEL);
        })
    }
    if(btnSave)
    {
        cButton.addBTN(btnSave, "Сохранить", BUTTOM_TYPE.TYPE_SAVE);
        btnSave.addEventListener("click", (event) =>
        {
            event.preventDefault(); // Отменяем стандартное поведение формы
            onUserPressedOnBTN(BUTTOM_TYPE.TYPE_SAVE);
        })
    }
    if(btnCancel)
    {
        cButton.addBTN(btnCancel, "Отменить редактирование", BUTTOM_TYPE.TYPE_CANCEL);
        btnCancel.addEventListener("click", (event) =>
        {
            event.preventDefault(); // Отменяем стандартное поведение формы
            onUserPressedOnBTN(BUTTOM_TYPE.TYPE_CANCEL);
        })
    }

    cButton.setShowForAll(false)

    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, false);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, false);


    //let csrftoken = $('meta[name=csrf-token]').attr('content')
    let csrftoken = $('.container-common input[name=csrf_token]').attr('value')
    if(csrftoken)
    {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
        })
    }

}); // document ready
