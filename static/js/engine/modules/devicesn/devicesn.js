
// Морда для просмотра и редактирования собранных устройств в базе
// Удаление, просмотр и редактирование
// Рязанов НВ ..2024
// ООО КВАНТ
// ЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫ


import {CMessBox} from "/static/js/engine/CMessBox.js"
import {
    CCaptha,
} from "/static/js/engine/CCaptha.js";
import {BUTTOM_TYPE, TABLE_TYPE} from "/static/js/engine/modules/devicesn/common.js";

import {
    cButtons,
} from "/static/js/engine/modules/asr/CButtons.js";


let query = false;
let cmessBoxMain = new CMessBox("error_box_main");
let cmessBoxBlock = new CMessBox("error_box_block");
let cButton = new cButtons(); // класс управления кнопками
let accessDelete, accessEdit, accessCreate, accessFind = null;
let isEdit = false;
let isFindSuccess = false;
let SuccessFindSN = null;
let tableID = null;


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
    if(tableID)
    {
        tableID.remove();
        tableID = null;
    }
    // HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, false);
    // HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, false);
    cButton.setShowForAll(false);
    CParameters.removeUnits();
}

class CParameters
{
    textID = null;
    textName = null;
    varType = null;
    currentValue = null;
    isEdit = false;
    static units = [];

    constructor()
    {
        this.constructor.units.push(this);
    }

    static getUnits()
    {
        if(this.units.length)
        {
            return this.units;
        }
        return false;
    }
    static removeUnits()
    {
        this.units = [];
    }
    static getUnitIDFromTextID(textID)
    {
        for(let item of this.units)
        {
            if(item.getTextID() === textID)
            {
                return item;
            }
        }
    }

    removeUnit()
    {
        this.constructor.units = this.constructor.units.filter((unitID) =>
            unitID !== this);
        return this.constructor.units;
    }
    isValid()
    {
        for(let item of [this.textID, this.textName])
        {
            if(!item)
                return false;
        }
        return true;
    }


    setTextID = (varValue) => this.textID = varValue;
    setTextName = (varValue) => this.textName = varValue;
    setCurrentValue = (varValue) => this.currentValue = varValue;
    setIsEdit = (varValue) => this.isEdit = varValue;
    setVarType = (varValue) => this.varType = varValue;

    getTextID = () => this.textID;
    getTextName = () => this.textName;
    getCurrentValue = () => this.currentValue;
    getIsEdit = () => this.isEdit;
    getVarType = () => this.varType;
}

