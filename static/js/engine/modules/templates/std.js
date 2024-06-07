
import {CMessBox} from "/static/js/engine/CMessBox.js"

let anim_table_block = null;
let table_block = null;
let query = false;

let acessDelete = false;
let accessEdit = false;

let cmessBox = new CMessBox("error_box")

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
                        let tableID = document.querySelector("#table_id_models_list:last-child")
                        if(tableID !== null)
                        {
                            let str = ""
                            for(let array of data.arr)
                            {
                                let modelName = array[0];
                                let modelID = array[1];
                                let modelTypeName = array[2];
                                let lastUpdateTime = array[3];
                                let serialNumber = array[4];
                                let scanFK = array[5];

                                let btn_del = null;
                                let btn_edit = null;

                                if(acessDelete)
                                    btn_del = `<button id = "btn_del_unit_${modelID}" type="submit" name = "delete" value = "delete" class = "btm_submit-common delete">Удалить</button>`
                                if(accessEdit)
                                    btn_edit = `<button id = "btn_edit_unit_${modelID}" type="submit" name = "edit" value = "edit" class = "btm_submit-common">Редактировать</button>`

                                str = `<tr>
                                        <td>${modelName}</td>
                                        <td>${modelTypeName}</td>
                                        <td>${lastUpdateTime}</td>
                                        <td>${btn_del}${btn_edit}</td>
                                       </tr>`;
                                let createElement = document.createElement("tr");
                                createElement.innerHTML = str;
                                tableID.append(createElement);
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


    if(!isValid(acessDelete) || !isValid(accessEdit))
    {
        alert("Ошибка!!!!")
        console.log(acessDelete)
        console.log(accessEdit)
        return
    }


    setTimeout(get_tv_list_ajax, 3000);

    //let csrftoken = $('meta[name=csrf-token]').attr('content')
    let csrftoken = $('.container-common input[name=csrf_token]').attr('value')

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
}); // document ready
