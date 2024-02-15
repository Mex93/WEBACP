import {
    CForms,

} from "./CForms";






// import {
//     LineParams,
//     PARAMS_ID,
//     INCOMMING_ARR_TYPE,
//     MAX_VRN_LINES,
//     MAX_ALL_LINES,
//     CUpdatedLines,
//     CChartID,
//     CDebugger,
//     CLineShowType,
//     CHTMLBlocks
//
// } from './libs/dashboard/Classes.js';

let inputFieldNameID = null
let inputFieldEmailID = null
let inputFieldSaveMeID = null

function get_login(nickname, password, safemy) {
    console.log("Я тут")
    let json_text = '{"cpassword": "'+ password +'", "cnickname": "'+ nickname +'", "csavemy": "'+ safemy +'"}';
    let completed_json = jQuery.parseJSON(json_text);

    $.getJSON('./account.py',
        completed_json, function (data)
        {
            console.log(data)
            let c_name = new CForms(inputFieldNameID)
            c_name.clearField()

        }
    );
    return false
}



$(document).ready(function() {

    inputFieldNameID = document.getElementById("user_name")
    inputFieldEmailID = document.getElementById("user_pass")
    inputFieldSaveMeID = document.getElementById("user_save_me")

    let c_name = new CForms(inputFieldNameID)
    let c_pass = new CForms(inputFieldEmailID)
    let c_savemy = new CForms(inputFieldSaveMeID)

    $("#login_form").on("submit", function (event) {
        event.preventDefault(); // Отменяем стандартное поведение формы

        // Получаем данные из полей формы
        const data = {
            name: c_name.getInputValue(),
            email: c_pass.getInputValue(),
            savemy: c_savemy.getInputValue(),
        }
        get_login(data.name, data.email, data.savemy)
    });




}); // document ready