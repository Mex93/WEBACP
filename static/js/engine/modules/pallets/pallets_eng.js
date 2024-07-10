
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
let tableDeviceBlockID = 'box_devices';
let tableDevicesIDName = 'device_table';
const MAX_PALLET_PLACES = 5*12


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
        return this.#deviceNumber;
    }
    static getDeviceCount()
    {
        let count = 0;
        this.units.forEach( (element) =>
        {
            if(!element.isValid())
                return
            count ++;
        })

        return count;
    }
    static getUnitIDFromDeviceNumber(dNumber)
    {
        for(let item of this.units)
        {
            if (item.#deviceNumber !== dNumber)
                continue;
            return item
        }
        return false;
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

function onUserPressedBtnDeviceDel(deviceUnit)
{
    if(deviceUnit)
    {
        if(accessDeleteDevice)
        {
            if(isSuccessFind)
            {
                let deviceSN = deviceUnit.getDeviceSN();
                if(!deviceSN)
                    return

                if (confirm(`"Вы действительно хотите удалить устройство '${deviceSN}' с паллета '${palletName}' ?
            \nОтменить действие будет невозможно!"`)) // yes
                {
                    if(query)
                    {
                        cmessBoxMain.sendErrorMessage("Запрос от сервера ещё не пришёл!")
                        return;
                    }
                    let destroyPallet = () =>
                    {
                        destroyTableBlock();
                        gotoToMainBlock();
                    }
                    if(CDevice.getUnitIDFromDeviceNumber(deviceSN) !== false)
                    {
                        let assy = deviceUnit.getAssy();
                        if(assy)
                        {
                            query = true;
                            let completed_json = JSON.stringify({
                                pallet_sn: palletName,
                                pallet_sql_id: palletSQLID,
                                device_sn: deviceSN,
                                device_assy: assy
                            }); //$.parseJSON(json_text);

                            $.ajax({
                                data : completed_json,
                                dataType: 'json',
                                type : 'POST',
                                url : './pallet_delete_device_ajax',
                                contentType: "application/json",
                                success: function(data) {
                                    query = false;

                                    if (data.result === true)
                                    {
                                        cmessBoxBlock.sendSuccessMessage(data.error_text);

                                        deviceUnit.removeUnit();

                                        let html_text_id = `device_field_${assy}`
                                        let tr = document.getElementById(html_text_id);
                                        if(tr)
                                        {
                                            tr.remove();

                                            let count = CDevice.getDeviceCount();
                                            if(!count)
                                            {
                                                let table = document.getElementById(tableDevicesIDName);
                                                if(table)
                                                    table.remove();
                                            }
                                        }
                                        else
                                        {
                                            cmessBoxBlock.sendErrorMessage('Ошибка вычисления tr ID');
                                            destroyPallet();
                                        }


                                    }
                                    else
                                    {
                                        cmessBoxBlock.sendErrorMessage(data.error_text);

                                        if(data.hasOwnProperty('reset_pallet'))
                                        {
                                            if(data.reset_pallet === true)
                                            {
                                                destroyPallet();
                                            }
                                        }
                                    }

                                },
                                error: function(error) {
                                    // responseProcess = false
                                    cmessBoxMain.sendErrorMessage("Ошибка AJAX на стороне сервера!");
                                    gotoToMainBlock();
                                }
                            });
                        }
                        else
                        {
                            cmessBoxBlock.sendErrorMessage('Ошибка вычисления assY ID');
                            destroyPallet();
                        }
                    }
                    else
                    {
                        cmessBoxBlock.sendErrorMessage('В паллете нет этого устройства!');
                        destroyPallet();
                    }
                }
            }
        }
    }
}


function createTableDeviceHeader()
{
    if(!document.getElementById(tableDevicesIDName))
    {
        let table = document.createElement('table');
        table.id = tableDevicesIDName;
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
        return table;
    }
   return null;
}


function createTableDeviceBody(table, deviceUnit)
{
    let deviceSN = deviceUnit.getDeviceSN();
    let scannedDate = deviceUnit.getScannedDate();
    let deviceAssy = deviceUnit.getAssy();
    let modelFK = deviceUnit.getModelFK();

    let tr = document.createElement('tr');
    tr.id = `device_field_${deviceAssy}`
    let th = document.createElement('td');
    th.innerText = deviceAssy;
    tr.append(th)
    th = document.createElement('td');
    th.innerText = deviceSN;
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
        btn.id = `btn_del_device_${deviceAssy}`
        btn.innerText = 'Удалить'
        btn.classList.add('btm_submit-common');
        btn.classList.add('btn_del_device');

        th.append(btn)

        if(btn)
        {
            btn.addEventListener("click", function (element) {
                onUserPressedBtnDeviceDel(deviceUnit);
            })
        }
    }
    else
    {
        th.innerText = '-'
    }

    tr.append(th)
    table.append(tr)
}


function destroyTableBlock()
{
    if(isSuccessFind)
    {
        palletSQLID = null;
        palletName = null;
        isSuccessFind = false;
        DestroyUnits();
        tableBlock.innerHTML = '';
        tableDeviceBlockID.innerHTML = '';
    }
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, false);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, false);
}

