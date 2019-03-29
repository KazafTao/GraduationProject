$(document).ready(function () {

    $(".bars").click(function () {
        $(".bars").toggleClass("active");
        $(".nav").toggleClass("active");
    });

    $('#user-div').css({
        position: 'absolute',
        top: $('.nav').offset().top + $('.nav').height(),
        left: $(".bars").offset().left + $(".bars").width()
    })

    if ($('#error_message').text()) {
        $('#error-div').css({
            position: 'absolute',
            top: $('#search-box').offset().top - $('#search-box').height() - 5,
            left: $('#search-box').offset().left + 55
        })
        // 取消placeholder的内容以免和错误信息相互干扰
        $('#search-input').attr('placeholder', '')
    } else
        $('#error-div').hide()

    $('#search-type').hide()

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

            // baidu version
            // url: "https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su",
            // data: {'wd': $('#search-input').val()},
            // dataType: 'jsonp',
            // jsonp: 'cb',
            // success: baiduAjax,

            error(err) {
                alert("ajax出错啦")
            }
        })
    })

});

