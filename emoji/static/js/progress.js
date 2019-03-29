$(function () {
    var tag = false, ox = 0, left = 0, bgleft = 0;
    $('.progress_btn').mousedown(function (e) {
        ox = e.pageX - left;
        tag = true;
    });
    $(document).mouseup(function () {
        tag = false;
    });
    //鼠标移动
    $('.progress').mousemove(function (e) {
        if (tag) {
            left = e.pageX - ox;
            if (left <= 0) {
                left = 0;
            } else if (left > 300) {
                left = 300;
            }
            $('.progress_btn').css('left', left);
            $('.progress_bar').width(left);
            $('.text').html(parseInt((left / 300) * 100) + '%');
            $('#text').css("font-size", 20 + parseInt((left / 300) * 20))
        }
    });

    //鼠标点击
    $('.progress_bg').click(function (e) {
        if (!tag) {
            bgleft = $('.progress_bg').offset().left;
            left = e.pageX - bgleft;
            if (left <= 0) {
                left = 0;
            } else if (left > 300) {
                left = 300;
            }
            $('.progress_btn').css('left', left);
            $('.progress_bar').animate({width: left}, 300);
            var percentage = parseInt((left / 300))
            $('.text').html(percentage * 100 + '%');
        }
    });
});