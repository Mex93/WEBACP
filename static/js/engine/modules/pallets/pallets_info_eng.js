


// Просмотр инфы о паллетах

import {getTimestampInSeconds} from "../../common.js";

const PALLETS_INFO_BLOCK_TEXT_ID = 'pallets_info_block';
const PALLETS_BUTTOMS_BLOCK_TEXT_ID = 'buttoms';
const PALLETS_ERROR_BLOCK_TEXT_ID = 'errors';
let palletSQLID = null;
let palletName = null;
let isSuccessFind = false;
let antiFlood = 0;
let query = false;

function createTableDeviceHeader()
{
    let table = document.createElement('table');
    table.className = 'custom-table table-palletesn';
    let tr = document.createElement('tr');
    let th = document.createElement('th');
    th.innerText = 'Номер устройства в БД:'
    tr.append(th)
    th = document.createElement('th');
    th.innerText = 'Серийный номер устройства:'
    tr.append(th)
    th = document.createElement('th');
    th.innerText = 'Дата сканировки:'
    tr.append(th)
    table.append(tr)
    return table;
}
function createTableDeviceBody(table, deviceUnit)
{
    let deviceSN = deviceUnit.getDeviceSN();
    let scannedDate = deviceUnit.getScannedDate();
    let deviceAssy = deviceUnit.getAssy();

    let tr = document.createElement('tr');
    tr.id = `device_field_${deviceAssy}`
    let th = document.createElement('td');
    th.innerText = deviceAssy;
    tr.append(th)
    th = document.createElement('td');
    th.innerText = deviceSN;
    tr.append(th)
    th = document.createElement('td');
    th.innerText = scannedDate;
    tr.append(th)
    table.append(tr)
}



function onUserFindPallet(inputID)
{
    let fieldValue = inputID.value;
    if(typeof fieldValue  === 'string')
    {
        if(fieldValue.length < 4 || fieldValue.length > 25)
        {
            inputID.value = ""
            new CError('Вы ошиблись во вводе!', 2000);
            return
        }
        if(!isStringDataValid(fieldValue))
        {
            inputID.value = ""
            new CError('Вы ошиблись во вводе!', 2000);
            return
        }

        let formattedPalletCode = fieldValue.trim().toUpperCase();

        if(palletName === formattedPalletCode)
        {
            new CError("Вы уже запросили этот паллет!", 3000);
            return;
        }
        if(query)
        {
            new CError("Запрос ещё не вернулся!!!", 3000);
            return
        }
        if(antiFlood > getTimestampInSeconds())
        {
            new CError("Не флуди запросами!!!", 3000);
            return
        }
        antiFlood = getTimestampInSeconds() + 1;

        let completed_json = JSON.stringify({

            csn_device: formattedPalletCode
        }); //$.parseJSON(json_text);


        $.ajax({
            data : completed_json,
            dataType: 'json',
            type : 'POST',
            url : './pallet_find_info_data_ajax',
            contentType: "application/json",
            success: function(data) {
                palletName = "";
                query = false;

                let blockID = document.getElementById(PALLETS_INFO_BLOCK_TEXT_ID);
                if(blockID === null)
                    return;
                blockID.innerHTML = "";
                let tableDeviceBlockID = document.createElement('div');
                blockID.append(tableDeviceBlockID)

                CPalletInfo.clearUnits();
                CDevice.clearUnits();

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
                                table.append(tr)

                                let pUnits = CPalletInfo.getUnits();
                                count = 0;
                                let arrHTMLID = [];
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

                                    table.append(tr);
                                    count++;
                                })
                                let devicesCount = 0;
                                if(count)
                                {
                                    blockID.append(table);
                                    // NOTE! Событие должно быть тут, так как раньше не приаттачится

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
                                                new CError("Не могу обработать параметры устройства!", 2000);
                                                break;
                                            }
                                        }
                                        if(count)
                                        {
                                            devicesCount = count;
                                            table = createTableDeviceHeader();
                                            if(table)
                                            {
                                                let units = CDevice.getUnits();
                                                //console.log(units)
                                                for(let device of units)
                                                {
                                                    createTableDeviceBody(table, device);
                                                }
                                            }
                                        }
                                    }
                                }

                                let div = document.createElement("div")

                                let title = document.createElement('h1');
                                title.innerText = 'Паллет найден!';
                                div.append(title);

                                let textCount = document.createElement('h2');
                                textCount.innerText = `Количество TV: ${devicesCount} штук`;
                                div.append(textCount);

                                let textModelName = document.createElement('h2');
                                textModelName.innerText = `Модель: '${data.pallet_device_model_name}' ID: ${data.pallet_device_fk}`;
                                div.append(textModelName);

                                let textPalletName = document.createElement('h3');
                                textPalletName.innerText = `Паллет: '${data.pallet_number}'`;
                                div.append(textPalletName);

                                if(count)
                                {
                                    tableDeviceBlockID.append(div);
                                    tableDeviceBlockID.append(table);
                                }

                                else
                                    blockID.append(tableDeviceBlockID);

                            }
                            else
                            {
                                new CError("Не могу обработать параметры паллета!", 2000);
                            }
                        }
                        else
                            new CError("Ошибка получения данных!", 2000);
                    }
                    else
                        new CError("Ошибка получения данных паллета!", 2000);
                }
                else
                    new CError(data.error_text, 3000);
            },
            error: function(error) {
                location.reload();
            }
        })



    }
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
class CError
{
    constructor(errorText, time) {
        let errorBlock = document.getElementById(PALLETS_ERROR_BLOCK_TEXT_ID)
        errorBlock.innerText = errorText;
        setTimeout(end, time, errorBlock,)

        function end(blockID)
        {
            blockID.innerHTML = ''
        }
    }
}

function isStringDataValid(input)
{
    const regex = /^[A-Za-z0-9]+$/;
    return regex.test(input);
}
// ----------------------------------------------------------------- FUNC END

$(document).ready(function()
{

    let buttomsBlockID = document.getElementById(PALLETS_BUTTOMS_BLOCK_TEXT_ID);
    if(buttomsBlockID !== null)
    {
        let div_btms = document.createElement('div');
        div_btms.className = 'block_buttoms'

        let input = document.createElement('input');
        input.placeholder = 'Введите Номер паллета или телевизора:'
        input.className = 'input_pallet'
        div_btms.append(input)

        let btn_find = document.createElement('button');
        btn_find.onclick = function (ev)
        {
            onUserFindPallet(input);
        };
        btn_find.textContent = 'Найти паллет';
        btn_find.className = 'btm_submit-common'
        div_btms.append(btn_find)

        buttomsBlockID.append(div_btms)
    }


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
