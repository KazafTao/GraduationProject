$(document).ready(function () {
    $('#search-type').hide()

    $('#search-type-div').css({
        position: 'absolute',
        top: $('#search-from').offset().top - $('#search-type-div').height - 5,
        left: $('#search-from').offset().left
    })

    $('#search-from').bind('keyup', function () {
        // 用百度的智能提示api来实现智能提示
        $.ajax({
            type: "GET",
            url: '../Ajax/',
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
})

function submit(choice) {
    switch (choice) {
        case '全部':
            $('#search-type').val('all')
            $('#search-from').submit()
            break
        case '静态图片':
            $('#search-type').val('static')
            $('#search-from').submit()
            break
        case 'gif':
            $('#search-type').val('gif')
            $('#search-from').submit()
            break
    }
}