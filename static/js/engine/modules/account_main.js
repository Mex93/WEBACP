import {CForms} from "../CForms.js";
import {CFieldsCheck} from "../CFieldsCheck.js";
import {CMessBox} from "../CMessBox.js";
import {CWindowBox} from "../CWindowBox.js";

import {
    getTimestampInSeconds,
    } from "../common.js";


let anim_table_block = null;
let table_block = null;
let cmessBox = new CMessBox("error_box_logs")
let query = false;
let getUpdate = 0;
function get_logs_ajax()
{
    if(query)
        return false;

    if(getUpdate > getTimestampInSeconds())
        return false

    query = true;

    $.ajax({
        data : {},
        dataType: 'json',
        type : 'POST',
        url : './account_logs_ajax',
        contentType: "application/json",
        success: function(data) {
            query = false;
            getUpdate = getTimestampInSeconds()+20;
            cmessBox.hide();

            if(data.result === true)
            {
                if(!data.logs)
                {
                    cmessBox.sendErrorMessage(data.error_text);
                }
                else
                {
                    let count = 0;
                    let tableID = document.querySelector("#table_logs_id:last-child")
                    if(tableID !== null)
                    {
                        let str = ""
                        for(let array of data.logs)
                        {
                            str = `<tr><td>${array[1]}</td><td>${array[2]}</td></tr>`;
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


let cwindowBox = new CWindowBox()
$(document).ready(function() {
    anim_table_block = document.getElementById("load_logs_anim_block");
    table_block = document.getElementById("load_logs_table");

    if(table_block !== null)
        table_block.style.display = "none";

    setTimeout(get_logs_ajax, 3000);

    //let csrftoken = $('meta[name=csrf-token]').attr('content')
    let csrftoken = $('.table-logs input[name=csrf_token]').attr('value')

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
    cwindowBox.show("Выполняется авторизация",
        "Если ваш браузер не поддерживает автоматическую переадресацию, " +
        "то просто обновите страницу", "rgb(4, 170, 109)", 0);

}); // document ready