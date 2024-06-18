
import {CMessBox} from "/static/js/engine/CMessBox.js"


let query = false;

let acessDelete = false;
let accessEdit = false;
let accessCreate = false;
let cEditTableID = undefined;
let modelLabelID = undefined;
let editModelUnitID = undefined;
let cmessBoxMainBlock = new CMessBox("error_box")
let cmessBoxEditBlock = new CMessBox("error_box_edit")

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
    removeModel()
    {
        this.constructor.itemsList = this.constructor.itemsList.filter((unitID) =>
            unitID !== this);

        delete this
    }
    static getArrIndexInItems(unitID)
    {
        for(let i of this.itemsList.length)
        {
            if(this.itemsList[i] !== unitID)continue;
            return i;
        }
    }

    static getItemsCount = () => this.itemsList.length;
    static getItemsList = () => this.itemsList;
}





function onUserPressedMainMenuBtnEdit(mmUnit)
{
    // console.log("Нажата клавиша Редактировать")
    // console.log(mmUnit.getModelName())

    if(query)
        return false;

    if(cEditTableID)
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
                    cmessBoxMainBlock.sendErrorMessage(data.error_text);
                }
                else
                {
                    if(Array.isArray(data.arr))
                    {
                        if(cEditTableID)
                        {
                            destroyEditBlock();
                        }

                        console.log(data.arr)

                        let count = 0;
                        CItemParams.clearUnits();
                        editModelUnitID = mmUnit;
                        let elementsCBArr = [];
                        let elementsInputArr = [];
                        data.arr.forEach( (element, index) => {
                          console.log(element, index)

                            if(index === 0)
                            {
                                let table = document.createElement('table');
                                table.id = 'edit_table';
                                table.className = 'custom-table table-templates';
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

                            let [text_id, field_id, text_name, cvalue, cstate] = element
                            let fieldUnit = new CItemParams(element);
                            count ++;
                            let checkedStatus = String();
                            if(cstate)checkedStatus = 'checked';
                            else checkedStatus = '';

                            if(cvalue === null)
                            {
                                cvalue = ''  // что бы отключить None
                            }
                            elementsCBArr.push([`input_checkbox_${text_id}`, fieldUnit]);
                            elementsInputArr.push([`input_field_${text_id}`, fieldUnit]);

                            let str = `<tr>
                                        <td>${text_name}</td>
                                        <td>
                                        <input id="input_checkbox_${text_id}" type="checkbox" ${checkedStatus}></td>
                                        <td id="old_value_${text_id}">${cvalue}</td>
                                        <td>
                                        <input value="${cvalue}" id="input_field_${text_id}" type="text" maxlength="64" size="40"></td>
                                       </tr>`
                            let createElement = document.createElement("tr");
                            createElement.innerHTML = str;
                            cEditTableID.append(createElement);

                        })

                        if(count > 0)
                        {
                            modelLabelID.innerText = `Редактирование шаблона ${modelName}`;
                            let AttachBlockID = HTMLBlocks.getHTMLID(HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK);
                            AttachBlockID.append(cEditTableID);


                            // state elements
                            elementsCBArr.forEach( (element) => {
                                let htmlID = element[0];
                                let unitID = element[1];
                                let elementID = document.getElementById(htmlID);
                                if(elementID !== null)
                                {
                                    elementID.addEventListener("click", function (element) {
                                        Edit_onUserClickCB(elementID, unitID);
                                    })
                                }
                            })
                            // cvalue element
                            elementsInputArr.forEach( (element) => {
                                let htmlID = element[0];
                                let unitID = element[1];
                                let elementID = document.getElementById(htmlID);
                                if(elementID !== null)
                                {
                                    elementID.addEventListener("change", function (element) {
                                        Edit_onUserEditField(elementID, unitID);
                                    })
                                }
                            })



                            HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_RESULT_LIST, false);
                            HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK, true);
                        }
                    }
                }
                return true;
            }
            else
            {
                cmessBoxMainBlock.sendErrorMessage(data.error_text);
                return false
            }
        },
        error: function(error) {
            // responseProcess = false
            cmessBoxMainBlock.sendErrorMessage("Ошибка AJAX на стороне сервера!");
            return false
        }
    })


    return false;
}

function Edit_onUserEditField(elementHTMLID, elementUnitID)
{
    console.log(elementHTMLID.value)
    console.log(`${elementUnitID.getTextID()}`)

    let currentValue = elementHTMLID.value;
    if(currentValue === '')
        currentValue = null;
    elementUnitID.setCurrentValue(currentValue);

}
function Edit_onUserClickCB(elementHTMLID, elementUnitID)
{
    console.log(elementHTMLID.checked)
    console.log(`${elementUnitID.getTextID()}`)

    let currentStateChecked = elementHTMLID.checked;
    elementUnitID.setCurrentState(currentStateChecked);

}

