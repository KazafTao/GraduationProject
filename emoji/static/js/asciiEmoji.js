$(document).ready(function () {
    $('#search-box').css({
        position: 'absolute',
        top: $('#logo-box').offset().top + $('#logo').height() + 5,
        left: $('#logo-box').offset().left
    })

    $('#search-from').bind('keyup', function () {
        // 用百度的智能提示api来实现智能提示
        $.ajax({
            type: "GET",
            url: 'Ajax/',
            data: {
                'data': $('#search-input').val()
            },
            dataType: 'json',
            success: function (data) {
                $("#suggest-ul").html('')
                data.result.forEach(str => {
                    $(`<li onclick="inputValue($(this).text())">${str}</li>`).appendTo("#suggest-ul");
                })

                // 显示搜索建议
                $('#search-suggest').show().css({
                    position: 'absolute',
                    top: $('#search-from').offset().top + $('#search-from').height() + 1,
                    left: $('#search-from').offset().left
                })
            },
            error(err) {
                alert("ajax出错啦")
            }
        })
    })

    $('#error-div').css({
        position: 'absolute',
        top: $('#logo-box').offset().top + $('#logo').height() + $('#search-input').height() + 10,
        left: $('#search-box').offset().left + 55
    })

    $('#tag-div').css({
        position: 'absolute',
        top: $('#logo-box').offset().top + $('#logo').height() + $('#search-input').height() + 60,
        left: ($(window).width() - $('#tag-div').width()) / 2
    })

    $('.tag-name').bind('click', function (e) {
        var keyword = $(this).text()
        $('#search-input').attr('value', keyword)
        $('#search-from').submit()
    })


    if ($('#keyword').length > 0) {
        $('#keyword').hide()
        var value = 'Result of ' + $('#keyword').text()
        $('#logo').text(value)
        $('#logo').css({
            position: 'absolute',
            top: $('#logo-box').offset().top - $('#logo').height() - $('#search-input').height() - 30,
            left: 50,
            width: 400
        })
    }

    $('#page-div').css({
        position: 'absolute',
        top: $('#tag-div').offset().top + $('#tag-div').height() + 10,
        left: ($(window).width() - $('#page-div').width()) / 2
    })

    $('footer').css({
        position: 'absolute',
        top: $('#page-div').offset().top + $('#page-div').height() + 20
    })

})