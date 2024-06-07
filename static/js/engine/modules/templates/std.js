
import {CMessBox} from "/static/js/engine/CMessBox.js"

let anim_table_block = null;
let table_block = null;
let query = false;

let acessDelete = false;
let accessEdit = false;

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
    console.log("Нажата клавиша Редактировать")
    console.log(mmUnit.getModelName())
    return false;
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

                                str = `<tr>
                                        <td>${modelName}</td>
                                        <td>${modelTypeName}</td>
                                        <td>${lastUpdateTime}</td>
                                        <td><div class = 'inline_buttom'>${btn_edit} ${btn_del}</div></td>
                                       </tr>`;
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
                            table_block.style.display = "block";
                            anim_table_block.style.display = "none";
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


// ----------------------------------------------------------------- FUNC END

$(document).ready(function() {
    anim_table_block = document.getElementById("skeleton_anim_block");
    table_block = document.getElementById("res_table_block");

    if(
        !anim_table_block ||
    !table_block)
    {
        alert("Ошибка!!!!")
        return
    }
    if(anim_table_block)
    {
        anim_table_block.style.display = "block";
        table_block.style.display = "none";
    }

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
