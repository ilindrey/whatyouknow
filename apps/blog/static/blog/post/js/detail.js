
safeWrap();

function safeWrap() {
    $(document).on('click', '#tags .item a', function (e) {
        e.preventDefault();

        let $element = $(this);

        let href, value, url;

        href = $element.attr('href');
        value = $element.data('value');

        url = getURL(null, null, href);
        url = setParamURL('tag', value, url.href);

        location = url;
    });

    $(document).on('click', '#share_link', function (e) {
        e.preventDefault();
        navigator.clipboard.writeText(window.location.href);
    });
}