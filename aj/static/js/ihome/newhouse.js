function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    var title = $('#house-title').val()
    var price = $('#house-price').val()

})



$.get('/house/area_facility/', function(msg){
    if(msg.code == 200){
        var area_str = ''
        var facility_str = ''
        for(var i=0; i<msg.areas.length; i++){
            area_option = '<option value=' + msg.areas[i].id +'>' + msg.areas[i].name +'</option>'
            area_str += area_option
        }
        $('#area-id').html(area_str)

        for(var j=0; j<msg.facilitys.length; j++){
            facility_li = '<li><div class="checkbox"><label>'
            facility_li += '<input type="checkbox" name="facility" value="' + msg.facilitys[j].id + '">' + msg.facilitys[j].name
            facility_li += '</label></div></li>'
            facility_str += facility_li
        }

        $('.house-facility-list').html(facility_str)
    }
})


$('#form-house-info').submit(function () {
     $.post('/house/newhouse/',$(this).serialize(), function (msg) {
         if(msg.code == 200){
            $('#form-house-info').hide();
            $('#form-house-image').show();
            $('#house-id').val(msg.house_id);
        }else{
            $('.error-msg text-center').show().find('span').html(ret_map[data.code]);
        }
     })
    // return false 取消刷新
    return false
})


$('#form-house-image').submit(function () {
    $(this).ajaxSubmit({
        url: '/house/newhouse_image/',
        type: 'post',
        dataType: 'json',
        success: function (msg) {
            if (msg.code == 200){
                $('.house-image-cons').append('<img src="'+msg.url+'"/>');
            }
        }
    })
    return false
})

