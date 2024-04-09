import {
    BUTTOM_TYPE,
    TABLE_TYPE
} from "/static/js/engine/modules/asr/common.js";


class cButtons
{
    #ARRAY_INDEX_TYPE = {
        DOCUMENT_ID: 0,
        NAME: 1,
        TYPE: 2,
    }
    #arrayBtn = [];

    addBTN(btnID, btnName, btnType)
    {
        let len = this.#arrayBtn.push([btnID, btnName, btnType]);
        btnID.innerText = btnName;
        return len;
    }
    getArrayIndexFromBTNType(btnType)
    {
        for(let i= 0; i < this.#arrayBtn.length; i++)
        {
            if(this.#arrayBtn[i][this.#ARRAY_INDEX_TYPE.TYPE] === btnType)
            {
                return i;
            }
        }
        return null;
    }
    isValidIndex(index)
    {
        return !!this.#arrayBtn[index].length;
    }
    getName(index)
    {
        if(this.isValidIndex(index))
        {
            return this.#arrayBtn[index][this.#ARRAY_INDEX_TYPE.NAME];
        }
    }
    getType(index)
    {
        if(this.isValidIndex(index))
        {
            return this.#arrayBtn[index][this.#ARRAY_INDEX_TYPE.TYPE];
        }
    }
    showStatus(index, status)
    {
        this.#arrayBtn[index][this.#ARRAY_INDEX_TYPE.DOCUMENT_ID].style.display = (status) ? "":"none";
    }

    setShowForAll(status)
    {
        this.#arrayBtn.forEach( (arr, index) => {
            if(this.isValidIndex(index))
            {
                this.showStatus(index, status);
            }
        })
    }
    switchBTNStatus(btnSwitchType)
    {
        let btnIndexEdit = this.getArrayIndexFromBTNType(BUTTOM_TYPE.TYPE_EDIT);
        let btnIndexDel = this.getArrayIndexFromBTNType(BUTTOM_TYPE.TYPE_DEL);
        let btnIndexSave = this.getArrayIndexFromBTNType(BUTTOM_TYPE.TYPE_SAVE);
        let btnIndexCancel = this.getArrayIndexFromBTNType(BUTTOM_TYPE.TYPE_CANCEL);

        if(btnSwitchType === TABLE_TYPE.TYPE_EDITTING)
        {
            if(btnIndexEdit !== null)this.showStatus(btnIndexEdit, false);
            if(btnIndexDel !== null)this.showStatus(btnIndexDel, true);
            if(btnIndexSave !== null)this.showStatus(btnIndexSave, true);
            if(btnIndexCancel !== null)this.showStatus(btnIndexCancel, true);
        }
        else if(btnSwitchType === TABLE_TYPE.TYPE_STANDART)
        {
            if(btnIndexEdit !== null)this.showStatus(btnIndexEdit, true);
            if(btnIndexDel !== null)this.showStatus(btnIndexDel, true);
            if(btnIndexSave !== null)this.showStatus(btnIndexSave, false);
            if(btnIndexCancel !== null)this.showStatus(btnIndexCancel, false);
        }

    }

}


export {
    cButtons
}