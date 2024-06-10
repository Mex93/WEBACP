
import {CMessBox} from "/static/js/engine/CMessBox.js"

let query = false;

let acessDelete = false;
let accessEdit = false;
let cEditTableID = undefined;
let cmessBox = new CMessBox("error_box")

class TVModelsList
{
    modelName = null;
    modelID = null;
    modelTypeName = null;
    lastUpdateTime = null;
    serialNumber = null;
    scanFK = null;

    static itemsList = [];

    constructor(obj)
    {
        if(obj.modelName && obj.modelID && obj.modelTypeName && obj.lastUpdateTime && obj.serialNumber && obj.scanFK)
        {
            this.modelName = obj.modelName;
            this.modelID = obj.modelID;
            this.modelTypeName = obj.modelTypeName;
            this.lastUpdateTime = obj.lastUpdateTime;
            this.serialNumber = obj.serialNumber;
            this.scanFK = obj.scanFK;

            this.constructor.itemsList.push(this);
        }
    }
    getModelName = () => this.modelName;
    getModelTypeName = () => this.modelTypeName;
    getModelID = () => this.modelID;
    getLastUpdateDateStamp = () => this.lastUpdateTime;
    getSN = () => this.serialNumber;
    getScanFK = () => this.scanFK;

    static getItemsList = () => this.itemsList;
}