function onUserPressedSaveTemplateBtn()
{
    console.log("Сохранить шаблон")

    if(cEditTableID)
    {
        if(query)
            return false;


        let units = CItemParams.getUnitsArr();
        let PA = [];  // массив с разницей в той же последовательности как и в конструкторе CItemParams
        let PA_Units = [];  // unit для обработки что бы в бэк не уходило
        let countPA = 0;
        for(let unit of units)
        {
            let currentValue = unit.getCurrentValue();
            let firstValue = unit.getFirstValue();

            let currentState = unit.getCurrentState();
            let firstState = unit.getFirstState();
            let isUsed = false;
            // value
            if(currentValue !== firstValue)
            {
                if(currentValue === '')
                    currentValue = null;  // нужно потому как в базе пустые значения это None, с бэка тоже приходят как None
                PA.push([unit.getTextName(), unit.getTextID(), unit.getFieldID(), "value", firstValue, currentValue]);
                countPA++;
                PA_Units.push(unit);
            }
            // checked
            if(currentState !== firstState)
            {
                PA.push([unit.getTextName(), unit.getTextID(), unit.getFieldID(), "state", firstState, currentState]);
                countPA++;
                PA_Units.push(unit);
            }

        }
        if(countPA > 0)  // если что то изменилось в филдах
        {
            console.log(PA);
            query = true;

            let scanFK = editModelUnitID.getScanFK();
            let modelID = editModelUnitID.getModelID();
            let modelName = editModelUnitID.getModelName();

            let completed_json = JSON.stringify({
                pa_array: PA,
                scan_fk: scanFK,
                model_id_fk: modelID,
                model_name: modelName
            }); //$.parseJSON(json_text);

            $.ajax({
                data : completed_json,
                dataType: 'json',
                type : 'POST',
                url : './templates_saved_edit_model_ajax',
                contentType: "application/json",
                success: function(data)
                {
                    query = false;
                    let result = data.result;
                    if(result === true)
                    {
                        cmessBoxEditBlock.sendSuccessMessage(data.error_text);

                        PA.forEach( (element, index) => {
                            let unitID = PA_Units[index];
                            let textID = unitID.getTextID();
                            if (element[3] === 'value')
                            {
                                let currentValue = unitID.getCurrentValue();
                                let firstValue = unitID.getFirstValue();
                                if (currentValue !== firstValue)  // на всякий
                                {
                                    let html_text = `old_value_${textID}`;

                                    let elementID = document.getElementById(html_text);
                                    if (elementID !== null)
                                    {
                                        elementID.innerText = currentValue;
                                    }

                                    html_text = `input_field_${textID}`;
                                    elementID = document.getElementById(html_text);
                                    if (elementID !== null)
                                    {
                                        elementID.innerText = currentValue;
                                    }
                                    unitID.setFirstValue(currentValue)
                                }
                            }
                            else if (element[3] === 'state')
                            {
                                let currentState = unitID.getCurrentState();
                                let firstState = unitID.getFirstState();

                                if (currentState !== firstState)
                                {
                                    let html_text = `input_checkbox_${textID}`;
                                    let elementID = document.getElementById(html_text);
                                    if (elementID !== null)
                                    {
                                        elementID.checked = currentState;
                                    }
                                    unitID.setFirstState(currentState)
                                }
                            }
                        });
                    }
                    else
                    {
                        cmessBoxEditBlock.sendErrorMessage(data.error_text);

                        PA.forEach( (element, index) =>
                        {
                            let unitID = PA_Units[index];
                            let textID = unitID.getTextID();
                            if(element[3] === 'value')
                            {
                                let currentValue = unitID.getCurrentValue();
                                let firstValue = unitID.getFirstValue();
                                if(currentValue !== firstValue)  // на всякий
                                {
                                    let html_text = `input_field_${textID}`;
                                    let elementID = document.getElementById(html_text);
                                    if(elementID !== null)
                                    {
                                        elementID.value = firstValue;
                                    }
                                    unitID.setCurrentValue(firstValue)
                                }
                            }
                            else  if(element[3] === 'state')
                            {
                                let currentState = unitID.getCurrentState();
                                let firstState = unitID.getFirstState();

                                if(currentState !== firstState)
                                {
                                    let html_text = `input_checkbox_${textID}`;
                                    let elementID = document.getElementById(html_text);
                                    if(elementID !== null)
                                    {
                                        elementID.checked = firstState;
                                    }
                                    unitID.setCurrentState(firstState)
                                }
                            }
                        });
                    }
                    return false;
                },
                error: function(error) {
                    // responseProcess = false
                    cmessBoxEditBlock.sendErrorMessage("Ошибка AJAX на стороне сервера!");
                    return false
                }
            })
        }
        else
        {
            cmessBoxEditBlock.sendErrorMessage("Вы ничего не изменили!");
        }
    }





    return false;
}
function onUserPressedCancelEditTemplateBtn()
{
    console.log("Нажата клавиша отменить редактирование")
    destroyEditBlock();

    return false;
}
function destroyEditBlock()
{
    if(cEditTableID)
    {
        editModelUnitID = undefined;
        cEditTableID.remove()
        cEditTableID = undefined;
        CItemParams.clearUnits();
        HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK, false);
    }
}


