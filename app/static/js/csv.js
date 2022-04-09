function replaceAll(string, search, replace) {
    return string.split(search).join(replace);
}

String.prototype.hexEncode = function () {
    var hex, i;

    var result = "";
    for (i = 0; i < this.length; i++) {
        hex = this.charCodeAt(i).toString(16);
        result += ("000" + hex).slice(-4);
    }

    return result
}

String.prototype.hexDecode = function () {
    let j;
    let hexes = this.match(/.{1,4}/g) || [];
    let back = "";
    for (j = 0; j < hexes.length; j++) {
        back += String.fromCharCode(parseInt(hexes[j], 16));
    }

    return back;
}

function encode(str) {
    str = str.hexEncode()
    str = replaceAll(str, "00c30085", "00c5")
    str = replaceAll(str, "00c300a5", "00e5")
    str = replaceAll(str, "00c30084", "00c4")
    str = replaceAll(str, "00c300a4", "00e4")
    str = replaceAll(str, "00c30096", "00d6")
    str = replaceAll(str, "00c300b6", "00f6")
    str = str.hexDecode()
    return str
}


function tr_filter(tr_name, tr_amount) {
    let a = 1930
    let b = 1799
    let tr_color = ''
    for (const fil in filter_list) {
        let konto_num = filter_list[fil][0].konto
        let filter_n = filter_list[fil][0].filter_str.split('|')
        // console.log(konto_num + '>>>' + filter_n)
        if (parseInt(tr_amount) < 0) {
            for (const string of filter_n) {
                if (tr_name.includes(string)) {
                    a = 1930
                    b = parseInt(konto_num)
                    tr_color = 'coral'
                    // console.log("STOP " + b + '=>' + tr_name)
                    // console.log('string ->'+ string +' tr_name '+ tr_name)
                    return [a, b, tr_color]
                    break
                }
            }
        } else if (parseInt(tr_amount) > 0) {
            a = 1930
            b = 1910
            tr_color = 'green'
            return [a, b, tr_color]
            break
        }
    }
    // console.log(b + ' konto ')
    return [a, b, tr_color]
}

function new_input(data, class_name, name) {
    const input_tr_date = document.createElement('input')
    input_tr_date.type = 'text'
    input_tr_date.className = class_name
    input_tr_date.value = data
    input_tr_date.name = name
    return input_tr_date;
}

function createARow(tr_date, tr_name, tr_amount, tr_id) {
    const new_input_group = document.createElement('div')
    new_input_group.className = 'input-group mb-1'

    //transaktion ID
    const input_tr_id = new_input(tr_id, 'input-group-text col-sm-1 justify-content-start', 'tr_id');
    input_tr_id.readOnly = "readonly"

    //transaktion Date
    const input_tr_date = new_input(tr_date, 'input-group-text col-sm-2 justify-content-start', 'tr_date');
    input_tr_date.readOnly = "readonly"

    //transaktion Name
    const input_tr_name = new_input(tr_name.replace('"', ''), 'form-control col-lg justify-content-center', 'tr_name')
    input_tr_name.style.textAlign = 'center'

    //transaktion amount
    const input_tr_amount = new_input(tr_amount, 'iput-group-text col-sm-2 justify-content-end', 'tr_amount')
    input_tr_amount.readOnly = "readonly"

    //transaktion konto
    const konto = tr_filter(tr_name, tr_amount, input_tr_name)
    // console.log(tr_name + ' ' + konto[1])

    const input_tr_konto_primary = new_input(konto[0], 'input-group-text col-sm-1 justify-content-start', 'konto_p');
    input_tr_konto_primary.readOnly = "readonly"
    const input_tr_konto_secondary = new_input(konto[1], 'input-group-text col-sm-1 justify-content-start', 'konto_s');
    input_tr_konto_secondary.readOnly = "readonly"


    if (parseInt(tr_amount) < 0) {
        input_tr_date.style.color = 'red'
        input_tr_amount.style.color = 'red'
        // input_tr_name.style.color = 'red'
        input_tr_konto_secondary.style.color = 'red'
        input_tr_konto_primary.style.color = 'red'
    } else {
        input_tr_date.style.color = 'green'
        input_tr_amount.style.color = 'green'
        //input_tr_name.style.color = 'green'
        input_tr_konto_secondary.style.color = 'green'
        input_tr_konto_primary.style.color = 'green'
    }
    if (konto[2] === 'coral') {
        input_tr_konto_secondary.style.color = konto[2]
        input_tr_name.style.color = konto[2]
    }


    new_input_group.appendChild(input_tr_id)
    new_input_group.appendChild(input_tr_date)
    new_input_group.appendChild(input_tr_name)
    new_input_group.appendChild(input_tr_konto_primary)
    new_input_group.appendChild(input_tr_konto_secondary)
    new_input_group.appendChild(input_tr_amount)


    document.getElementById("action_form").appendChild(new_input_group);

};

