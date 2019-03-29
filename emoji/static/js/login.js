$(document).ready(function () {
    // $('#email').hide()

    $('#bg-div').css({
        position: 'absolute',
        top: ($(window).height() - $('#bg-div').height()) / 2,
        left: ($(window).width() - $('#logo-box').width()) / 2
    })

    $('#form-div').css({
        position: 'absolute',
        top: $('#logo-box').offset().top + 30,
        left: 200
    })

})