function onUserPressedMainMenuBtnEdit(mmUnit)
{
    // console.log("Нажата клавиша Редактировать")
    // console.log(mmUnit.getModelName())

    if(query)
        return false;

    query = true;

    let scanFK = mmUnit.getScanFK();
    let modelID = mmUnit.getModelID();
    let modelName = mmUnit.getModelName();

    let completed_json = JSON.stringify({
        scan_fk: scanFK,
        model_id: modelID,
        model_name: modelName
    }); //$.parseJSON(json_text);

    $.ajax({
        data : completed_json,
        dataType: 'json',
        type : 'POST',
        url : './templates_edit_mask_ajax',
        contentType: "application/json",
        success: function(data) {
            query = false;

            if(data.result === true)
            {
                if(!data.arr)
                {
                    cmessBox.sendErrorMessage(data.error_text);
                }
                else
                {
                    if(Array.isArray(data.arr))
                    {
                        destroyEditBlock();
                        console.log(data.arr)

                        let count = 0;
                        CItemParams.clearUnits();
                        let tableID = undefined;
                        data.arr.forEach( (element, index) => {
                          console.log(element, index)

                            if(index === 0)
                            {
                                let table = document.createElement('table');
                                table.id = 'edit_table';
                                table.className = 'custom-table';
                                cEditTableID = table;

                                let tr = document.createElement('tr');
                                let th = document.createElement('th');
                                th.innerText = 'Параметр:'
                                tr.append(th)
                                th = document.createElement('th');
                                th.innerText = 'Используется:'
                                tr.append(th)
                                th = document.createElement('th');
                                th.innerText = 'Старое значение:'
                                tr.append(th)
                                th = document.createElement('th');
                                th.innerText = 'Новое значение:'
                                tr.append(th)
                                table.append(tr)
                            }
                            let [text_id, sql_name, text_name, field_type, cvalue, is_used] = element
                            new CItemParams(text_name, sql_name, text_id, field_type, cvalue, is_used);
                            count ++;

                            let str = `<tr>
                                        <td>${text_name}</td>
                                        <td>ff</td>
                                        <td>${cvalue}</td>
                                        <td>${cvalue}</td>
                                       </tr>`
                            let createElement = document.createElement("tr");
                            createElement.innerHTML = str;
                            cEditTableID.append(createElement);
                        })

                        if(count > 0)
                        {
                            let AttachBlockID = HTMLBlocks.getHTMLID(HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK);
                            AttachBlockID.append(cEditTableID)

                            HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_RESULT_LIST, false);
                            HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK, true);
                        }
                    }
                }
                return true;
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


    return false;
}
function destroyEditBlock()
{
    CItemParams.clearUnits();
}




function onUserPressedMainMenuBtnDel(mmUnit)
{
    console.log("Нажата клавиша удалить")
    console.log(mmUnit.getModelName())
    return false;
}

function onUserPressedCreateTemplateBtn()
{
    console.log("Нажата клавиша создать")
    return true;
}


function get_tv_list_ajax()
{
    if(query)
        return false;

    query = true;

    $.ajax({
        data : {},
        dataType: 'json',
        type : 'POST',
        url : './templates_get_models_list_ajax',
        contentType: "application/json",
        success: function(data) {
            query = false;

            if(data.result === true)
            {
                if(!data.arr)
                {
                    cmessBox.sendErrorMessage(data.error_text);
                }
                else
                {
                    if(Array.isArray(data.arr))
                    {
                        let count = 0;
                        let tableID = document.querySelector("#table_models_list:last-child")
                        if(tableID !== null)
                        {
                            let str = ""
                            for(let array of data.arr)
                            {
                                let modelName = array['model_name'];
                                let modelID = array['model_id'];
                                let modelTypeName = array['model_type_name'];
                                let lastUpdateTime = array['last_update_time'];
                                let serialNumber = array['serial_number'];
                                let scanFK = array['model_scan_fk'];
                                if(!modelName || !modelID || !modelTypeName || !lastUpdateTime || !serialNumber || !scanFK)
                                {
                                    continue;
                                }
                                let obj = {
                                    modelName,
                                    modelID,
                                    modelTypeName,
                                    lastUpdateTime,
                                    serialNumber,
                                    scanFK};

                               let unit = new TVModelsList(obj);


                                let btn_del = null;
                                let btn_edit = null;
                                let btn_del_str = null;
                                let btn_edit_str = null;
                                if(acessDelete)
                                    btn_del_str = `btn_del_unit_${modelID}`;
                                    btn_del = `<button id = "${btn_del_str}" type="submit" name = "delete" value = "delete" class = "btm_submit-common delete">Удалить</button>`
                                if(accessEdit)
                                    btn_edit_str = `btn_edit_unit_${modelID}`;
                                    btn_edit = `<button id = "${btn_edit_str}" type="submit" name = "edit" value = "edit" class = "btm_submit-common edit">Редактировать</button>`

                                str = `
                                        <td>${modelName}</td>
                                        <td>${modelTypeName}</td>
                                        <td>${lastUpdateTime}</td>
                                        <td><div class = 'inline_buttom'>${btn_edit} ${btn_del}</div></td>
                                       `;
                                let createElement = document.createElement("tr");
                                createElement.innerHTML = str;
                                tableID.append(createElement);

                                // Инициализация клавиш в главное меню списка моделей
                                if(btn_edit_str)
                                {
                                    btn_edit = document.getElementById(`${btn_edit_str}`);
                                    if(btn_edit !== null)
                                    {
                                        btn_edit.addEventListener("click", function (element) {
                                            onUserPressedMainMenuBtnEdit(unit);
                                        })
                                    }
                                }
                               if(btn_del_str)
                               {
                                   btn_del = document.getElementById(`${btn_del_str}`);
                                   if(btn_del !== null)
                                   {
                                       btn_del.addEventListener("click", function (element) {
                                           onUserPressedMainMenuBtnDel(unit);
                                       })
                                   }
                               }

                                count++;
                            }
                        }
                        if(count > 0)
                        {
                            HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_MODELS_LIST,false);
                            HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.MODELS_LIST,true);
                        }
                    }
                }
                return true;
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
    return true;
}



class HTMLBlocks
{
    static BLOCK_TYPE = {
        ANIM_MODELS_LIST: 0,
        ANIM_RESULT_LIST: 1,
        MODELS_LIST: 2,
        EDIT_BLOCK: 3
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
    static isValidNonUnit(blockType)
    {
        let unitID = this.getUnitIDFromBlockType(blockType);
        return unitID.htmlID !== null;
    }
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
    static getHTMLName(blockType)
    {
        let unitID = this.getUnitIDFromBlockType(blockType);
        if(unitID !== null)
        {
            return unitID.htmlName;
        }
    }
    static getHTMLID(blockType)
    {
        let unitID = this.getUnitIDFromBlockType(blockType);
        if(unitID !== null)
        {
            return unitID.htmlID;
        }
    }
    static isBlockShow(blockType)
    {
        let unitID = this.getUnitIDFromBlockType(blockType);
        if(unitID !== null)
        {
           return unitID.showStatus;
        }
    }
}


class CItemParams
{
    textName = undefined;
    sqlLabels = undefined;
    textID = undefined;
    checkType = undefined;
    currentValue = undefined;
    isUsed = undefined;
    static units = [];

    constructor(textName, sqlLabels, textID, checkType, cValue, isUsed)
    {
        if(textName && sqlLabels && textID)
        {
            this.textName = textName;
            this.sqlLabels = sqlLabels;
            this.textID = textID;
            this.checkType = checkType;
            this.currentValue = cValue;
            this.isUsed = isUsed;

            this.constructor.units.push(this);
        }
    }

    static getUnitIDFromTextID(textID)
    {
        for(let item of this.units)
        {
            if(item.textID !== textID)
                continue;
            return item
        }
    }
    getTextName = () => this.textName;
    getTextID = () => this.textID;
    getCheckType = () => this.checkType;
    getSQLLabel = () => this.sqlLabels;
    getCValue = () => this.currentValue;
    getUsedStatus = () => this.isUsed;
    static clearUnits = () =>
    {
        if(this.units.length > 0)
        {
            for(let item of this.units)
            {
                // delete item;
            }
        }
    }
}

// ----------------------------------------------------------------- FUNC END

$(document).ready(function()
{
    let units = [];
    units.push(new HTMLBlocks('seleketon_model_list',   HTMLBlocks.BLOCK_TYPE.ANIM_MODELS_LIST));
    units.push(new HTMLBlocks('skeleton_edit_block',    HTMLBlocks.BLOCK_TYPE.ANIM_RESULT_LIST));
    units.push(new HTMLBlocks('block_edit',             HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK));
    units.push(new HTMLBlocks('res_model_list_block',   HTMLBlocks.BLOCK_TYPE.MODELS_LIST));

    for(let item of units)
    {
        if(!item.isValidWithUnit())
        {
            alert("Ошибка!!!!")
            return;
        }
    }

    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_MODELS_LIST, true);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.MODELS_LIST, false);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK, false);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_RESULT_LIST, false);
    let isValid = (numb) => (numb === 0 || numb === 1)


    acessDelete = +document.getElementById("access_del").innerText
    accessEdit = +document.getElementById("access_edit").innerText


    let btnCreateTemplate = document.getElementById('btn_create');
    if(btnCreateTemplate !== null)
    {
        btnCreateTemplate.addEventListener("click", function (element) {
            onUserPressedCreateTemplateBtn();
        })
    }

    if(!isValid(acessDelete) || !isValid(accessEdit) || !btnCreateTemplate)
    {
        alert("Ошибка!!!!")
        console.log(acessDelete)
        console.log(accessEdit)
        return
    }


    setTimeout(get_tv_list_ajax, 3000);


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
