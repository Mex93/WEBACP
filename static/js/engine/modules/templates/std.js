
// Морда для создания и редактирования модели устройства сканировки
// Удаление, создание и редактирование
// Рязанов НВ 26.06.2024
// ООО КВАНТ
// ЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫ


import {CMessBox} from "/static/js/engine/CMessBox.js"


let query = false;

let accessDelete = false;
let accessEdit = false;
let accessCreate = false;
let accessFind = false;
let cEditTableID = undefined;
let isEditTemplate = undefined;
let modelLabelID = undefined;
let editModelUnitID = undefined;
let isCreateTemplate = false;
let cmessBoxMainBlock = new CMessBox("error_box")
let cmessBoxEditBlock = new CMessBox("error_box_edit")
let cmessBoxCreateBlock = new CMessBox("error_box_create")


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
        if(obj.modelName && obj.modelID && obj.modelTypeName && obj.scanFK)
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
    getScanFK = () => this.scanFK;
    removeModel()
    {
        this.constructor.itemsList = this.constructor.itemsList.filter((unitID) =>
            unitID !== this);

        delete this
    }
    // static getArrIndexInItems(unitID)
    // {
    //     for(let i of this.itemsList.length)
    //     {
    //         if(this.itemsList[i] !== unitID)continue;
    //         return i;
    //     }
    // }

    static getItemsCount = () => this.itemsList.length;
    //static getItemsList = () => this.itemsList;
}


function onUserPressedMainMenuBtnEdit(mmUnit)
{
    // console.log("Нажата клавиша Редактировать")
    // console.log(mmUnit.getModelName())
    if(!accessEdit && !accessFind)
    {
        return
    }
    if(query)
        return false;
    if(isCreateTemplate)
    {
        alert('Сперва завершите создание модели!')
        return
    }
    if(isEditTemplate)
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
                if(Array.isArray(data.arr))
                {

                    //console.log(data.arr)

                    let count = 0;
                    CItemParams.clearUnits();
                    editModelUnitID = mmUnit;
                    let elementsCBArr = [];
                    let elementsInputArr = [];
                    data.arr.forEach( (element, index) => {
                      //console.log(element, index)

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
                            if(accessEdit)
                            {
                                th = document.createElement('th');
                                th.innerText = 'Старое значение:'
                                tr.append(th)
                            }
                           else if(accessFind)
                            {
                                th = document.createElement('th');
                                th.innerText = 'Текущее значение:'
                                tr.append(th)
                            }
                            if(accessEdit)
                            {
                                th = document.createElement('th');
                                th.innerText = 'Новое значение:'
                                tr.append(th)
                            }

                            table.append(tr)
                        }

                        let [text_id, , text_name, cvalue, cstate, req_once] = element
                        let fieldUnit = new CItemParams(element);
                        count ++;
                        let checkedStatus = String();
                        let lockedState;
                        let lockedValue = '';

                        if(cstate !== null)
                        {
                            if(cstate)checkedStatus = 'checked';
                            else checkedStatus = '';
                            lockedState = ''
                        }
                        else
                        {
                            lockedState = 'disabled';
                        }

                        if(cvalue === '')
                        {
                            cvalue = ''  // что бы отключить None
                            lockedValue = '';
                        }
                        else if(cvalue === null)
                        {
                            cvalue = ''  // что бы отключить None
                            lockedValue = 'disabled';
                        }

                        if(req_once === true)
                            req_once = 'required placeholder = ""'
                        else req_once = ''

                        if(accessEdit)
                        {
                            elementsCBArr.push([`input_checkbox_${text_id}`, fieldUnit]);
                            elementsInputArr.push([`input_field_${text_id}`, fieldUnit]);
                        }
                        if(!accessEdit)
                        {
                            lockedState = 'disabled';
                        }

                        if(text_id === 'model_fk')
                        {
                            lockedValue = 'disabled';
                            lockedState = 'disabled';
                        }


                        let rulesText = getHelpText(text_id);
                        let str = null;

                        if(accessEdit)
                        {
                            str = `<tr>
                                    <td data-tooltip="${rulesText}">${text_name} 
                                    <img src="static/icons/help_icon.svg" alt="Информация" width="25px" height="25px">
                                    </td>
                                    <td>
                                    <input name = 'field check' ${lockedState} id="input_checkbox_${text_id}" type="checkbox" ${checkedStatus}></td>
                                    <td ${lockedValue} id="old_value_${text_id}">${cvalue}</td>
                                    <td>
                                    <input name = 'field input' ${req_once} ${lockedValue} value="${cvalue}" id="input_field_${text_id}" type="text" maxlength="64" size="40"></td>
                                   </tr>`
                        }
                        else if(accessFind)
                        {
                            str = `<tr>
                                    <td data-tooltip="${rulesText}">${text_name} 
                                    <img src="static/icons/help_icon.svg" alt="Информация" width="25px" height="25px">
                                    </td>
                                    <td>
                                    <input name = 'field check' ${lockedState} id="input_checkbox_${text_id}" type="checkbox" ${checkedStatus}></td>
                                    <td ${lockedValue} id="old_value_${text_id}">${cvalue}</td>
                                   </tr>`
                        }

                        let createElement = document.createElement("tr");
                        createElement.innerHTML = str;
                        cEditTableID.append(createElement);

                    })

                    if(count > 0)
                    {
                        modelLabelID.innerText = `Редактирование модели ${modelName}`;
                        let AttachBlockID = HTMLBlocks.getHTMLID(HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK);
                        AttachBlockID.append(cEditTableID);

                        if(accessEdit)
                        {
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
                        }

                        isEditTemplate = true;

                        HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_RESULT_LIST, false);
                        HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK, true);

                        gotoToEditBlock();
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


