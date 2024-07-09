
// Морда для просмотра и редактирования собранных устройств в базе
// Удаление, просмотр и редактирование
// Рязанов НВ ..2024
// ООО КВАНТ
// ЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫ


import {CMessBox} from "/static/js/engine/CMessBox.js"
import {
    CCaptha,
} from "/static/js/engine/CCaptha.js";
import {BUTTOM_TYPE, TABLE_TYPE} from "/static/js/engine/modules/pallets/common.js";

import {
    cButtons,
} from "/static/js/engine/modules/asr/CButtons.js";


let query = false;
let cmessBoxMain = new CMessBox("error_box_main");
let cmessBoxBlock = new CMessBox("error_box_block");
let cButton = new cButtons(); // класс управления кнопками
let accessDeletePallet, accessDeleteDevice, accessAddDevice, accessChangedStatus, accessChangedInfo, accessFind = null;
let palletSQLID = null;
let palletName = null;
let isSuccessFind = false;
let tableBlock = 'table_block_id';
let tableDeviceBlock = 'box_add_device';


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

class CDevice
{
    #deviceNumber = null;
    #deviceAssyID = null;
    #modelFK = null;
    #scannedDate = null;
    static units = [];
    constructor(cSN, deviceAssyID)
    {
        this.#deviceNumber = cSN;
        this.#deviceAssyID = deviceAssyID;
        this.constructor.units.push(this);
    }
    removeUnit()
    {
        this.constructor.units = this.constructor.units.filter((unitID) =>
            unitID !== this);
        return this.constructor.units;
    }
    isValid()
    {
        if(!this.#deviceNumber)
            return false;
    }
    getUnitIDFromDeviceNumber(dNumber)
    {
        for(let item of this.constructor.units)
        {
            if (item.#deviceNumber !== dNumber)
                continue;
            return item
        }
    }
    getUnitIDFromDeviceAssy(dAssy)
    {
        for(let item of this.constructor.units)
        {
            if (item.#deviceAssyID !== dAssy)
                continue;
            return item
        }
    }
    // setters
    setScannedDate = (cValue) => this.#scannedDate = cValue;
    setModelFK = (cValue) => this.#modelFK = cValue;

    // getters
    getScannedDate = () => this.#scannedDate;
    getModelFK = () => this.#modelFK;
    getAssy = () => this.#deviceAssyID;
    getDeviceSN = () => this.#deviceNumber;
    static getUnits = () => this.units;

    static clearUnits = () => this.units = [];

}

class CPalletInfo
{
    #textID;
    #textName;
    #EditStatus;
    #valueType;
    #inputType;
    #cValue;
    static units = [];

    constructor(cValue)
    {
        this.#cValue = cValue;

        this.constructor.units.push(this);
    }
    // SETTERS
    setTextID = (cValue) => this.#textID = cValue;
    setTextName = (cValue) => this.#textName = cValue;
    setEditStatus = (cValue) => this.#EditStatus = cValue;
    setValueType = (cValue) => this.#valueType = cValue;
    setInputType = (cValue) => this.#inputType = cValue;
    setValue = (cValue) => this.#cValue = cValue;

    getTextID = () => this.#textID;
    getTextName = () => this.#textName;
    getEditStatus = () => this.#EditStatus;
    getValueType = () => this.#valueType;
    getInputType = () => this.#inputType;
    getValue = () => this.#cValue;

    static getUnitIDFromTextID(textID)
    {
        for(let item of this.units)
        {
            if(item.getTextID() !== textID)
                continue;
            return item;
        }
    }


    static getUnits = () => this.units;
    static clearUnits = () => this.units = [];

}


function destroyTableBlock()
{
    if(palletName)
    {
        palletSQLID = null;
        palletName = null;
        isSuccessFind = false;
        DestroyUnits();
        tableBlock.innerHTML = '';
        tableDeviceBlock.innerHTML = '';
    }
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, false);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, false);
}

function onUserPressedOnBTN(btnType)
{
    if(btnType === BUTTOM_TYPE.TYPE_CANCEL)
    {
        if(palletName)
        {
            destroyTableBlock();
        }
    }
}

function DestroyUnits()
{
    CPalletInfo.clearUnits();
    CDevice.clearUnits();
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
    // if(isSuccessFind)
    // {
    //     if(snNumber === palletName)
    //     {
    //         cmessBoxMain.sendErrorMessage("Вы уже запросили этот серийный номер!")
    //         return
    //     }
    // }
    // if(isSuccessFind !== false)
    // {
    //     destroyTableBlock()
    // }
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
        url : './pallet_find_data_ajax',
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

            console.log(data.pallet_data)
            console.log(data.pallet_devices)
            if(data.result === true)
            {
                if(Array.isArray(data.pallet_data))
                {
                    let count = 0;
                    for(let item of data.pallet_data)
                    {
                        let [text_id, text_name, value_type, input_type, is_editting, cvalue] = item;
                        let unit = new CPalletInfo(cvalue);
                        unit.setInputType(input_type);
                        unit.setTextID(text_id);
                        unit.setValue(cvalue);
                        unit.setEditStatus(is_editting);
                        unit.setTextName(text_name);
                        unit.setValueType(value_type);
                        count++;
                    }
                    if(count)
                    {
                        let pUnit = CPalletInfo.getUnitIDFromTextID('pallet_sn');
                        if(pUnit)
                        {
                            palletName = pUnit.getValue();
                            pUnit = CPalletInfo.getUnitIDFromTextID('assy_id');
                            if(pUnit)
                            {
                                palletSQLID = pUnit.getValue();
                            }
                        }
                        if(palletName && palletSQLID)
                        {
                            let table = document.createElement('table');
                            table.id = 'parameters_table';
                            table.className = 'custom-table table-palletesn';
                            let tr = document.createElement('tr');
                            let th = document.createElement('th');
                            th.innerText = 'Параметр:'
                            tr.append(th)
                            th = document.createElement('th');
                            th.innerText = 'Значение:'
                            tr.append(th)
                            if(accessChangedInfo)
                            {
                                th = document.createElement('th');
                                th.innerText = 'Новое значение:'
                                tr.append(th)
                            }
                            table.append(tr)

                            let pUnits = CPalletInfo.getUnits();
                            count = 0;
                            pUnits.forEach( (element, index) => {

                                let textID = element.getTextID();
                                tr = document.createElement('tr');
                                th = document.createElement('td');
                                th.innerText = `${element.getTextName()}`;
                                tr.append(th)
                                th = document.createElement('td');

                                let inputType = element.getInputType();
                                if(inputType === 'input')
                                {
                                    th.innerText = `${element.getValue()}`;
                                }
                                else if(inputType === 'cb')
                                {
                                    th.innerText = `${element.getValue() ? 'Закрыт': 'Открыт'}`;
                                }
                                th.id = `old_info_table_value_${textID}`;
                                tr.append(th);

                                if(accessChangedInfo)
                                {
                                    th = document.createElement('td');

                                    let disabledField = false;
                                    if(!accessChangedStatus ||
                                        element.getEditStatus() === 'no-editable')
                                    {
                                        disabledField = true;
                                    }
                                    let vType = element.getValueType();


                                    if(inputType === 'input')
                                    {
                                        let input = document.createElement("input");
                                        input.type = "text";
                                        input.innerText = `${element.getValue()}`;
                                        input.placeholder = `${element.getValue()}`;

                                        if(vType === 'string')
                                        {
                                            input.maxLength = 64;
                                        }
                                        else if(vType === 'integer')
                                        {
                                            input.maxLength = 11;
                                        }

                                        input.minLength = 0;
                                        input.value = `${element.getValue()}`;
                                        input.id = `new_info_table_value_${textID}`;

                                        if(disabledField)
                                        {
                                            input.disabled = true;
                                        }
                                        else if(textID === 'completed_check')
                                        {
                                            if(!accessChangedStatus)
                                            {
                                                input.disabled = true;
                                            }
                                        }
                                        th.append(input);
                                    }
                                    else if(inputType === 'cb')
                                    {
                                        let input = document.createElement("input");
                                        input.type = "checkbox";
                                        input.checked = element.getValue();

                                        if(disabledField)
                                        {
                                            input.disabled = true;
                                        }
                                        else if(textID === 'completed_check')
                                        {
                                            if(!accessChangedStatus)
                                            {
                                                input.disabled = true;
                                            }
                                        }
                                        input.id = `new_info_table_value_${textID}`;
                                        th.append(input);
                                    }

                                    tr.append(th);

                                }
                                table.append(tr);
                                count++;
                            })
                            if(count)
                            {
                                tableBlock.append(table);

                                if(Array.isArray(data.pallet_devices))
                                {
                                    let count = 0;
                                    for(let device of data.pallet_devices)
                                    {
                                        let
                                            {
                                                device_assy: assyID,
                                                device_sn: deviceSN,
                                                model_fk: modelFK,
                                                scanned_data: scannedDate
                                            } = device;
                                        if(assyID && deviceSN && modelFK)
                                        {
                                            let unit = new CDevice(assyID, deviceSN);
                                            unit.setScannedDate(scannedDate);
                                            unit.setModelFK(modelFK);
                                            count++;
                                        }
                                        else
                                        {
                                            cmessBoxMain.sendErrorMessage("Не могу обработать параметры устройства!");
                                            destroyTableBlock();
                                            break;
                                        }
                                    }
                                    if(count)
                                    {
                                        let table = document.createElement('table');
                                        table.id = 'device_table';
                                        table.className = 'custom-table table-palletesn';
                                        let tr = document.createElement('tr');
                                        let th = document.createElement('th');
                                        th.innerText = 'Номер устройства в БД:'
                                        tr.append(th)
                                        th = document.createElement('th');
                                        th.innerText = 'Серийный номер устройства:'
                                        tr.append(th)
                                        th = document.createElement('th');
                                        th.innerText = 'ID модели:'
                                        tr.append(th)
                                        th = document.createElement('th');
                                        th.innerText = 'Дата сканировки:'
                                        tr.append(th)
                                        th = document.createElement('th');
                                        th.innerText = 'Действие:'
                                        tr.append(th)
                                        table.append(tr)

                                        let units = CDevice.getUnits();
                                        console.log(units)
                                        for(let device of units)
                                        {
                                            let deviceSN = device.getDeviceSN();
                                            let scannedDate = device.getScannedDate();
                                            let deviceAssy = device.getAssy();
                                            let modelFK = device.getModelFK();

                                            tr = document.createElement('tr');
                                            th = document.createElement('td');
                                            th.innerText = deviceSN;
                                            tr.append(th)
                                            th = document.createElement('td');
                                            th.innerText = deviceAssy;
                                            tr.append(th)
                                            th = document.createElement('td');
                                            th.innerText = modelFK;
                                            tr.append(th)
                                            th = document.createElement('td');
                                            th.innerText = scannedDate;
                                            tr.append(th)
                                            th = document.createElement('td');
                                            if(accessDeleteDevice)
                                            {
                                                let btn = document.createElement('button');
                                                btn.id = 'btn_del_device'
                                                btn.innerText = 'Удалить'
                                                btn.className = 'btm_submit-common'
                                                th.append(btn)
                                            }
                                            else
                                            {
                                                th.innerText = '-'
                                            }

                                            tr.append(th)
                                            table.append(tr)
                                        }
                                        tableDeviceBlock.append(table);
                                    }
                                }
                                HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, false);
                                HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, true);

                            }
                        }
                        else
                        {
                            DestroyUnits();
                            cmessBoxMain.sendErrorMessage("Не могу обработать параметры паллета!");
                        }
                    }
                    else
                        cmessBoxMain.sendErrorMessage("Ошибка получения данных!");
                }
                else
                    cmessBoxMain.sendErrorMessage("Ошибка получения данных паллета!");
            }
            else
                cmessBoxMain.sendErrorMessage(data.error_text);
        },
        error: function(error) {
            // responseProcess = false
            if(isSuccessFind !== false)
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

// ----------------------------------------------------------------- FUNC END

$(document).ready(function()
{
    tableBlock = document.getElementById(tableBlock);
    if(!tableBlock)
    {
        alert("Не могу найти блок для вставки главной таблицы!")
        return
    }

    tableDeviceBlock = document.getElementById(tableDeviceBlock);
    if(!tableDeviceBlock)
    {
        alert("Не могу найти блок для вставки таблицы устройств!")
        return
    }




    let isValid = (numb) => (numb === 0 || numb === 1)

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

    accessDeletePallet = document.getElementById("access_del_all");
    if(accessDeletePallet)
    {
        accessDeletePallet = +accessDeletePallet.innerText;
        if(!isValid(accessDeletePallet))
        {
            accessDeletePallet = false;
        }
    }

    else
        accessDeletePallet = false;

    accessDeleteDevice = document.getElementById("access_del_device");
    if(accessDeleteDevice)
    {
        accessDeleteDevice = +accessDeleteDevice.innerText;
        if(!isValid(accessDeleteDevice))
        {
            accessDeleteDevice = false;
        }
    }
    else
        accessDeleteDevice = false;

    accessChangedStatus = document.getElementById("access_changed_status");
    if(accessChangedStatus)
    {
        accessChangedStatus = +accessChangedStatus.innerText;
        if(!isValid(accessChangedStatus))
        {
            accessChangedStatus = false;
        }
    }
    else
        accessChangedStatus = false;


    accessChangedInfo = document.getElementById("access_changed_info");
    if(accessChangedInfo)
    {
        accessChangedInfo = +accessChangedInfo.innerText;
        if(!isValid(accessChangedInfo))
        {
            accessChangedInfo = false;
        }
    }
    else
        accessChangedInfo = false;

    accessAddDevice = document.getElementById("access_add_tv");
    if(accessAddDevice)
    {
        accessAddDevice = +accessAddDevice.innerText;
        if(!isValid(accessAddDevice))
        {
            accessAddDevice = false;
        }
    }
    else
        accessAddDevice = false;

    const arr = [
        accessChangedInfo,
        accessChangedStatus,
        accessAddDevice,
        accessFind,
        accessDeleteDevice,
        accessDeletePallet
        ]

    for(let item in arr)
    {
        if(!item)
        {
            alert("Ошибка доступа 1!!!!")
            return;
        }
    }

    let inputFieldSN = document.getElementById("pallets_name")
    if(inputFieldSN !== null)
    {
        $("#pallets_find").on("submit", function (event) {
            event.preventDefault(); // Отменяем стандартное поведение формы

            // Получаем данные из полей формы
            getSerialNumberInfoData(inputFieldSN.value);
        });
    }
    else
    {
        alert("Ошибка 2!!!!")
        return;
    }

    let units = [];
    units.push(new HTMLBlocks('load_anim_block',   HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK));
    units.push(new HTMLBlocks('pallets_result_block',   HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK));

    for(let item of units)
    {
        if(!item.isValidWithUnit())
        {
            alert("Ошибка 3!!!!")
            return;
        }
    }
    let btnAddDevice = document.getElementById("btn_add_device");
    let btnDelPallet = document.getElementById("btn_del_all");
    let btnCancel = document.getElementById("btn_cancel");

    if(!btnCancel)
    {
        alert("Ошибка 4!!!!")
        return;
    }
    btnCancel.addEventListener("click", (event) =>
    {
        event.preventDefault(); // Отменяем стандартное поведение формы
        onUserPressedOnBTN(BUTTOM_TYPE.TYPE_CANCEL);
    })


    if(accessDeletePallet)
    {
        if(!btnDelPallet)
        {
            alert("Ошибка 5!!!!")
            return;
        }
        btnDelPallet.addEventListener("click", (event) =>
        {
            event.preventDefault(); // Отменяем стандартное поведение формы
            onUserPressedOnBTN(BUTTOM_TYPE.TYPE_DELETE_PALLET);
        })
    }
    if(accessAddDevice)
    {
        if(!btnAddDevice)
        {
            alert("Ошибка 5!!!!")
            return;
        }
        btnAddDevice.addEventListener("click", (event) =>
        {
            event.preventDefault(); // Отменяем стандартное поведение формы
            onUserPressedOnBTN(BUTTOM_TYPE.TYPE_ADD_DEVICE);
        })
    }

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
