
import {CMessBox} from "/static/js/engine/CMessBox.js"


import {
    getTimestampInSeconds,
} from "/static/js/engine/common.js";


function hideResultBox()
{
    Object.values(blockID).forEach(function(values) {
        if(values !== null)
        {
            values.style.display = "none";
        }
    });
}

let BLOCK_TYPE = {
    BOX_RESULT: 0,
    BOX_ANIM: 1,
    BOX_ASR: 2
}
let blockID = {};


function setVisibleAnimBox(status)
{
   loadAnimBlock.style.display = "none";
}
function hideASRResultBox()
{
    asrResultBlock.style.display = "none";
}

$(document).ready(function() {
    blockID.resultBox = document.getElementById("all_result_block");
    blockID.loadAnimBlock = document.getElementById("load_anim_block");
    blockID.asrResultBlock = document.getElementById("asr_result_block");

    hideResultBox();

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