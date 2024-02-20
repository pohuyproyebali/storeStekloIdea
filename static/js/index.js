$(function ($) {
    var windowWidth = $(window).width();
    var windowHeight = $(window).height();

    $(window).resize(function () {
        if (windowWidth != $(window).width() || windowHeight != $(window).height()) {
            location.reload();
            return;
        }
    });
});

window.onload = function () {
    $('body').removeClass('preload__body')
    $preloader = $('.preloader')
    $preloader.addClass('preloader__hidden')
    setTimeout(function () {
        $preloader.addClass('preloader__none')
    }, 950)

    $(document).ready(function () {
        $('.product__slide__block').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            asNavFor: '.product__subslide__block',
            arrows: true,
            fade: true,
            adaptiveHeight: true,
            focusOnSelected: true
        });

        $('.product__subslide__block').slick({
            arrows: false,
            draggable: false,
            asNavFor: '.product__slide__block',
            centerMode: false,
            dots: false,
            variableWidth: true,
            focusOnSelect: true
        });

        $('.mirror-show').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            asNavFor: '.mirror__nav',
            arrows: false,
            fade: true,
            adaptiveHeight: true
        });
        $('.mirror__nav').slick({
            arrows: true,
            asNavFor: '.mirror-show',
            centerMode: true,
            slidesToShow: 3,
            focusOnSelect: true,
            variableWidth: true,
            responsive: [{
                breakpoint: 510,
                settings: {
                    arrows: false,
                    centerMode: true,
                }
            }]
        });

        $('.projects__slider').slick({
            fade: true,
            draggable: false,
            swipe: false
        });

        // $('.parallax__slick').slick({
        //     fade: false,
        //     draggable: true,
        //     swipe: true,
        //     arrows: false,
        //     infinite: false,
        //     variableWidth: true,
        //     slidesToShow: 2
        // });

        $('.image-show__slider').slick({
            slidesToShow: 1,
            variableWidth: true,
            infinite: false,
        });

        $('.projects-slide__images').slick({
            draggable: true,
            swipe: true,
            slidesToShow: 1,
            arrows: true,
            variableWidth: true,
            centerMode: true,
            infinite: false,

            mobileFirst: true,
            responsive: [{
                breakpoint: 1200,
                settings: 'unslick'
            }]
        });

        $('.header__burger, .burger__nav__link').click(function (event) {
            $('.header__burger, .header__burger__block, .header__nav, body').toggleClass('main__active');
        });

        $(window).on("scroll", function () {
            setTimeout(function () {
                $('.header__burger, .header__burger__block, .header__nav, body').removeClass('main__active');
            }, 500);
        });

        // $('#payment').on('change', function(e, checked){
        //     $('#blockToToggle')[checked?'show':'hide']();
        //   });

        $('.sort-goods__item').click(function (event) {
            $(this).toggleClass('active');
            $(this).next('.sort-goods__content').toggleClass('active').slideToggle(300, 'linear');
        });

        $('.v2').click(function (event) {
            $('.goods__item, .goods__block, .goods-item__img, .goods-item__name, .buy__cost, .buy__cost-mobile, .goods-line, .cart, .cart__txt-mobile, .goods-item__buy').addClass('active')
            $('.filters__mobile').removeClass('active');
            $('body').removeClass('active')
        });

        if ($(window).width() < 650) {
            $('.goods__item, .goods__block, .goods-item__img, .goods-item__name, .buy__cost, .buy__cost-mobile, .goods-line, .cart, .cart__txt-mobile, .goods-item__buy').addClass('active')
        }


        $('.v1').click(function (event) {
            $('.goods__item, .goods__block, .goods-item__img, .goods-item__name, .buy__cost, .buy__cost-mobile, .goods-line, .cart, .cart__txt-mobile, .goods-item__buy').removeClass('active')
            $('.filters__mobile').removeClass('active');
            $('body').removeClass('active')
        });

        $('.pagination__item').click(function (event) {
            $('.pagination__item').removeClass('active');
            $(this).addClass('active');
        });

        $('.pagination__arrows.next').click(function (event) {
            $('.pagination__item.active').next('.pagination__item').addClass('active')
            $('.pagination__item.active').prev().removeClass('active')
        });

        $('.pagination__arrows.next.first').click(function (event) {
            $('.pagination__item').removeClass('active')
            $('.pagination__item').last().addClass('active')
        });

        $('.pagination__arrows.prev').click(function (event) {
            $('.pagination__item.active').prev('.pagination__item').addClass('active')
            $('.pagination__item.active').next().removeClass('active')
        });

        $('.pagination__arrows.prev.first').click(function (event) {
            $('.pagination__item').removeClass('active')
            $('.pagination__item').first().addClass('active')
        });

        $('.goods__sort__choose, .sort__btn-m').click(function (event) {
            $(this).toggleClass('active');
            $('.goods__sort__block').toggleClass('active');
        });

        $('.filter-item__txt').click(function (event) {
            $(this).siblings('.filter-mobile__open').slideToggle(300, 'linear');
        });

        $('.filter__btn, .filter-close__btn').click(function (event) {
            $('.filters__mobile').toggleClass('active');
            $('body').toggleClass('active')
        });

        $(window).on("scroll", function () {

            $('.filters__mobile').removeClass('active');

        });

        $('.cart__link__block').click(function (event) {
            $('.cart__block').toggleClass('active');
            $('body').toggleClass('active-cart')
        });

        $('.cart-header__close.cart-close').click(function (event) {
            $('.cart__block').removeClass('active');
            $('body').removeClass('active-cart')
        });

        $('.order-m__btn').click(function (event) {
            $('.cart__order').addClass('active');
        });

        $('.cart-header__close.order-close').click(function (event) {
            $('.cart__order').removeClass('active');
        });

        $('.question').click(function (event) {
            $(this).find('.question__txt').toggleClass('active').slideToggle(300, 'linear');
            $(this).find('.question__arrow').toggleClass('active');
        });

        $('.goods__sort__radio').click(function (event) {

            $('.goods__sort__radio').each(function () {
                $('.goods__sort__radio').prop('checked', false)
            });

            $(this).prop('checked', true);

            var text = $(this).siblings().find('p').text();

            $('.goods__sort-value').text(text);

            setTimeout(function () {
                $('.goods__sort__block').removeClass('active');
            }, 200);

        });



        $window = $(window);
        $headerNav = $('.popular-mirrors');
        $headerScrollUp = $headerNav.offset().top;
        $headerHeight = $('.header').outerHeight();

        $window.scroll(function () {
            if ($window.scrollTop() + $headerNav.height() > $headerScrollUp + $headerNav.height()) {
                $('.header__nav-block').addClass('fixed')
                $('.up__btn').addClass('fixed')
                $('.header').css({
                    height: '' + $headerHeight + 'px'
                })
            }
            else {
                $('.header__nav-block').removeClass('fixed')
                $('.up__btn').removeClass('fixed')
                $('.header').css({
                    height: 'max-content'
                })
            }

            if (scrollDirection == 1) {
                $('.header__nav-block').removeClass('fixed')
                $('.header').css({
                    height: 'max-content'
                })
            }
        });

        $('.up__btn').click(function () {
            $('html, body').animate({ scrollTop: 0 }, 300);
            return false;
        });

        $parallaxTitle = $('.img-wrapper__title')
        $parallaxFor = $parallaxTitle.length

        for (i = 0; i < $parallaxFor; i++) {
            if ($($parallaxTitle[i]).text() < 10) {
                $($parallaxTitle[i]).text('0' + $($parallaxTitle[i]).text())
            }
        }

        $('.img__wrapper').last().addClass('img__wrapper-last')

        $('.parallax__arrow').last().addClass('d-none')

        var lastScrollTop = 0;
        $(window).scroll(function (event) {
            var st = $(this).scrollTop();
            if (st > lastScrollTop) {

                scrollDirection = 0;
            } else {
                scrollDirection = 1;
            }
            lastScrollTop = st;
        });

        $(function () {
            if ($(window).width() > 514) {
                scrollActive = true;
                scrollDirection = 0;

                $muchElements = $('.img__wrapper').length;

                $('.img__wrapper').last().addClass('img__wrapper-last')


                $nav = $('.parallax__block');
                $scrollBlock = $('.horizontal-scroll__wrapper');
                $fixedWidth = $nav.outerWidth();

                $scrollTotalWidth = $('.img__wrapper').width() * ($muchElements - 1) + $('.img__wrapper-last').width() + 180;

                $koefScroll = 100 / ($scrollTotalWidth / 100)

                $koefWidth = 100 / ($scrollTotalWidth / $nav.width())
                $parallaxStatusBkg = $('.status__bkg').width();
                $statusLineWidth = $parallaxStatusBkg / 100 * $koefWidth

                $('.status__line').css({
                    width: '' + $statusLineWidth + 'px',
                });


                $window = $(window);

                $windowBottom = $window.height();

                $window.scroll(function () {
                    if ($nav.hasClass('fixed') == false) {
                        $h = $nav.offset().top;
                    }

                    $scrollUp = $nav.offset().top;
                    $muchLeft = ($scrollTotalWidth - $window.width()) / $muchElements;
                    $muchPadding = $muchLeft + 100;
                    $parallaxFixed = $('.parallax__fixed');
                    $parallaxFixed.css('padding-bottom', $muchPadding * $muchElements + 'px')


                    if (scrollDirection == 1 && $window.scrollTop() + $nav.height() + 200 < $scrollUp + 200 + $nav.height()) {
                        scrollActive = true
                        $nav.css({
                            transform: 'translateY(0px)',
                        });
                        $h = $nav.offset().top;
                    }
                    if (scrollActive) {

                        var scrollMuch = $window.scrollTop() - $h;
                        $koefScrollLine = ($parallaxStatusBkg / 100) * $koefScroll
                        $scrollMuchKoef = (100 / ($koefScrollLine / 100)) / 100
                        $scrollMuchLine = scrollMuch / $scrollMuchKoef

                        if ($nav.hasClass('fixed') == true) {
                            $scrollBlock.css({
                                transform: 'translateX(-' + scrollMuch + 'px)'
                            });

                            if ($scrollMuchLine + $statusLineWidth < $parallaxStatusBkg) {
                                $('.status__line').css({
                                    transform: 'translateX(' + $scrollMuchLine + 'px)'
                                });
                            }
                        }

                        if ($window.scrollTop() > $h) {
                            $nav.addClass('fixed');
                        }
                        else {
                            $nav.removeClass('fixed');
                        }


                        $muchScrollBottom = $muchPadding * $muchElements - 1000

                        if (scrollMuch > $muchLeft * $muchElements && scrollDirection == 0) {
                            $nav.removeClass('fixed');
                            $nav.css({
                                transform: 'translateY(' + $muchScrollBottom + 'px)'
                            });

                            scrollActive = false;
                        }
                    }
                });
            }
        });

        var count = 1;

        $('.count-plus').click(function (event) {
            count += 1;
            $('.count').text(count)
        });


        $('.count-minus').click(function (event) {
            if ($('.count').text() == '1')
                return
            count -= 1;
            $('.count').text(count)
        });


    });

}