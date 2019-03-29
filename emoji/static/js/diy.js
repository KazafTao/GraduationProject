$(document).ready(function () {
    // $('#result').hide()

    $('#main-div').css({
        position: 'absolute',
        top: 100,
        left: ($(window).width() - $('#main-div').width()) / 2
    })

    $('#text').css({
        position: 'absolute',
        top: $('#material').offset().top + 0.6 * $('#material').height()
    })

    $('#text').bind('click', function () {
        $('#text').text('')
        // setTextColor('black')
    })

    $('#material').bind('click', function () {
        $('#text').text('点我输入文字')
    })

    $('#toolbar').css({
        position: 'absolute',
        top: $('#material-div').offset().top - 100,
        left: $('#material-div').offset().left + 200
    })

    $('#font-div').find('div').first().css('background-color','red')
    $('#hidden-font').val('msyh')
    
    $('.font').click(function () {
        $('.font').css('background-color','transparent')
        $(this).css('background-color','red')
        $('#hidden-font').val($(this).css('font-family'))
    })

    $('#diy-button').css({
        position: 'absolute',
        top: $('#color-div').offset().top + 40,
        left: $('#material').offset().left - 300
    })

    $('#diy-button').bind('click', function () {
        // 获取图片，文字，字体，颜色，大小等属性提交给服务器
        $('#hidden-material').val($('#material')[0].src)
        $('#hidden-text').val($('#text').text())
        var text = document.getElementById("text")
        var fontSize = window.getComputedStyle(text).fontSize
        var color = window.getComputedStyle(text).color
        $('#hidden-font-size').val(fontSize)
        $('#hidden-color').val(color)
        $('#form').submit()
    })

    // $('#diy-button').click(function () {
    //     var material=$('#material')[0].src
    //     var text=$('#text').text()
    //     var textele = document.getElementById("text")
    //     var fontSize = window.getComputedStyle(textele).fontSize
    //     var color = window.getComputedStyle(textele).color
    //     $.get("diy/diy",{
    //         'material':material,
    //         'text':text,
    //         'font-size':fontSize,
    //         'color':color,
    //         'font':$('#hidden-font').val(),
    //     },function (ret) {
    //         var img="data:image/png;base64," + ret;
    //         // alert(ret)
    //         $("#result").attr("src", ret)
    //         $('#result').show()
    //     })
    // })
})

function setTextColor(color) {
    $('#text').css('color', color)
}
