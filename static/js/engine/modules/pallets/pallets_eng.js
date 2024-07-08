
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
let palletUnit = null;



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
    #palletNumber = null;
    #deviceAssyID = null;
    #modelFK = null;
    #scannedDate = null;
    constructor(cSN, palletNumber, deviceAssyID)
    {
        this.#deviceNumber = cSN;
        this.#palletNumber = palletNumber;
        this.#deviceAssyID = deviceAssyID;
    }
    // setters
    setScannedDate = (cValue) => this.#scannedDate = cValue;
    setModelFK = (cValue) => this.#modelFK = cValue;

    // getters
    getScannedDate = () => this.#scannedDate;
    getModelFK = () => this.#modelFK;

}

class CPallet
{
    #snNumber = null;
    #assembledLine = null;
    #completedStatus = null;
    #completedDate = null;
    #createdDate = null;
    #assyID = null;
    #devicesUnits;
    constructor(palletNumber, assyID)
    {
        this.#snNumber = palletNumber;
        this.#assyID = assyID;
        this.#devicesUnits = new Set();
    }
    // SETTERS
    setLine = (cValue) => this.#assembledLine = cValue;
    setCompletedStatus = (cValue) => this.#completedStatus = cValue;
    setCompletedDate = (cValue) => this.#completedDate = cValue;
    setCreatedDate = (cValue) => this.#createdDate = cValue;
    setAssy = (cValue) => this.#assyID = cValue;

    addDevice(aUnit)
    {
        if(aUnit instanceof CDevice)
        {
            this.#devicesUnits.add(aUnit);
            return true;
        }
    }
    getDevicesList()
    {
        return this.#devicesUnits.values();
    }
    clearDevicesList = () => this.#devicesUnits.clear();

    // GETTERS
    getLine = () => this.#assembledLine;
    getCompletedStatus = () => this.#completedStatus;
    getCompletedDate = () => this.#completedDate;
    getCreatedDate = () => this.#createdDate;
    getAssy = () => this.#assyID;
}


function destroyTableBlock()
{

}

function onUserPressedOnBTN(btnType)
{

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
                if(data.pallet_data instanceof Object)
                {
                    let {   assembled_line:line,
                            assy_id:assyID,
                            completed_check:complCheck,
                            completed_date:complDate,
                            create_date:createDate,
                            pallet_sn:palletSN
                        }
                        = data.pallet_data;
                    if(assyID && palletSN)
                    {
                        if(Boolean(complCheck))
                        {
                            palletUnit = new CPallet(palletSN);
                            palletUnit.setCompletedDate(complDate);
                            palletUnit.setLine(line);
                            palletUnit.setCompletedStatus(complCheck);
                            palletUnit.setCreatedDate(createDate);
                            palletUnit.setAssy(assyID);

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
                                        let unit = new CDevice(deviceSN, palletSN, assyID);
                                        unit.setScannedDate(scannedDate);
                                        unit.setModelFK(modelFK);
                                        palletUnit.addDevice(unit);
                                        count++;
                                    }
                                    else
                                    {
                                        cmessBoxMain.sendErrorMessage("Не могу обработать параметры устройства!");
                                        break;
                                    }
                                }
                                if(count)
                                {
                                    console.log(palletUnit)
                                    console.log(palletUnit.getDevicesList())
                                }
                            }
                        }
                        else
                           cmessBoxMain.sendErrorMessage("Ошибка получения статуса паллета!");
                    }
                    else
                        cmessBoxMain.sendErrorMessage("Ошибка получения данных паллета!");
                }
                else
                    cmessBoxMain.sendErrorMessage("Возникла ошибка формирования паллета!!!");
            }
            else
            {
                cmessBoxMain.sendErrorMessage(data.error_text);
            }


            // if(data.result === true)  // загрузка ASR
            // {
            //     if (Array.isArray(data.arr))
            //     {
            //         console.log(data.arr)
            //         let count = 0;
            //         for(let item of data.arr)
            //         {
            //             console.log(item)
            //             let textID = item.text_id;
            //             let textName = item.text_name;
            //             let isEditable = item.is_editable;
            //             let currentValue = item.current_value;
            //             let valueType = item.value_type;
            //
            //             let parameter = new CParameters();
            //             parameter.setTextID(textID);
            //             parameter.setTextName(textName);
            //             parameter.setIsEdit(isEditable);
            //             parameter.setVarType(valueType);
            //             parameter.setCurrentValue(currentValue);
            //
            //             if(!parameter.isValid())
            //             {
            //                 parameter.removeUnit();
            //                 continue
            //             }
            //
            //             count++;
            //         }
            //         if(count)
            //         {
            //             // isEdit = false;
            //             // isFindSuccess = true;
            //             // SuccessFindSN = snNumber;
            //             // CreateTable(TABLE_TYPE.TYPE_STANDART);
            //             HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.RESULT_BLOCK, true);
            //             cButton.switchBTNStatus(TABLE_TYPE.TYPE_STANDART);
            //         }
            //     }
            // }
            // else
            // {
            //     cmessBoxMain.sendErrorMessage(data.error_text);
            // }
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
