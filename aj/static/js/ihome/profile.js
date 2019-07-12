function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#form-avatar").submit(function(){
        $(this).ajaxSubmit({
            url: '/user/profile/',
            dataType: 'json',
            type: 'PATCH',
            // data:{'avatar':avatar,'name':name},
            success: function (msg) {
                if (msg.code == 200) {
                    $('#user-avatar').attr('src', '/static/' + msg.image_url)

                }
            },
            error: function (msg) {
                $('#error_msg1').show();
            }
        })
        return false;
    });

    $("#form-name").submit(function(){
        var name = $('#user-name').val();
        $.ajax({
            url: '/user/proname/',
            dataType: 'json',
            type: 'PATCH',
            data: {'name': name},
            success: function (msg) {
                if (msg.code == '1008') {
                    $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>' + msg.msg)
                    $('.error-msg').show()
                }
            },
            error: function (msg) {
                alert('请求失败')
            }
        })
        return false;
    })

})


