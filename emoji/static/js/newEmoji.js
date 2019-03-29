$(document).ready(function () {
    $('#save-button').css({
        position: 'absolute',
        top: $('#emoji').offset().top + $('#emoji').height() + 50,
        left: $('#emoji').offset().left - $('#save-button').width()
    })

    $('#download-button').css({
        position: 'absolute',
        top: $('#emoji').offset().top + $('#emoji').height() + 50,
        left: $('#emoji').offset().left + $('#emoji').width()
    })

    // $('#img-div').width($('#emoji').width + 50)
    // $('#img-div').height($('#emoji').height + 50)
})