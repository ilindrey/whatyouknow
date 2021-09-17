
$(document).on('click', '#back_to_editing', function (e) {
    e.preventDefault();
    runAction($(this), false);
});


$(document).on('click', '#send_to_moderation', function (e) {
    e.preventDefault();
    runAction($(this), true);
});

function runAction(button, sendToModeration = false)
{
    const actionUrl = button.data(keyActionUrl);
    let deferred = $.get(actionUrl);
    deferred.done(function (responseText) {
        // let $content = $(keyContent);
        if ($content) {
            $content.html(responseText);
            setCurrentUrl();
        }
    });
    deferred.fail(function (xhr, ajaxOptions, thrownError) {
        showErrorMessage(xhr, ajaxOptions, thrownError);
    });
}