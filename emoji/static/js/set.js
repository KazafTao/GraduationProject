$(document).ready(function () {
    $('#logo-box').css({
        position: 'absolute',
        top: 50,
        left: ($(window).width() - $('#logo-box').width()) / 2
    })

    $('#series-div').css({
        position: 'absolute',
        top: $('#logo-box').offset().top + $('#slogan').height(),
        left: ($(window).width() - $('#series-div').width()) / 2
    })

    $('#page-div').css({
        position: 'absolute',
        top: $('#series-div').offset().top + $('#series-div').height() + 10,
        left: ($(window).width() - $('#page-div').width()) / 2
    })

    $('footer').css({
        position: 'absolute',
        top: $('#page-div').offset().top + $('#page-div').height() + 20
    })
})