function onUserPressedSaveTemplateBtn()
{
    console.log("Сохранить модель")

    if(!accessEdit)
    {
        return
    }
    if(isEditTemplate)
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


function onUserPressedMainMenuBtnDel(mmUnit)
{
    console.log("Нажата клавиша удалить")

    if(query)
        return false;

    if(!accessDelete)
    {
        return
    }
    if(isEditTemplate)
    {
        alert('Сперва завершите редактирование или просмотр модели!')
        return
    }
    if(isCreateTemplate)
    {
        alert('Сперва завершите создание новой модели!')
        return
    }


    let modelName = mmUnit.getModelName();
    let modelTypeName = mmUnit.getModelTypeName();
    if (confirm(`"Вы действительно хотите удалить выбранную модель '${modelTypeName}' '${modelName}' ?
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
                    if(isEditTemplate)
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



function get_tv_list_ajax()
{
    if(query)
        return false;

    if(!accessEdit && !accessCreate && !accessDelete && !accessFind)
    {
        return
    }

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

                                if(!modelName || !modelID || !modelTypeName || !scanFK)
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

                                let btn_del = '';
                                let btn_edit = '';
                                let btn_del_str = '';
                                let btn_edit_str = '';
                                let btn_string = '';
                                if(accessDelete)
                                {
                                    btn_del_str = `btn_del_unit_${modelID}`;
                                    btn_del = `<button id = "${btn_del_str}" type="submit" name = "delete" value = "delete" class = "btm_submit-common delete">Удалить</button>`
                                }

                                if(accessEdit)
                                {
                                    btn_edit_str = `btn_edit_unit_${modelID}`;
                                    btn_edit = `<button id = "${btn_edit_str}" type="submit" name = "edit" value = "edit" class = "btm_submit-common edit">Редактировать</button>`
                                }
                                else if(accessFind)
                                {
                                    btn_edit_str = `btn_edit_unit_${modelID}`;
                                    btn_edit = `<button id = "${btn_edit_str}" type="submit" name = "edit" value = "edit" class = "btm_submit-common edit">Просмотр</button>`
                                }

                                if(accessDelete || accessEdit)
                                {
                                    btn_string = `<td>
                                                <div class = 'inline_buttom'>
                                                ${btn_edit} ${btn_del}
                                                </div>
                                                </td>`;
                                }
                                else
                                {
                                    btn_string = `<td>
                                                <div class = 'inline_buttom'>
                                                Нет доступа!
                                                </div>
                                                </td>`;
                                }


                                str = `
                                        <td>${modelName}</td>
                                        <td>${modelTypeName}</td>
                                        <td>${lastUpdateTime}</td>
                                        ${btn_string}
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
                            if(!accessDelete && !accessEdit)
                            {
                                let element = document.getElementById('deleted_models_buttons');
                                if(element !== null)
                                {
                                    // удаление таблички с кнопками если прав нет полностью
                                    element.remove();
                                }
                            }

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
        ANIM_CREATE_BLOCK: 2,
        MODELS_LIST: 3,
        EDIT_BLOCK: 4,
        CREATE_BLOCK: 5
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

    // static getUnitIDFromTextID(textID)
    // {
    //     for(let item of this.units)
    //     {
    //         if(item.textID !== textID)
    //             continue;
    //         return item
    //     }
    // }
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
            this.units = [];
        }
    }
}
function gotoToMainBlock()
{
    document.querySelector("#block_scross_main").scrollIntoView({
        behavior: 'smooth'
    });
}
function gotoToEditBlock()
{
    document.querySelector("#block_edit").scrollIntoView({
        behavior: 'smooth'
    });
}
function gotoToCreateBlock()
{
    document.querySelector("#block_create").scrollIntoView({
        behavior: 'smooth'
    });
}

//////////////////////////////////////
function onUserPressedCancelEditTemplateBtn()
{
    console.log("Нажата клавиша отменить редактирование")
    if(isEditTemplate)
    {
        gotoToMainBlock();
        destroyEditBlock();
    }
    return false;
}


//////////////////////////////////////
function onUserPressedSaveCreateTemplateBtn()
{
    console.log("сохранить созданную модель")
    if(isEditTemplate)
    {
        return
    }
    if(isCreateTemplate)
    {
        if(accessCreate)
        {
            if(query)
                return false;

            let arr = CreatedTemplateMain.getUnitsArray();
            if(Array.isArray(arr))
            {
                let arrayForQuery = [];
                let countSuccess = 0;
                for(let unitArr of arr)
                {
                    let [mainUnit, unitOne, unitTwo] = unitArr;
                    let textName = mainUnit.getTextName();
                    let textID = mainUnit.getTextID();

                    let result = true;
                    let cState = null;
                    let cValue = null;
                    for(let unit of [unitOne, unitTwo])
                    {
                        if(unit !== null)
                        {
                            let fType = unit.getType();
                            let htmlID = unit.getHTMLId();
                            if(fType ==='state')
                            {
                                cState = htmlID.checked;
                            }
                            else if(fType ==='value')
                            {
                                cValue = String(htmlID.value);
                                if(/[а-яА-ЯЁё]/.test(cValue))
                                {
                                    htmlID.value = cValue + ' [Ошибка!]';
                                    result = false;
                                    break;
                                }
                                if(cValue.length >= 64)
                                {
                                    htmlID.value = cValue + ' [Ошибка!]';
                                    result = false;
                                    break;
                                }
                            }
                        }
                    }
                    if(result)
                    {
                        arrayForQuery.push([textID, textName, cState, cValue])
                        countSuccess++;
                    }
                }
                if(countSuccess)
                {
                    query = true;
                    let completed_json = JSON.stringify({
                        create_parameters: arrayForQuery,
                    }); //$.parseJSON(json_text);

                    $.ajax({
                        data : completed_json,
                        dataType: 'json',
                        type : 'POST',
                        url : './templates_create_mask_add_ajax',
                        contentType: "application/json",
                        success: function(data) {
                            query = false;

                            if(data.result === true)
                            {
                                if(Array.isArray(data.arr_result))
                                {
                                    arr = data.arr_result;
                                    console.log(`Созданы индексы: ${arr}`)
                                }
                                cmessBoxMainBlock.sendSuccessMessage(data.error_text);

                                destroyCreateBlock();
                                gotoToMainBlock();
                                setTimeout(function (){
                                    location.reload()
                                },
                                    2000)
                            }
                            else
                            {
                                cmessBoxCreateBlock.sendErrorMessage(data.error_text);
                                return false
                            }
                        },
                        error: function(error) {
                            // responseProcess = false
                            cmessBoxCreateBlock.sendErrorMessage("Ошибка AJAX на стороне сервера!");
                            return false
                        }
                    })

                }
            }
        }
    }

}
function destroyCreateBlock()
{
    if(isCreateTemplate)
    {
        if(cEditTableID)
        {
            CreatedTemplateMain.destroyUnits();
            isCreateTemplate = false;
            cEditTableID.remove();
            cEditTableID = undefined;
        }
        HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.CREATE_BLOCK, false);
    }
}
function onUserPressedCancelCreateTemplateBtn()
{
    console.log("отменить созданный модель")
    if(isCreateTemplate)
    {
        gotoToMainBlock();
        destroyCreateBlock()
    }
}
class CreatedTemplateMain  // класс для создания шаблона
{
    textName = null;
    textID = null;
    static units = [];

