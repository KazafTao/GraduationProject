$(document).ready(function () {
    $('#logo-box').css({
        position: 'absolute',
        top: 30,
        left: ($(window).width() - $('#logo-box').width()) / 2
    })

    $('#page-div').css({
        position: 'absolute',
        top: $('#main-div').offset().top + $('#main-div').height() + 10,
        left: ($(window).width() - $('#page-div').width()) / 2
    })
})