function onUserPressedOnBTN(btnType)
{
    if(btnType === BUTTOM_TYPE.TYPE_CANCEL)
    {
        if(isSuccessFind)
        {
            destroyTableBlock();
            gotoToMainBlock();
        }
    }
    else if(btnType === BUTTOM_TYPE.TYPE_ADD_DEVICE)
    {
        if(accessAddDevice)
        {
            if(isSuccessFind)
            {
                let result = prompt(`Укажите серийный номер устройства, что бы добавить в паллет '${palletName}'.\n\n\
                Условия добавления:\n\
                - Паллет должен быть не заполнен выше максимального значения в ${MAX_PALLET_PLACES} штук.\n\
                - Устройство должно быть собрано на сборочном конвейере.\n\
                - Устройство должно физически находится на паллете.\n\
                - Устройство не должно быть привязано к выбранному или другому паллету.\n\
                - Устройство, во время сборки на сборочном конвейере, должно успешно пройти операцию сканировки на упаковке.\n\
                - Сборочная линия устройства и паллета должны совпадать.\n\n\
               Нажмите 'ОК', что бы добавить устройство:`, '');

                if(result)  // ввёл что либо или окно пустое
                {
                    let deviceSN = result.toUpperCase();
                    if(deviceSN.length > 10)
                    {
                        if(query)
                        {
                            cmessBoxMain.sendErrorMessage("Запрос от сервера ещё не пришёл!")
                            return;
                        }
                        if(!CDevice.getUnitIDFromDeviceNumber(deviceSN))
                        {
                            if(CDevice.getDeviceCount() < MAX_PALLET_PLACES)
                            {
                                query = true;
                                let completed_json = JSON.stringify({
                                    pallet_sn: palletName,
                                    pallet_sql_id: palletSQLID,
                                    device_sn: deviceSN
                                }); //$.parseJSON(json_text);

                                $.ajax({
                                    data : completed_json,
                                    dataType: 'json',
                                    type : 'POST',
                                    url : './pallet_add_device_ajax',
                                    contentType: "application/json",
                                    success: function(data) {
                                        query = false;

                                        let destroyPallet = () =>
                                        {
                                            destroyTableBlock();
                                            cmessBoxMain.sendErrorMessage("Возникла ошибка. Паллет сброшен!");
                                            gotoToMainBlock();
                                        }

                                        if (data.result === true)
                                        {
                                            //let countInPallet = CDevice.getDeviceCount();
                                            let table = document.getElementById(tableDevicesIDName);
                                            if(!table)  // если ноль, то создать таблицу
                                            {
                                                table = createTableDeviceHeader();
                                                if(!table)
                                                {
                                                    destroyPallet();
                                                    return
                                                }
                                                else
                                                {
                                                    tableDeviceBlockID.append(table);
                                                }
                                            }
                                            if(table)
                                            {
                                                let assy = data.assyid;
                                                let modelFK = data.model_fk;
                                                let scannedDate = data.scanned_data;
                                                if(assy && modelFK && scannedDate)
                                                {
                                                    let unit = new CDevice(deviceSN, assy);
                                                    unit.setScannedDate(scannedDate);
                                                    unit.setModelFK(modelFK);
                                                    createTableDeviceBody(table, unit)
                                                }
                                            }
                                            cmessBoxBlock.sendSuccessMessage(data.error_text);
                                        }
                                        else
                                        {
                                            gotoToDeviceBlock();
                                            cmessBoxBlock.sendErrorMessage(data.error_text);
                                            if(data.hasOwnProperty('reset_pallet'))
                                            {
                                                if(data.reset_pallet === true)
                                                {
                                                    destroyPallet();
                                                }
                                            }
                                        }

                                    },
                                    error: function(error) {
                                        // responseProcess = false
                                        gotoToMainBlock();
                                        cmessBoxMain.sendErrorMessage("Ошибка AJAX на стороне сервера!");
                                    }
                                })
                            }
                            else
                                cmessBoxBlock.sendErrorMessage("Паллет уже заполнен максимально!")
                        }
                        else
                            cmessBoxBlock.sendErrorMessage("Указанное устройство уже есть в выбранном паллете!")
                    }
                    else
                        cmessBoxBlock.sendErrorMessage("Длинна SN устройства слишком мала!")
                }
            }
        }

    }
    else if(btnType === BUTTOM_TYPE.TYPE_DELETE_PALLET)
    {
        if(accessDeletePallet)
        {
            if(isSuccessFind)
            {
                if (confirm(`"Вы действительно хотите удалить выбранный паллет '${palletName}' ?
                \nОтменить действие будет невозможно!\n
                Содержимое паллета будет удалено!"`)) // yes
                 {
                     if(query)
                     {
                         cmessBoxMain.sendErrorMessage("Запрос от сервера ещё не пришёл!")
                         return;
                     }
                     query = true;
                     let completed_json = JSON.stringify({
                         pallet_sn: palletName,
                         pallet_sql_id: palletSQLID
                     }); //$.parseJSON(json_text);

                     $.ajax({
                         data : completed_json,
                         dataType: 'json',
                         type : 'POST',
                         url : './pallet_delete_all_ajax',
                         contentType: "application/json",
                         success: function(data) {
                             query = false;
                             if(isSuccessFind)
                                 destroyTableBlock();

                             if (data.result === true)
                             {
                                 cmessBoxMain.sendSuccessMessage(data.error_text);
                             }
                             else
                                cmessBoxMain.sendErrorMessage(data.error_text);

                             gotoToMainBlock();
                         },
                         error: function(error) {
                                 // responseProcess = false
                                 cmessBoxMain.sendErrorMessage("Ошибка AJAX на стороне сервера!");
                             }
                     })
                 }
            }
        }

    }
}