    constructor(unitOne, unitTwo)
    {
       this.constructor.units.push([this, unitOne, unitTwo])
    }

    setTextName = (textName) => this.textName = textName;
    setTextID = (textID) => this.textID = textID;

    getTextName = () => this.textName;
    getTextID = () => this.textID;

    static getUnitsArray = () => this.units;
    static destroyUnits = () =>
    {
        this.units = [];
    }
}
class CreatedTemplateUnit  // класс для создания шаблона
{
    htmlElementID = null;
    elementType = null;

    constructor(eType)
    {
        this.elementType = eType;
    }
    setHTMLId = (htmlID) => this.htmlElementID = htmlID;
    getHTMLId = () => this.htmlElementID;

    getType = () => this.elementType;
}
function onUserPressedCreateTemplateBtn()
{
    console.log("Нажата клавиша создать")

    if(isEditTemplate)
    {
        alert('Сперва завершите редактирование или просмотр модели!')
        return
    }

    if(accessCreate)
    {
        if(!isCreateTemplate)
        {
            if(query)
                return false;
            query = true;
            HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_CREATE_BLOCK, true);
            HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.CREATE_BLOCK, true);
            $.ajax({
                data : {},
                dataType: 'json',
                type : 'POST',
                url : './templates_create_mask_get_elemets_ajax',
                contentType: "application/json",
                success: function(data) {
                    query = false;
                    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_CREATE_BLOCK, false);


                    if(data.result === true)
                    {
                        if(Array.isArray(data.arr))
                        {
                            let tableID = undefined;
                            if(data.arr.length > 0)
                            {
                                let count = 0;
                                let table = undefined;
                                let idsInputFields = [];
                                data.arr.forEach( (element, index) =>
                                {
                                    // console.log(element, index)

                                    if(index === 0)
                                    {
                                        table = document.createElement('table');

                                        table.id = 'create_table';
                                        table.className = 'custom-table table-templates';
                                        tableID = table;

                                        let tr = document.createElement('tr');
                                        let th = document.createElement('th');
                                        th.innerText = 'Параметр:'
                                        tr.append(th)
                                        th = document.createElement('th');
                                        th.innerText = 'Используется:'
                                        tr.append(th)
                                        th = document.createElement('th');
                                        th.innerText = 'Значение:'
                                        tr.append(th)
                                        table.append(tr)


                                        let str = `<tr>
                                        <td data-tooltip="
                                        Название устройства должно быть уникальным и состоять из латинских букв и цифр, 
                                        в том числе возможные знаки разделения.\n
                                        Название должно начинаться с префикса TV, MNT и так далее, \n
                                        в зависимости от типа устройства. Например: 'TV TCL 32S65A', 'MNT IRBIS 24FILUS01MIR'">
                                        Название устройства 
                                        <img id="rules_device_name" src="static/icons/help_icon.svg" alt="Информация" width="25px" height="25px"> </td>
                                        <td>
                                        <input disabled type="checkbox"></td>
                                        <td>
                                        <input required value="" id="create_input_field_device_name" type="text" maxlength="64" size="40"></td>
                                       </tr>`
                                        let createElement = document.createElement("tr");
                                        createElement.innerHTML = str;
                                        table.append(createElement);

                                        idsInputFields.push([null, 'create_input_field_device_name', 'device_name', 'Название устройства']);
                                    }
                                    if(table !== undefined)
                                    {
                                        let [text_id, field_id, text_name, cvalue, cstate, req_once] = element

                                        if(text_id === 'model_fk')
                                            return false;

                                        if(cvalue === null)
                                        {
                                            cvalue = 'disabled'
                                        }
                                        if(cstate === null)
                                        {
                                            cstate = 'disabled'
                                        }

                                        if(req_once === true)
                                            req_once = 'required'
                                        else req_once = ''

                                        let rulesText = getHelpText(text_id);

                                        let str = `<tr>
                                        <td data-tooltip="${rulesText}"> ${text_name}
                                        <img src="static/icons/help_icon.svg" alt="Информация" width="25px" height="25px"></td>
                                        <td>
                                        <input ${cstate} id="create_input_checkbox_${text_id}" type="checkbox"></td>
                                        <td>
                                        <input ${req_once} ${cvalue} value="" id="create_input_field_${text_id}" type="text" maxlength="64" size="40"></td>
                                       </tr>`
                                        let createElement = document.createElement("tr");
                                        createElement.innerHTML = str;
                                        table.append(createElement);

                                        idsInputFields.push([
                                            cstate === 'disabled' ? null:`create_input_checkbox_${text_id}`,
                                            cvalue === 'disabled' ? null:`create_input_field_${text_id}`,
                                            text_id,
                                            text_name]);

                                        count++;
                                    }

                                });
                                if(count > 0)
                                {
                                    let AttachBlockID = HTMLBlocks.getHTMLID(HTMLBlocks.BLOCK_TYPE.CREATE_BLOCK);
                                    AttachBlockID.append(tableID);
                                    cEditTableID = tableID;

                                    isCreateTemplate = true;
                                    count = 0;

                                    for(let item of idsInputFields)
                                    {
                                        let [stateCheckHTML, inputFieldHTML, textID, textName] = item;
                                        let arrWithUnits = [];
                                        if(stateCheckHTML !== null)
                                        {
                                            let stateCheckHTMLID = document.getElementById(stateCheckHTML);
                                            if(stateCheckHTMLID == null)
                                            {
                                                console.log(`Внимание! Не найден HTML ID '${stateCheckHTML}'`)
                                                destroyCreateBlock();
                                                return false;
                                            }
                                            let unit = new CreatedTemplateUnit('state');
                                            unit.setHTMLId(stateCheckHTMLID);
                                            arrWithUnits.push(unit)
                                        }
                                        else arrWithUnits.push(null);

                                        if(inputFieldHTML !== null)
                                        {
                                            let inputFieldHTMLID = document.getElementById(inputFieldHTML);
                                            if(inputFieldHTMLID == null)
                                            {
                                                console.log(`Внимание! Не найден HTML ID '${inputFieldHTML}'`)
                                                destroyCreateBlock();
                                                return false;
                                            }
                                            let unit = new CreatedTemplateUnit('value');
                                            unit.setHTMLId(inputFieldHTMLID);
                                            arrWithUnits.push(unit)
                                        }
                                        else arrWithUnits.push(null);

                                        if(arrWithUnits.length === 0)
                                            continue;

                                        let mainUnit = new CreatedTemplateMain(...arrWithUnits);
                                        mainUnit.setTextName(textName);
                                        mainUnit.setTextID(textID);
                                        count ++;

                                    }
                                    if(!count)
                                    {
                                        console.log(`Внимание! Ошибка в построении таблицы параметров для создания модели!`)
                                        destroyCreateBlock();
                                        return false;
                                    }
                                    else
                                    {
                                        gotoToCreateBlock();
                                    }
                                }
                                else
                                {
                                    cmessBoxMainBlock.sendErrorMessage("Не могу составить таблицу параметров!");
                                }
                            }
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
                    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_CREATE_BLOCK, false);
                    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.CREATE_BLOCK, false);
                    return false
                }
            })
        }
    }
    return true;
}
function getHelpText(textID)
{
    let rulesText;
    switch(textID)
    {
        case 'device_name':
        {
            rulesText = "" +
                "Название устройства должно быть уникальным и состоять из латинских букв и цифр, в том числе возможные знаки разделения.\n\n" +
                "Название должно начинаться с префикса TV, MNT и так далее, в зависимости от типа устройства.\n" +
                "Например: 'TV TCL 32S65A', 'MNT IRBIS 24FILUS01MIR'";
            break;
        }
        case 'vendor_code':
        {
            rulesText = "" +
                "Код производителя должен быть уникален для каждой модели устройства. " +
                "Обычно код производителя можно получить из части названия устройства, например: 'IRBIS 24FILUS01MIR. ' -> '24FILUS01MIR'.\n" +
                "Код должен состоять из латинских букв и цифр, а так же знаков разделения.";
            break;
        }
        case 'device_sn':
        {
            rulesText = "" +
                "Серийный номер устройства может состоять из лазличных диапазонов значений, которые заявляет заказчик. " +
                "Например, может содержать дату производства, XYZ стекла, порядковый номер устройства и так далее. " +
                "Для составления правильного шаблона нужно руководствоваться правилом повторения символов в серийном номере. " +
                "Заменяйте знаком '*' все символы, которые не повторяются. " +
                "В шаблоне не должно быть кириллицы. Формат шаблона должен полностью повторять оригинал серийного номера конкретного компонента. " +
                "Количество символов должно быть одинаковым в шаблоне и серийном номере. " +
                "Оставляйте символы серийного номера, которые всегда остаются неизменны. " +
                "Пример: серийный номер устройства '2406BHQ213128F00001' -> вариант шаблона '24**BHQ213128F*****'.";
            break;
        }
        case 'platform_fk':
        {
            rulesText = "" +
                "Номер платформы указывается с помощью цифр, обычно он означает производителя, к которому принадлежит конкретная модель. " +
                "Например: TCL, IFFALCON: 1, MNT IRBIS: 6, и так далее. Для актуализации информации обратитесь к системному администратору. ";
            break;
        }
        case 'software_type':
        {
            rulesText = "" +
                "Тип программного обеспечания указывается цифрой порядкового номера ОС конкретной модели устройства. " +
                "Данный параметр важен и задействован в сканировочных программах. Например: для телевизоров на базе ОС 'OneWay': 2, Мониторы: 4, " +
                "Интерактивные панели: 5, TCL/IFFCALCON: 1 и так далее. ";
            break;
        }
        case 'model_fk':
        {
            rulesText = "" +
                "Это поле устанавливается автоматически и не требует редактирования.";
            break;
        }
        default:
        {
            rulesText = "" +
                "Для составления правильного шаблона нужно руководствоваться правилом повторения символов в серийном номере компонента или устройства. " +
                "Заменяйте знаком '*' все символы, которые не повторяются. " +
                "В шаблоне не должно быть кириллицы. Формат шаблона должен полностью повторять оригинал серийного номера конкретного компонента. " +
                "Количество символов должно быть одинаковым в шаблоне и серийном номере. " +
                "Оставляйте символы серийного номера, которые всегда остаются неизменны. " +
                "Пример: серийный номер стекла 'A24231531505060P1AM2H' -> вариант шаблона 'A********************'.";
            break;
        }
    }
    return rulesText;
}


