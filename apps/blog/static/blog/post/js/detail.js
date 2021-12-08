
safeWrap();

function safeWrap() {
    const keyContent = '#content',
        keySubContent = '#sub_content',
        keyCurUrl = 'cur-url';

    let $content,
        $subContent;

    $(document).ready(function () {
        $content = $(keyContent);
        $subContent = $content.find(keySubContent);

        setCurrentUrl();
    });

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

    function setCurrentUrl() {
        if ($subContent) {
            const curUrl = $subContent.data(keyCurUrl);
            if (curUrl) {
                const url = getURL(null, null, curUrl);
                history.replaceState(null, null, url.href);
            }
        }
    }
}