function hrefBack() {
    history.go(-1);
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {
    var info = location.search
    house_id = info.split('=')[1]
    $.get('/house/detail/' + house_id + '/', function (msg) {
        if (msg.code == 200) {
            for (var i = 0; i < msg.house_info.images.length; i++) {
                $('.swiper-wrapper').append('<li class="swiper-slide"><img src="' + msg.house_info.images[i] + '"></li>')
            }
            var mySwiper = new Swiper('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })
            $(".book-house").show();
            $('.house-title').text(msg.house_info.title)
            $('.house-price-s').text(msg.house_info.price)
            $('.landlord-pic img').attr('src', '/static/' + msg.house_info.user_avatar)
            $('.landlord-name').text('房东：' + msg.house_info.user_name)
            $('.house-info-list li').text(msg.house_info.address)
            $('.house-count').text('出租' + msg.house_info.room_count + '间')
            $('.house_acreage').text('房屋面积:'+msg.house_info.acreage+'平米')
            $('.house_unit').text('房屋户型:'+msg.house_info.unit)

            $('.book-house').attr('href', '/house/booking/?house_id=' + msg.house_info.id)
        }

    })


})

