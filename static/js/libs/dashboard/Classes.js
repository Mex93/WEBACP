
import {
    Enum
} from './utils.js';

import {
    LINE_ID
} from './common.js';


const INCOMMING_ARR_TYPE = {
    HOURS: 0,
    FIVEMINS: 1,
    DAY_PLANE: 2,
    HOUR_PLANE: 3,
    LINEID: 4

};


const MAX_VRN_LINES = 4;
const MAX_ALL_LINES = 5;


const PARAMS_ID = Enum({
    LINE_NONE: 0,
    LINE_DAY_PLANE: 1,
    LINE_HOUR_PLANE: 2,
    LINE_FIVE_MINS: 3,
    LINE_FIVE_MINS_DOTS_ARR: 4,
    LINE_FIVE_MINS_MAIN_ARR: 5,
    LINE_HOURS: 6,
    LINE_HOURS_DOTS_ARR: 7,
    LINE_HOURS_MAIN_ARR: 8,
    LINE_NAME: 9,
    LINE_ID: 10,
    LINE_CANVAS_ID: 11,
    LINE_DATE_STATUS: 12
});
class LineParams
{
    #lineID;
    #lineName= String();
    #lineInHour = new Map();
    #lineInFiveMins = new Map();
    #lineDayPlane;
    #chartCanvasID;
    #lineHourPlane;
    #successCreatedStatus = false;
    #dateStatus = false;