function onUserPressedMainMenuBtnDel(mmUnit)
{
    console.log("Нажата клавиша удалить")

    if(query)
        return false;

    if(cEditTableID)
    {
        alert('Сперва завершите редактирование шаблона!')
        return
    }

    let modelName = mmUnit.getModelName();
    let modelTypeName = mmUnit.getModelTypeName();
    if (confirm(`"Вы действительно хотите удалить выбранный шаблон '${modelTypeName}' '${modelName}' ?
            \nОтменить действие будет невозможно!"`)) // yes
    {

        query = true;

        let scanFK = mmUnit.getScanFK();
        let modelID = mmUnit.getModelID();
        console.log(scanFK, modelID)
        let completed_json = JSON.stringify({
            scan_fk: scanFK,
            model_id: modelID,
            model_name: modelName
        }); //$.parseJSON(json_text);

        $.ajax({
            data : completed_json,
            dataType: 'json',
            type : 'POST',
            url : './templates_delete_model_ajax',
            contentType: "application/json",
            success: function(data) {
                query = false;

                if(data.result === true)
                {
                    cmessBoxMainBlock.sendSuccessMessage(data.error_text);
                    if(cEditTableID)
                    {
                        // на всякий
                        destroyEditBlock();
                    }
                    mmUnit.removeModel()

                    if(TVModelsList.getItemsCount() === 0)
                    {
                        location.reload()
                        return;
                    }

                    let element = document.getElementById(`table_models_field_${modelID}`);
                    if(element !== null)
                    {
                        element.remove();
                    }
                }
                else
                {
                    cmessBoxMainBlock.sendErrorMessage(data.error_text);
                    return false
                }
            },
            error: function(error) {
                // responseProcess = false
                cmessBoxMainBlock.sendErrorMessage("Ошибка AJAX на стороне сервера!");
                return false
            }
        })
    }
    else {

    }



    return false;
}

function onUserPressedCreateTemplateBtn()
{
    if(accessCreate)
    {

    }
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
                    cmessBoxMainBlock.sendErrorMessage(data.error_text);
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
                                createElement.id = `table_models_field_${modelID}`;
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
                cmessBoxMainBlock.sendErrorMessage(data.error_text);
                return false
            }
        },
        error: function(error) {
            // responseProcess = false
            cmessBoxMainBlock.sendErrorMessage("Ошибка AJAX на стороне сервера!");
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
    textID = undefined;
    currentStateChange = undefined;
    firstStateChange = undefined;
    firstValue = undefined;
    currentValue = undefined;
    fieldID = undefined;
    static units = [];

    //[text_id, field_id, text_name, cvalue, cstate] = element
    constructor([ text_id, field_id, text_name, cvalue, cstate ])
    {
        if(text_name)
        {
            this.fieldID = field_id;
            this.textName = text_name;
            this.textID = text_id;
            this.currentStateChange = cstate;
            this.currentValue = cvalue;
            this.firstValue = cvalue;
            this.firstStateChange = cstate;

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

    getCurrentState = () => this.currentStateChange;
    setCurrentState = (cValue) => this.currentStateChange = cValue;
    
    getFirstState = () => this.firstStateChange;
    setFirstState = (cValue) => this.firstStateChange = cValue;

    getFieldID = () => this.fieldID;

    getCurrentValue = () => this.currentValue;
    setCurrentValue = (cValue) => this.currentValue = cValue;
    
    getFirstValue = () => this.firstValue;
    setFirstValue = (cValue) => this.firstValue = cValue;
    static getUnitsArr = () => this.units;
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
    accessCreate = +document.getElementById("access_create").innerText


    let btnCreateTemplate = document.getElementById('btn_create');
    if(btnCreateTemplate !== null)
    {
        btnCreateTemplate.addEventListener("click", function (element) {
            onUserPressedCreateTemplateBtn();
        })
    }
    let btnSaveTemplate = document.getElementById('btn_save');
    if(btnSaveTemplate !== null)
    {
        btnSaveTemplate.addEventListener("click", function (element) {
            onUserPressedSaveTemplateBtn();
        })
    }
    let btnCancelTemplate = document.getElementById('btn_edit_template_cancel');
    if(btnCancelTemplate !== null)
    {
        btnCancelTemplate.addEventListener("click", function (element) {
            onUserPressedCancelEditTemplateBtn();
        })
    }

    modelLabelID = document.getElementById('model_name_field');

    if(
        !isValid(acessDelete) ||
        !isValid(accessEdit) ||
        !isValid(accessCreate) ||
        !btnSaveTemplate ||
        !btnCreateTemplate ||
        !modelLabelID ||
        !btnCancelTemplate)
    {
        alert("Ошибка!!!!")
        console.log(acessDelete)
        console.log(accessEdit)
        console.log(accessCreate)
        return
    }
    editModelUnitID = undefined;

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
