
safeWrap();

function safeWrap() {

    let $currentForm = null,
        $profileMenu = null,
        $profileMenuItems = null,
        $profileSettingsSegment = null,
        currentUrl = null;

    const keyProfileMenu = '#profile_menu',
        keyProfileMenuItems = keyProfileMenu + ' .item',
        keyProfileSettingsSegment = '#profile_settings_segment',
        keyCurrentUsername = 'current-username';


    $(document).ready(function () {
        $profileMenu = $(keyProfileMenu);
        $profileSettingsSegment = $(keyProfileSettingsSegment);
        $profileMenuItems = $(keyProfileMenuItems);

        $profileMenuItems.get(0).click();
    });

    $(document).on('click', keyProfileMenuItems, function (e) {

        e.preventDefault();

        let item, deferred;

        item = $(this);
        setMenuActiveItem($profileMenuItems, item);

        currentUrl = item.data('current-url');

        deferred = $.get(currentUrl);
        deferred.done(function (responseText) {
            updateSegment(responseText);
        });
        deferred.fail(function (xhr, ajaxOptions, thrownError) {
            showErrorMessage(xhr, ajaxOptions, thrownError);
        });
    });

    $(document).on('submit', '#edit_profile_form', function (e) {
        e.preventDefault();
        profileSubmit();
    });

    $(document).on('submit', '#password_change_form', function (e) {
        e.preventDefault();
        formSubmit('Feed settings updated!')
    });


    $(document).on('submit', '#edit_feed_settings_form', function (e) {
        e.preventDefault();
        formSubmit('Password updated!')
    });

    function profileSubmit()
    {
        let data = new FormData($currentForm.get(0));

        $.ajax({
            type: 'post',
            url: currentUrl,
            data: data,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: function (responseText) {
                updateSegment(responseText, 'Profile updated!', true);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });
    }

    function formSubmit(successMessage = null)
    {
        let deferred = $.post(currentUrl, $currentForm.serialize());
        deferred.done(function (responseText) {
            updateSegment(responseText, successMessage, false);

        });
        deferred.fail(function (xhr, ajaxOptions, thrownError) {
            showErrorMessage(xhr, ajaxOptions, thrownError);
        });
    }

    function updateSegment(responseText, successMessage= null, runActionsUpdateUsername = false)
    {
        $profileSettingsSegment.html(responseText);

        $currentForm = $profileSettingsSegment.find('.ui.form');
        let isValid = $currentForm.find('.error').length === 0;

        if ($currentForm.length)
            $currentForm.form();

        if (!isValid)
            return;

        if (successMessage)
            showSuccessMessage(successMessage);

        if (runActionsUpdateUsername)
            updateUrlsWhenUsernameChanged();
    }

    function updateUrlsWhenUsernameChanged()
    {
        let oldUsername = $profileMenu.data(keyCurrentUsername);
        let newUsername = $currentForm.find('#id_username').val();

        if (oldUsername === newUsername)
            return;

        let newUrl = new URL(window.location);
        newUrl.pathname = newUrl.pathname.replace(oldUsername, newUsername);
        history.pushState(null, null, newUrl.href);

        showInfoMessage('Wait for the page to reload...')

        setTimeout(() => { location.reload(); }, 1000);
    }
}