    constructor(lineName, chartCanvasID, lineID)
    {
        if(lineName.length > 2)
        {
            if(lineID >= 0 && lineID <= 4)
            {
                this.#SetDefaultParams();
                this.#successCreatedStatus = true;
                this.#lineID = lineID;
                this.#lineName = lineName;
                this.#chartCanvasID = chartCanvasID;
            }
        }
    }
    SetParams(paramType, paramsToSet)
    {
        switch(paramType)
        {
            case PARAMS_ID.LINE_DATE_STATUS:
            {
                this.#dateStatus = paramsToSet;
                return true;
            }
            case PARAMS_ID.LINE_NAME:
            {
                this.#lineName = paramsToSet;
                return true;
            }
            case PARAMS_ID.LINE_DAY_PLANE:
            {
                this.#lineDayPlane = paramsToSet;
                return true;
            }
            case PARAMS_ID.LINE_HOUR_PLANE:
            {
                this.#lineHourPlane = paramsToSet;
                return true;
            }
            case PARAMS_ID.LINE_FIVE_MINS:
            {
                this.#lineInFiveMins = new Map(Object.entries(paramsToSet));
                return true;
            }
            case PARAMS_ID.LINE_HOURS:
            {
                this.#lineInHour = new Map(Object.entries(paramsToSet));
                return true;
            }
        }
        return false;
    }
    GetParams(paramType)
    {
        if(this.#successCreatedStatus === true)
        {
            switch(paramType)
            {
                case PARAMS_ID.LINE_ID:
                {
                    return (this.#lineID);  // вернёт с +1, не с нуля
                }
                case PARAMS_ID.LINE_DATE_STATUS:
                {
                    return (this.#dateStatus);
                }
                case PARAMS_ID.LINE_NAME:
                {
                    return (this.#lineName);
                }
                case PARAMS_ID.LINE_DAY_PLANE:
                {
                    return (this.#lineDayPlane);
                }
                case PARAMS_ID.LINE_HOUR_PLANE:
                {
                    return (this.#lineHourPlane);
                }
                case PARAMS_ID.LINE_FIVE_MINS_DOTS_ARR:
                {
                    return Array.from(this.#lineInFiveMins.values());
                }
                case PARAMS_ID.LINE_FIVE_MINS_MAIN_ARR:
                {
                    return Array.from(this.#lineInFiveMins.keys());
                }
                case PARAMS_ID.LINE_FIVE_MINS:
                {
                    return structuredClone(this.#lineInFiveMins);
                }
                case PARAMS_ID.LINE_HOURS_DOTS_ARR:
                {
                    return Array.from(this.#lineInHour.values());
                }
                case PARAMS_ID.LINE_HOURS_MAIN_ARR:
                {
                    return Array.from(this.#lineInHour.keys());
                }
                case PARAMS_ID.LINE_HOURS:
                {
                    return structuredClone(this.#lineInHour);
                }
                case PARAMS_ID.LINE_CANVAS_ID:
                {
                    return this.#chartCanvasID;
                }
            }
        }

        return false;
    }
    #SetDefaultParams()
    {
        this.#lineID = LINE_ID.NONE;
        this.#lineName = "None";
        this.#lineInHour.clear();
        this.#lineInFiveMins.clear();
        this.#lineDayPlane = 0;
        this.#lineHourPlane = 0;
        this.#successCreatedStatus = false;
    }
    static GetObjectIDFromLineID(objectArr, lineID)
    {
        if(typeof objectArr === 'object')
        {
            for(let i = 0; i < objectArr.length; i++)
            {
                if(objectArr[i].#successCreatedStatus === true)
                {
                    if(lineID === objectArr[i].#lineID)
                    {
                        return objectArr[i];
                    }
                }
            }
        }
        return -1;
    }
}



class CDebugger
{
    static #activePrint = false;
    constructor(activePrint)
    {
        if(typeof activePrint == "boolean")
        {
            if(activePrint)this.OnPrint();
            else this.OffPrint();
            return true;
        }
        return false;
    }
    dprint(message)
    {
        if(CDebugger.#activePrint)
        {
            if(message.length > 0)
            {
                console.log(message);
            }
        }
    }
    OnPrint = () => {CDebugger.#activePrint = true}
    OffPrint = () => {CDebugger.#activePrint = false}
}


class CChartID
{
    static arrLinesChart = Array();
    static chartCreatedCounts = 0;


    CreatedChart(lineID, chartID)
    {
        CChartID.arrLinesChart[lineID] = chartID;
        CChartID.chartCreatedCounts ++;
    }
    GetChartID(lineID)
    {
        let cID = CChartID.arrLinesChart[lineID];
        if(cID !== -1 && cID !== undefined)
        {
            return cID;
        }
        return false;
    }
    // DeleteChartID(lineID)
    // {
    //     if(CChartID.GetChartID(lineID))
    //     {
    //         CChartID.arrLinesChart[lineID] = -1;
    //         CChartID.chartCreatedCounts --;
    //         return
    //     }
    //     return false;
    // }
    GetARRIDFromChartID(chartID)
    {
        let chartFinded = -1;
        CChartID.arrLinesChart.forEach((el, index) => {
            if(el !== -1)
            {
                if(el === chartID)
                {
                    chartFinded = index;
                    return true;
                }
            }
        });
        return chartFinded;
    }
    GetLenght = () => CChartID.chartCreatedCounts;
}

class CLineShowType
{
    static SHOW_TYPES = {
        KZ: "kz",
        VRN: "vrn",
        ALL: "all"
    }
    static currentShowType = null;

    setType(currentShowType)
    {
        CLineShowType.currentShowType = currentShowType;
    }

    static convertType(stype)
    {
        let finded = null;
        Object.values(CLineShowType.SHOW_TYPES).forEach((element, index) =>
        {
            //console.log(element, stype);
            if(element === stype)
            {
                finded = index+1;
                return true;
            }
        })
        return finded;
    }
    isCurrentShowType(stype)
    {
        for(let values in CLineShowType.SHOW_TYPES)
        {
            if(CLineShowType.currentShowType === stype)
            {
                return true;
            }
        }
        return false;
    }
    getMaxLines()
    {
        if(this.isCurrentShowType(CLineShowType.SHOW_TYPES.KZ))
        {
            return 1;
        }
        else if(this.isCurrentShowType(CLineShowType.SHOW_TYPES.VRN))
        {
            return MAX_VRN_LINES;
        }
        else if(this.isCurrentShowType(CLineShowType.SHOW_TYPES.ALL))
        {
            return MAX_ALL_LINES;
        }
    }
}

class CUpdatedLines
{
    static #arrUpdated = Array();
    constructor() {
        return true;
    }

    ClearStats()
    {
        CUpdatedLines.#arrUpdated = CUpdatedLines.#arrUpdated.map((element) => element = -1);
        return true;
    }
    AddStats(lineID)
    {
        CUpdatedLines.#arrUpdated.push(lineID);
        return true;
    }
    GetCountLines()
    {
        let count = 0;
        CUpdatedLines.#arrUpdated.forEach((el) => {
            if(el !== -1)
            {
                count++;
            }
        });
        return count;
    }
    GetLenght = () => CUpdatedLines.#arrUpdated.length;
}

class CHTMLBlocks
{
    static CANVAS_CSS_NAME = [
        "chart_0",
        "chart_1",
        "chart_2",
        "chart_3",
        "chart_4",
    ];

    static arrGraphCSSName = [
        'canvas_main_one',
        'canvas_main_two',
        'canvas_main_tri',
        'canvas_main_four',
        'canvas_main_five',
    ];
    static arrGraphDivPlaceSpanID = [
        ['graf_1_1'],
        ['graf_2_1','graf_2_2'],
        ['graf_3_1','graf_3_2','graf_3_3'],
        ['graf_4_1','graf_4_2','graf_4_3','graf_4_4'],
        ['graf_5_1','graf_5_2','graf_5_3','graf_5_4','graf_5_5'],
    ];
    static arrOnBlocksName = [
        'lines_count_one',
        'lines_count_two',
        'lines_count_tris',
        'lines_count_fours',
        'lines_count_five',
    ];
    GetCanvasArr = (index) => CHTMLBlocks.CANVAS_CSS_NAME[index];
    GetGraphCSSName = (index) => CHTMLBlocks.arrGraphCSSName[index];
    GetGraphCSSLen = () => CHTMLBlocks.arrGraphCSSName.length;
    GraphDivPlaceSpanID = (mainIndex, index) => CHTMLBlocks.arrGraphDivPlaceSpanID[mainIndex][index];
    GraphDivPlaceSpanIDLen = (mainIndex, index) => CHTMLBlocks.arrGraphDivPlaceSpanID.length;
    GetOnBlocksName = (index) => CHTMLBlocks.arrOnBlocksName[index];
    GetOnBlocksLen = (index) => CHTMLBlocks.arrOnBlocksName.length;
}



export {
    CHTMLBlocks,
    LineParams,
    CUpdatedLines,
    CChartID,
    CLineShowType,
    CDebugger,
    MAX_VRN_LINES,
    MAX_ALL_LINES,
    PARAMS_ID,
    INCOMMING_ARR_TYPE

}

