const fs = require('fs');
const path = require('path');

let rawdata = fs.readFileSync(path.resolve(__dirname, 'MyGUI_Trace.json'));
let JSON_DATA = JSON.parse(rawdata);

function CreateHTMLFromJSON(jsonData, startElem)
{
    jQuery.each(obj, function (i, val) {
        let myElm = document.createElement("div");

        myElm.innerText = i;
        myElm.style.color = 'red';

        startElem.appendChild(myElm);

        CreateHTMLFromJSON(val, myElm);
    });
}

CreateHTMLFromJSON(JSON_DATA, document.body);