function CreateTable(tableType)
{
    let block = document.getElementById('table_dsn_id');
    if(block)
    {
        if(isFindSuccess)
        {
            block.innerHTML = '';
        }

        let table = document.createElement('table');

        if(table)
        {
            table.id = 'parameters_table';
            table.className = 'custom-table table-devicesn';
            tableID = table;
            if(tableType === TABLE_TYPE.TYPE_STANDART)
            {
                let tr = document.createElement('tr');
                let th = document.createElement('th');
                th.innerText = 'Параметр:'
                tr.append(th)
                th = document.createElement('th');
                th.innerText = 'Значение:'
                tr.append(th)
                table.append(tr)

                let arr = CParameters.getUnits();
                for(let item of arr)
                {
                    let currentValue = item.getCurrentValue();
                    if(!currentValue)
                        continue  // костыль что бы пустые столбцы не показывались(так попизже)
                    let textID = item.getTextID();
                    let textName = item.getTextName();
                    let varType = item.getVarType();
                    // is valid не нужна так как уже была проверка во время загрузки
                    if(varType === 'string' || varType === 'integer' || varType === 'date')
                    {
                        if(!currentValue)
                        {
                            currentValue = '';
                        }
                    }

                    let tr = document.createElement('tr');
                    let th = document.createElement('td');
                    th.innerText = textName;
                    tr.append(th)
                    th = document.createElement('td');
                    th.innerText = currentValue;
                    th.id = `old_table_value_${textID}`;
                    tr.append(th);
                    table.append(tr);
                }
            }
            else if(tableType === TABLE_TYPE.TYPE_EDITTING)
            {
                let tr = document.createElement('tr');
                let th = document.createElement('th');
                th.innerText = 'Параметр:'
                tr.append(th)
                th = document.createElement('th');
                th.innerText = 'Старое значение:'
                tr.append(th)
                th = document.createElement('th');
                th.innerText = 'Новое значение:'
                tr.append(th)
                table.append(tr)


                let arr = CParameters.getUnits();
                for(let item of arr)
                {
                    let textID = item.getTextID();
                    let textName = item.getTextName();
                    let currentValue = item.getCurrentValue();
                    let varType = item.getVarType();
                    let isEdit = item.getIsEdit();

                    // is valid не нужна так как уже была проверка во время загрузки
                    if(varType === 'string' || varType === 'integer' || varType === 'date')
                    {
                        if(!currentValue)
                        {
                            currentValue = '';
                        }
                    }

                    let tr = document.createElement('tr');
                    let th = document.createElement('td');
                    th.innerText = textName;
                    tr.append(th)
                    th = document.createElement('td');
                    th.innerText = currentValue;
                    th.id = `old_table_value_${textID}`;
                    if(!isEdit)
                    {
                        th.disabled = true;
                    }
                    tr.append(th)

                    th = document.createElement('td');
                    let input = document.createElement("input");
                    input.type = "text";
                    input.innerText = currentValue;
                    input.placeholder = currentValue;
                    input.maxLength = 64;
                    input.minLength = 0;
                    input.value = currentValue;
                    input.id = `new_table_value_${textID}`;
                    if(!isEdit)
                    {
                        input.disabled = true;
                    }
                    th.append(input);
                    tr.append(th);

                    table.append(tr);
                }
            }
            block.append(table);
        }
    }
}