function move_submit_button() {
    element = document.getElementById("submit_button");
    element.style.display = 'none'
    const new_submit_button = document.createElement('button')
    new_submit_button.type = 'submit'
    new_submit_button.className = 'btn btn-primary'
    new_submit_button.innerText = 'Klart'
    document.getElementById("action_form").appendChild(new_submit_button);
}

function SEB(data) {
    data.shift()
    document.getElementById('summary')
    // console.table(data)
    let tr_id = 0
    for (const line of data) {
        const line_array = line.toString().split(',')
        if (tr_id == 0) document.getElementById('summary').value = accounting.formatMoney(parseInt(line[5]), "Kr", 2, " ", ",", "%v %s"); // €4.999,99()
        if (line_array.length === 6) {
            if (line_array[4] != undefined) {
                createARow(line_array[0], encode(replaceAll(line_array[3], '"', '')), line_array[4], tr_id)
            }
        } else {
            let msg_error = document.createElement('div')
            msg_error.innerHTML = "OBS!!! hittad fel i line " + tr_id + " | " + line + "<br>"
            document.getElementById('error_msg').appendChild(msg_error)
        }


        tr_id++
    }
    move_submit_button()
}

function SWEDBANK(data) {
    data.shift()
    data.shift()
    document.getElementById('summary')
    // console.table(data)
    let tr_id = 0
    for (const line of data) {
        const line_array = line.toString().split(',')
        if (tr_id == 0) document.getElementById('summary').value = accounting.formatMoney(parseInt(line[11]), "Kr", 2, " ", ",", "%v %s"); // €4.999,99()
        if (line_array.length === 12) {
            if (line_array[4] != undefined) {
                createARow(line_array[7], encode(replaceAll(line_array[8], '"', '')), line_array[10], tr_id)
            }
        } else {
            let msg_error = document.createElement('div')
            msg_error.innerHTML = "OBS!!! hittad fel i line " + tr_id + " | " + line + "<br>"
            document.getElementById('error_msg').appendChild(msg_error)
        }
        tr_id++
    }
    move_submit_button()
}

function SVEA(data) {
    data.shift()
    document.getElementById('summary')
    // console.table(data)
    let tr_id = 0
    for (const line of data) {
        const line_array = line.toString().split(';')
        if (tr_id == 0) document.getElementById('summary').value = accounting.formatMoney(parseInt(replaceAll(line_array[4], '"', '')), "Kr", 2, " ", ",", "%v %s"); // €4.999,99()
        if (line_array.length === 5) {
            if (line_array[4] != undefined) {
                createARow(replaceAll(line_array[0], '"', ''), encode(replaceAll(line_array[1], '"', '')), replaceAll(replaceAll(line_array[2], '"', ''), ',', '.'), tr_id)

            }
        } else {
            let msg_error = document.createElement('div')
            msg_error.innerHTML = "OBS!!! hittad fel i line " + tr_id + " | " + line + "<br>"
            document.getElementById('error_msg').appendChild(msg_error)
        }
        tr_id++
    }
    move_submit_button()
}

