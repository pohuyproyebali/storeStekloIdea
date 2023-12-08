$(document).ready(function () {
    $('.header__burger').click(function (event) {
        $('.header__burger, .header__burger__block').toggleClass('main__active');
    });

    $('.sort-goods__item').click(function (event) {
        $(this).toggleClass('active');
    });

    $('.goods__sort__choose').click(function (event) {
        $(this).toggleClass('active');
        $('.goods__sort__block').toggleClass('active');
    });

    $('.goods__sort__radio').click(function (event) {

        $('.goods__sort__radio').each(function () {
            $('.goods__sort__radio').prop('checked', false)
        });

        $(this).prop('checked', true);

        var text = $(this).siblings().find('p').text();

        $('.goods__sort-value').text(text);

        // $('.goods__sort__name').each(function () {
        //     $('.goods__sort-value').empty();
        //     var text = $(this).text();
        //     console.log($(this))
        //     $('.goods__sort-value').append(text);
        // });

        setTimeout(function () {
            $('.goods__sort__block').removeClass('active');
        }, 200);

    });

    $("body").on("scroll", function () {
        setTimeout(function () {
            $('.header__burger, .header__burger__block').removeClass('main__active');
        }, 500);
    });

    $('.mirror-show').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        asNavFor: '.mirror__nav',
        arrows: false,
        fade: true,
        adaptiveHeight: true,
        responsive: [{
            breakpoint: 510,
            settings: {
                fade: false
            }
        }]
    });
    $('.mirror__nav').slick({
        arrows: true,
        asNavFor: '.mirror-show',
        centerMode: false,
        slidesToShow: 3,
        variableWidth: true,
        responsive: [{
            breakpoint: 510,
            settings: {
                arrows: false,
                centerMode: true,
            }
        }]
    });
});






