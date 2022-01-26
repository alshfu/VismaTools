function new_input(elem, data, class_name, name) {
    const input_tr_date = document.createElement(elem)
    input_tr_date.type = 'text'
    input_tr_date.className = class_name
    input_tr_date.value = data
    input_tr_date.name = name
    return input_tr_date;
}

function create_filter_element() {
    const settings_form = document.getElementById('settings')
    const new_input_group = document.createElement('div')
    new_input_group.className = 'input-group mb-1'

    const konto_number = new_input(
        'input',
        'data',
        'input-group-text col-sm-1 justify-content-start',
        'konto_n');
    const filter_list = new_input(
        'textarea',
        'data',
        'form-control col-lg justify-content-center',
        'filter_list');
    konto_number.style.height='38px'
    konto_number.style.color='red'
    new_input_group.appendChild(konto_number)
    new_input_group.appendChild(filter_list)
    settings_form.appendChild(new_input_group)
    settings_form.style.display = ''
}




function settings() {
    create_filter_element()
    console.log('Ïm hire ')

}