//////////////////////////////////////
function Edit_onUserEditField(elementHTMLID, elementUnitID)
{
    if(!accessEdit)
        return
    // console.log(elementHTMLID.value)
    // console.log(`${elementUnitID.getTextID()}`)

    let currentValue = elementHTMLID.value;

    if(/[а-яА-ЯЁё]/.test(currentValue))
    {
        elementHTMLID.value = elementUnitID.getFirstValue();
        return;
    }

    elementUnitID.setCurrentValue(currentValue);

}
function Edit_onUserClickCB(elementHTMLID, elementUnitID)
{
    if(!accessEdit)
        return
    // console.log(elementHTMLID.checked)
    // console.log(`${elementUnitID.getTextID()}`)

    let currentStateChecked = elementHTMLID.checked;
    elementUnitID.setCurrentState(currentStateChecked);

}

function destroyEditBlock()
{
    if(isEditTemplate)
    {
        if(cEditTableID)
        {
            editModelUnitID = undefined;
            cEditTableID.remove()
            cEditTableID = undefined;
            isEditTemplate = false;
            CItemParams.clearUnits();
        }
        HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK, false);
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

    let btnCreateTemplate = document.getElementById('btn_create');
    if(btnCreateTemplate !== null)
    {
        btnCreateTemplate.addEventListener("click", function (element) {
            onUserPressedCreateTemplateBtn();
        })
    }

    accessCreate = document.getElementById("access_create");
    if(accessCreate)
    {
        accessCreate = +accessCreate.innerText;
        if(!isValid(accessCreate))
        {
            accessCreate = false;
        }
        if(accessCreate)
        {
            if(!btnCreateTemplate)
            {
                alert("Ошибка accessCreate!!!!")
                return
            }
        }
    }
    else
        accessCreate = false;

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

    if(!accessEdit && !accessCreate && !accessDelete && !accessFind)
    {
        alert("Ошибка доступа!!!!")
        return;
    }

    let units = [];
    units.push(new HTMLBlocks('seleketon_model_list',   HTMLBlocks.BLOCK_TYPE.ANIM_MODELS_LIST));
    units.push(new HTMLBlocks('skeleton_create_block',  HTMLBlocks.BLOCK_TYPE.ANIM_CREATE_BLOCK));
    units.push(new HTMLBlocks('skeleton_edit_block',    HTMLBlocks.BLOCK_TYPE.ANIM_RESULT_LIST));
    units.push(new HTMLBlocks('block_edit',             HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK));
    units.push(new HTMLBlocks('res_model_list_block',   HTMLBlocks.BLOCK_TYPE.MODELS_LIST));
    units.push(new HTMLBlocks('block_create',           HTMLBlocks.BLOCK_TYPE.CREATE_BLOCK));

    for(let item of units)
    {
        if(!item.isValidWithUnit())
        {
            alert("Ошибка!!!!")
            return;
        }
    }

    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_MODELS_LIST, true);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_CREATE_BLOCK, false);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.MODELS_LIST, false);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.EDIT_BLOCK, false);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.ANIM_RESULT_LIST, false);
    HTMLBlocks.showBlock(HTMLBlocks.BLOCK_TYPE.CREATE_BLOCK, false);


    let btnSaveTemplate = document.getElementById('btn_save_edit');
    if(btnSaveTemplate !== null)
    {
        btnSaveTemplate.addEventListener("click", function (element) {
            onUserPressedSaveTemplateBtn();
        })
    }
    let btnSaveCreateTemplate = document.getElementById('btn_save_create');
    if(btnSaveCreateTemplate !== null)
    {
        btnSaveCreateTemplate.addEventListener("click", function (element) {
            onUserPressedSaveCreateTemplateBtn();
        })
    }
    let btnCancelTemplate = document.getElementById('btn_edit_template_cancel_edit');
    if(btnCancelTemplate !== null)
    {
        btnCancelTemplate.addEventListener("click", function (element) {
            onUserPressedCancelEditTemplateBtn();
        })
    }
    let btnCancelCreateTemplate = document.getElementById('btn_edit_template_cancel_create');
    if(btnCancelCreateTemplate !== null)
    {
        btnCancelCreateTemplate.addEventListener("click", function (element) {
            onUserPressedCancelCreateTemplateBtn();
        })
    }

    modelLabelID = document.getElementById('model_name_field_edit');

    if(
        !btnSaveTemplate ||
        !btnCancelCreateTemplate ||
        !btnSaveCreateTemplate ||
        !modelLabelID ||
        !btnCancelTemplate)
    {
        alert("Ошибка!!!!")
        return
    }

    if(!accessEdit && accessFind)
    {
        btnSaveTemplate.remove()
    }

    editModelUnitID = undefined;
    isCreateTemplate = false;
    isEditTemplate = false;

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
