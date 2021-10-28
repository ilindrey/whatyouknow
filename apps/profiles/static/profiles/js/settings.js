
safeWrap();

function safeWrap() {

    let $currentForm,
        $profileMenu,
        $profileMenuItems,
        $profileSettingsSegment,
        basePathnameURL,
        currentUrl,
        currentTab;

    const idProfileMenu = '#profile_menu',
        idProfileSettingsSegment = '#interaction_area',
        keyProfileMenuItems = idProfileMenu + ' .item',
        keyCurrentUsername = 'current-username',
        keyCurrentTab = 'current-tab',
        keyBasePathnameUrl = 'base-pathname-url';


    $(document).ready(function () {

        $profileMenu = $(idProfileMenu);
        $profileSettingsSegment = $(idProfileSettingsSegment);
        $profileMenuItems = $(keyProfileMenuItems);

        basePathnameURL = $profileMenu.data(keyBasePathnameUrl);
        currentTab = $profileMenu.data(keyCurrentTab);

        if(currentTab)
        {
            for (let i = 0; i < $profileMenuItems.length; i++)
            {
                let $item = $($profileMenuItems[i]);
                if($item.data('value') == currentTab)
                {
                    $item.click();
                    break;
                }
            }
        }
        else
        {
            $profileMenuItems.get(0).click();
        }
    });

    $(document).on('click', keyProfileMenuItems, function (e) {

        e.preventDefault();

        let $item, deferred;

        $item = $(this);
        setMenuActiveItem($profileMenuItems, $item);

        currentTab = $item.data('value');
        currentUrl = $item.data('current-url');

        $profileMenu.data(keyCurrentTab, currentTab);
        const url = getURL(null, null, basePathnameURL, currentTab);
        history.replaceState(null, null, url.href);

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