function DestroyUnits()
{
    CPalletInfo.clearUnits();
    CDevice.clearUnits();
}

function gotoToPalletBlock()
{
    document.querySelector("#table_block_id").scrollIntoView({
        behavior: 'smooth'
    });
}
function gotoToDeviceBlock()
{
    document.querySelector("#box_devices").scrollIntoView({
        behavior: 'smooth'
    });
}
function gotoToMainBlock()
{
    document.querySelector("#pallets_find").scrollIntoView({
        behavior: 'smooth'
    });
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

    // класс должен быть объявлен тут для капчи, иначе значение блока не будед перезаписываться
    let cCaptha = new CCaptha('div input[name=captcha-hash]', "captcha-text");
    let cresult = cCaptha.validate(cmessBoxMain);
    if(!cresult)
    {
        return false;
    }

    if(!isSuccessFind)
    {
        HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, false);
    }
    else
    {
        if(palletName === snNumber)
        {
            cmessBoxMain.sendErrorMessage("Вы уже запросили этот паллет!")
            return;
        }
    }
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_BLOCK, true);

    query = true;
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
                    if(isSuccessFind)
                        destroyTableBlock()


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
                                isSuccessFind = true;
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
                                    let value = element.getValue();
                                    value = value === null ? '': value;
                                    th.innerText = `${value}`;
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
                                        let value = element.getValue();
                                        value = value === null ? '': value;

                                        let input = document.createElement("input");
                                        input.type = "text";
                                        input.innerText = `${value}`;
                                        input.placeholder = `${value}`;

                                        if(vType === 'string')
                                        {
                                            input.maxLength = 64;
                                        }
                                        else if(vType === 'integer')
                                        {
                                            input.maxLength = 11;
                                        }

                                        input.minLength = 0;
                                        input.value = `${value}`;
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
                                gotoToPalletBlock();
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
                                            let unit = new CDevice(deviceSN, assyID);
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
                                        table = createTableDeviceHeader();
                                        if(table)
                                        {
                                            let units = CDevice.getUnits();
                                            //console.log(units)
                                            for(let device of units)
                                            {
                                                createTableDeviceBody(table, device);
                                            }
                                            tableDeviceBlockID.append(table);
                                        }
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

    tableDeviceBlockID = document.getElementById(tableDeviceBlockID);
    if(!tableDeviceBlockID)
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