function getSerialNumberInfoData(snNumber)
{
    console.log(snNumber)
    if(!accessFind)
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
    if(isFindSuccess)
    {
        if(SuccessFindSN !== null)
        {
            if(snNumber === SuccessFindSN)
            {
                cmessBoxMain.sendErrorMessage("Вы уже запросили этот серийный номер!")
                return
            }
        }
    }
    if(isFindSuccess !== false)
    {
        destroyTableBlock()
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
                if (Array.isArray(data.arr))
                {
                    console.log(data.arr)
                    let count = 0;
                    for(let item of data.arr)
                    {
                        console.log(item)
                        let textID = item.text_id;
                        let textName = item.text_name;
                        let isEditable = item.is_editable;
                        let currentValue = item.current_value;
                        let valueType = item.value_type;

                        let parameter = new CParameters();
                        parameter.setTextID(textID);
                        parameter.setTextName(textName);
                        parameter.setIsEdit(isEditable);
                        parameter.setVarType(valueType);
                        parameter.setCurrentValue(currentValue);

                        if(!parameter.isValid())
                        {
                            parameter.removeUnit();
                            continue
                        }

                        count++;
                    }
                    if(count)
                    {
                        isEdit = false;
                        isFindSuccess = true;
                        SuccessFindSN = snNumber;
                        CreateTable(TABLE_TYPE.TYPE_STANDART);
                        HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, true);
                        cButton.switchBTNStatus(TABLE_TYPE.TYPE_STANDART);
                    }
                }
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
                HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, false);
                HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, false);
            }
            cmessBoxMain.sendErrorMessage("Ошибка AJAX на стороне сервера!");
        }
    })


    return false;
}
function gotoToMainBlock()
{
    document.querySelector("#dsn_find").scrollIntoView({
        behavior: 'smooth'
    });
}
function onUserPressedOnBTN(btnType)
{
    if(btnType === BUTTOM_TYPE.TYPE_EDIT)
    {
        if(accessEdit)
        {
            if(isFindSuccess)
            {
                if(!isEdit)
                {
                    CreateTable(TABLE_TYPE.TYPE_EDITTING);
                    cButton.switchBTNStatus(TABLE_TYPE.TYPE_EDITTING);
                    isEdit = true;
                }
            }
        }
    }
    else if(btnType === BUTTOM_TYPE.TYPE_CANCEL)
    {
        if(isFindSuccess)
        {
            if(isEdit)
            {
                CreateTable(TABLE_TYPE.TYPE_STANDART);
                cButton.switchBTNStatus(TABLE_TYPE.TYPE_STANDART);
                isEdit = false;
            }
        }
    }
    else if(btnType === BUTTOM_TYPE.TYPE_DEL)
    {
        if(accessDelete)
        {
            if(isFindSuccess)
            {
                if (confirm(`"Вы действительно хотите удалить выбранный SN '${SuccessFindSN}' из базы готовых изделий ?
            \nОтменить действие будет невозможно!"`)) // yes
                {
                    if(query)
                        return

                    let serial = SuccessFindSN;
                    let assy = CParameters.getUnitIDFromTextID('db_primary_key');
                    assy = Number(assy.getCurrentValue());


                    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, true);

                    if(!assy)
                        return

                    let completed_json = JSON.stringify({
                        serial_number: serial,
                        assy_id: assy,
                    }); //$.parseJSON(json_text);


                    $.ajax({
                        data : completed_json,
                        dataType: 'json',
                        type : 'POST',
                        url : './dsn_delete_sn_ajax',
                        contentType: "application/json",
                        success: function(data) {
                            query = false;
                            HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, false);

                            if(data.hasOwnProperty('reset_table'))
                            {
                                destroyTableBlock();
                                HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, true);
                            }


                            if(data.result === true)  // удалился успешно
                            {
                                cmessBoxMain.sendSuccessMessage(data.error_text);
                            }
                            else
                            {
                                gotoToMainBlock();
                                cmessBoxMain.sendErrorMessage(data.error_text);
                            }
                        },
                        error: function(error) {
                            // responseProcess = false

                            cmessBoxMain.sendErrorMessage("Ошибка AJAX на стороне сервера!");
                            return false
                        }
                    })
                }
            }
        }
    }
    else if(btnType === BUTTOM_TYPE.TYPE_SAVE)
    {
        if(accessEdit)
        {
            if(isFindSuccess)
            {
                if(isEdit)
                {
                    if(query)
                        return

                    let arr = CParameters.getUnits();
                    let arr_result = [];
                    let count = 0;
                    let isError = false;
                    for(let item of arr)
                    {
                        let textID = item.getTextID();
                        let element = document.getElementById(`new_table_value_${textID}`);
                        if(element)
                        {
                            if(!item.getIsEdit())
                                continue

                            let oldValue = item.getCurrentValue();
                            let varType = item.getVarType();

                            let currentValue = element.value;

                            if(varType === 'string')
                            {
                                currentValue = String(currentValue);
                            }
                            else if(varType === 'integer')
                            {
                                currentValue = Number(currentValue);
                            }
                            else if(varType === 'date')
                            {
                                currentValue = String(currentValue);
                            }

                            if(currentValue === oldValue)
                                continue

                            arr_result.push([textID, oldValue, currentValue, element, varType]);
                            count++;
                        }
                    }
                    if(count)
                    {
                        console.log(arr_result)

                        let serial = SuccessFindSN;
                        let assy = CParameters.getUnitIDFromTextID('db_primary_key');
                        assy = Number(assy.getCurrentValue());

                        if(!assy)
                            return

                        let completed_json = JSON.stringify({
                            serial_number: serial,
                            assy_id: assy,
                            arr: arr_result
                        }); //$.parseJSON(json_text);
                        HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, true);

                        $.ajax({
                            data : completed_json,
                            dataType: 'json',
                            type : 'POST',
                            url : './dsn_save_edit_sn_ajax',
                            contentType: "application/json",
                            success: function(data) {
                                query = false;

                                HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, false);

                                if(data.result === true)  // удалился успешно
                                {
                                    // cmessBoxMain.sendSuccessMessage(data.error_text);
                                    let count = 0;
                                    for(let arr of arr_result)
                                    {
                                        let [textID, , currentValue, htmlID, ] = arr;
                                        let old_element = document.getElementById(`old_table_value_${textID}`);

                                        if(old_element)
                                        {
                                            old_element.innerText = currentValue;
                                        }

                                        htmlID.value = currentValue;
                                        htmlID.placeholder = currentValue;

                                        let unit = CParameters.getUnitIDFromTextID(textID);
                                        if(unit)
                                        {
                                            unit.setCurrentValue(currentValue);
                                        }
                                        count++;
                                    }
                                    if(count !== arr_result.length || data.reload_block)
                                    {
                                        destroyTableBlock();
                                        HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, false);
                                        HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, false);

                                        document.querySelector("#dsn_find").scrollIntoView({
                                            behavior: 'smooth'
                                        });
                                    }
                                    else
                                    {
                                        document.querySelector("#dsn_result_block").scrollIntoView({
                                            behavior: 'smooth'
                                        });
                                    }

                                    if(count !== arr_result.length)
                                        cmessBoxMain.sendErrorMessage("Возникла ошибка в обработчике!");
                                    else if(data.reload_block)
                                        cmessBoxMain.sendWarningMessage("Ключевое поле изменено! Режим поиска сброшен!");
                                    else
                                        cmessBoxBlock.sendSuccessMessage('Данные успешно изменены!');
                                }
                                else
                                {
                                    document.querySelector("#dsn_result_block").scrollIntoView({
                                        behavior: 'smooth'
                                    });
                                    cmessBoxBlock.sendErrorMessage(data.error_text);
                                }
                            },
                            error: function(error) {
                                // responseProcess = false

                                cmessBoxMain.sendErrorMessage("Ошибка AJAX на стороне сервера!");
                                return false
                            }
                        })
                    }
                    else
                    {
                        cmessBoxBlock.sendWarningMessage("Вы пока ещё не вносили изменений!");
                        document.querySelector("#dsn_result_block").scrollIntoView({
                            behavior: 'smooth'
                        });
                    }
                }
            }
        }
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

    accessFind = document.getElementById("access_find");
    if(accessFind)
    {
        accessFind = +accessFind.innerText;
        if(!isValid(accessFind))
        {
            accessFind = false;
        }
    }
    else
        accessFind = false;


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

    if(!accessEdit && !accessCreate && !accessDelete && !accessFind)
    {
        alert("Ошибка доступа 2!!!!")
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
        alert("Ошибка 3!!!!")
        return;
    }


    let units = [];
    units.push(new HTMLBlocks('load_anim_block',   HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK));
    units.push(new HTMLBlocks('dsn_result_block',   HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK));

    for(let item of units)
    {
        if(!item.isValidWithUnit())
        {
            alert("Ошибка 4!!!!")
            return;
        }
    }
    let btnEdit = document.getElementById("btn_edit");
    let btnDel = document.getElementById("btn_del");
    let btnSave = document.getElementById("btn_save");
    let btnCancel = document.getElementById("btn_cancel");

    if(accessEdit)
    {
        if(
            !btnEdit ||
            !btnSave ||
            !btnCancel)
        {
            alert("Ошибка 5!!!!")
            return;
        }
    }
    if(accessDelete)
    {
        if(!btnDel)
        {
            alert("Ошибка 5!!!!")
            return;
        }
    }

    // if(
    //     !btnEdit ||
    // !btnDel ||
    // !btnSave ||
    // !btnCancel)
    // {
    //     alert("Ошибка 5!!!!")
    //     return;
    // }

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
