function new_input(data, class_name) {
    const input_tr_date = document.createElement('input')
    input_tr_date.type = 'text'
    input_tr_date.className = class_name
    input_tr_date.value = data
    return input_tr_date;
}

function createARow(tr_date, tr_name, tr_amount, tr_id) {
    const new_input_group = document.createElement('div')
    new_input_group.className = 'input-group mb-1'

    //transaktion ID
    const input_tr_id = new_input(tr_id, 'input-group-text col-sm-1 justify-content-start');
    input_tr_id.disabled = true
    //transaktion Date
    const input_tr_date = new_input(tr_date, 'input-group-text col-sm-2 justify-content-start');
    input_tr_date.disabled = true
    //transaktion Name
    const input_tr_name = new_input(tr_name, 'form-control col-lg justify-content-center')
    input_tr_name.style.textAlign = 'center'
    //transaktion amount
    const input_tr_amount = new_input(tr_amount, 'input-group-text col-sm-2 justify-content-end')
    input_tr_amount.disabled = true
    //transaktion konto
    const konto = tr_filter(tr_name, tr_amount)

    const input_tr_konto_primary = new_input(konto[0], 'input-group-text col-sm-1 justify-content-start');
    input_tr_konto_primary.disabled = true
    const input_tr_konto_secondary = new_input(konto[1], 'input-group-text col-sm-1 justify-content-start');
    input_tr_konto_secondary.disabled = true

    if (parseInt(tr_amount) < 0) {
        input_tr_date.style.color = 'red'
        input_tr_amount.style.color = 'red'
        // input_tr_name.style.color = 'red'
        input_tr_konto_secondary.style.color = 'red'
        input_tr_konto_primary.style.color = 'red'
    } else {
        input_tr_date.style.color = 'green'
        input_tr_amount.style.color = 'green'
        // input_tr_name.style.color = 'green'
        input_tr_konto_secondary.style.color = 'green'
        input_tr_konto_primary.style.color = 'green'
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
        if (tr_id == 0)
            document.getElementById('summary').value = accounting.formatMoney(parseInt(line[5]), "Kr", 2, " ", ",", "%v %s"); // €4.999,99()
        const line_array = line.toString().split(',')
        createARow(line_array[0], line_array[3], line_array[4], tr_id)
        tr_id++
    }
    move_submit_button()
}

function uploadDealcsv() {
};

function tr_filter(tr_name, tr_amount) {

    //Bokföringssystemet
    // Samtliga utbetalningar som heter Aut, avräkning, avr, utlägg, privat ska döpas till konto 2893 istället för 1799.
    // Samtliga transaktioner som heter Skatteverket ska ha kontonummer 1630
    // Samtliga transaktioner som är nummer, t.ex. 81056563654326 döper du till 1613
    // Samtliga transaktioner som heter fordonsskatt eller trängselskatt döps till konto 5616

    // Samtliga transaktioner som heter banktjänster döps till 6570
    // Samtliga transaktioner som heter lön, döps till 1613
    // Samtliga transaktioner som heter lån döps till 1680
    // Kan du även lägga till följande kontonr i localhost:
    // 1932, 1933, 1934, 1935

    const konto_2893 = [
        'Aut',
        'avräkning',
        'avr',
        'utlägg',
        'privat',
        'Vattenfall'
    ]
    const konto_5616 = [
        'fordonsskatt',
        'trängselskatt',
        'Fordonsskatt',
        'Trängselskatt',
    ]
    const konto_1630 = [
        'Skatteverket',
        'skatteverket',
        'Felparkeringsavgift',
        'skatt'
    ]
    const konto_6570 = [
        'banktjänster',
        'Banktjänster'
    ]
    const konto_1613 = [
        'lön',
        'LÖN',
        'Lön'
    ]
    const konto_1680 = [
        'lån',
        'LÅN',
        'Lån'
    ]

    let a, b

    function filter(konto_array, konto_a, konto_b, tr_name) {
        for (const string of konto_array) {
            if (tr_name.includes(string)) {
                a = konto_a
                b = konto_b
                break
            }
        }
    }

    if (parseInt(tr_amount) < 0) {
        filter(konto_2893, 1930, 2893, tr_name);
        filter(konto_1630, 1930, 1630, tr_name);
        filter(konto_5616, 1930, 5616, tr_name);
        filter(konto_6570, 1930, 6570, tr_name);
        filter(konto_1613, 1930, 1613, tr_name);
        filter(konto_1680, 1930, 1680, tr_name);

    } else {
        a = 5555
        b = 6666
    }
    return [a, b]
}

/*------ Method for read uploded csv file ------*/
uploadDealcsv.prototype.getCsv = function (e) {

    let input = document.getElementById('cvs_file');
    input.addEventListener('change', function () {

        if (this.files && this.files[0]) {

            var myFile = this.files[0];
            var reader = new FileReader();

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
    SEB(parsedata)


    // console.table(parsedata);
}

var parseCsv = new uploadDealcsv();
parseCsv.getCsv();