function NORDEA(data) {
    data.shift()
    document.getElementById('summary')
    // console.table(data)
    let tr_id = 0
    for (const line of data) {
        const line_array = line.toString().split(';')
        if (tr_id == 0) document.getElementById('summary').value = accounting.formatMoney(parseInt(replaceAll(line_array[8], '"', '')), "Kr", 2, " ", ",", "%v %s"); // €4.999,99()
        if (line_array.length === 10) {
            if (line_array[4] != undefined) {
                createARow(line_array[0], encode(replaceAll(line_array[5], '"', '')), replaceAll(line_array[1], ',', '.'), tr_id)

            }
        } else {
            let msg_error = document.createElement('div')
            msg_error.innerHTML = "OBS!!! hittad fel i line " + tr_id + " | " + line + "<br>"
            document.getElementById('error_msg').appendChild(msg_error)
        }
        tr_id++
    }
    move_submit_button()
}

function MARGINAL(data) {
    data.shift()
    document.getElementById('summary')
    // console.table(data)
    let tr_id = 0
    for (const line of data) {
        const line_array = line.toString().split(';')
        if (tr_id == 0) document.getElementById('summary').value = accounting.formatMoney(parseInt(replaceAll(line_array[3], '"', '')), "Kr", 2, " ", ",", "%v %s"); // €4.999,99()
        if (line_array.length === 4) {
            if (line_array[3] != undefined) {
                createARow(line_array[0], encode(replaceAll(line_array[1], '"', '')), replaceAll(line_array[2], ',', '.'), tr_id)

            }
        } else {
            let msg_error = document.createElement('div')
            msg_error.innerHTML = "OBS!!! hittad fel i line " + tr_id + " | " + line + "<br>"
            document.getElementById('error_msg').appendChild(msg_error)
        }
        tr_id++
    }
    move_submit_button()
}

function uploadDealcsv() {
};


/*------ Method for read uploded csv file ------*/
uploadDealcsv.prototype.getCsv = function (e) {
    let main_bank_account = document.getElementById('main_bank_account')
    main_bank_account.addEventListener('change', function () {
        let konto_p = document.getElementsByName('konto_p')
        for (let elem of konto_p) {
            console.log(elem.value)
            elem.value = main_bank_account.value
        }
    })

    let input = document.getElementById('cvs_file');
    input.addEventListener('change', function () {

        if (this.files && this.files[0]) {

            let myFile = this.files[0];
            let reader = new FileReader();

            reader.addEventListener('load', function (e) {

                let csvdata = e.target.result;
                parseCsv.getParsecsvdata(csvdata); // calling function for parse csv data
            });

            reader.readAsBinaryString(myFile);
        }
    });
}

/*------- Method for parse csv data and display --------------*/
uploadDealcsv.prototype.getParsecsvdata = function (data) {

    let parsedata = [];

    let newLinebrk = data.split("\n");
    for (let i = 0; i < newLinebrk.length; i++) {
        parsedata.push(newLinebrk[i].split(","))
    }
    document.getElementById('action_form').style.display = ''
    let bank = parseInt(document.getElementById('bank').value)
    console.log(typeof (bank))
    if (bank === 0 || bank === 1) //SEB
        SEB(parsedata)
    else if (bank === 2) //SWEDBANK
        SWEDBANK(parsedata)
    else if (bank === 3) //SVEA Bank
        SVEA(parsedata)
    else if (bank === 4) //Nordea
        NORDEA(parsedata)
    else if (bank === 5) //Nordea
        MARGINAL(parsedata)


    // console.table(parsedata);
}

var parseCsv = new uploadDealcsv();
parseCsv.getCsv();
