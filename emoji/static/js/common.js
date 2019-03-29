$(document).ready(function () {
    $(document).bind('click', function () {
        $('#search-suggest').hide()
    })

    $('#search-from').attr('autocomplete', 'off')

})

function baiduAjax(json) {
    $("#suggest-ul").html('');
    json.s.forEach(str => {
        $(`<li>${str}</li>`).appendTo("#suggest-ul");
    })
}

function inputValue(value) {
    $('#search-input').val(value)
    $('#search-input').focus()
}