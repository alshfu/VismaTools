function createARow(tr_date, tr_name, tr_amount,) {
    const new_input_group = document.createElement('div')
    new_input_group.className = 'input-group mb-1'
    // const input_group_prepend = document.createElement('div')
    // input_group_prepend.className = 'input-group-prepend col-sm'
    const input_group_text_1 = document.createElement('span')
    input_group_text_1.className = 'input-group-text col-sm-2 justify-content-start'
    const input_group_text_2 = document.createElement('span')
    input_group_text_2.className = 'input-group-text col-sm-2 justify-content-end'
    const new_input = document.createElement('input')
    new_input.style = 'text-align:center'
    new_input.className = 'form-control col-lg justify-content-center'
    new_input.type = 'text'

    new_input.value = tr_name

    input_group_text_1.innerText = tr_date

    if (parseInt(tr_amount) < 0)
        input_group_text_2.style.color = 'red'
    else
        input_group_text_2.style.color = 'green'
    input_group_text_2.innerText = tr_amount

    new_input_group.appendChild(input_group_text_1)
    // new_input_group.appendChild(input_group_prepend)
    new_input_group.appendChild(new_input)
    new_input_group.appendChild(input_group_text_2)


    document.getElementById("action_form").appendChild(new_input_group);

};

function SEB(data) {
    data.shift()
    // console.table(data)

    for (const line of data) {
        const line_array = line.toString().split(',')
        createARow(line_array[0], line_array[3], line_array[4])
    }
}

function uploadDealcsv() {
};

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
