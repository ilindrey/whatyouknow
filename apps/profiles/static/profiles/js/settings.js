
safeWrap();

function safeWrap() {

    let $currentForm,
        $profileMenu,
        $profileMenuItems,
        $profileInteractionArea,
        $loader,
        basePathnameURL,
        currentUrl,
        currentTab;

    const idProfileMenu = '#profile_menu',
        idInteractionArea = '#interaction_area',
        keyProfileMenuItems = idProfileMenu + ' .item',
        keyCurrentUsername = 'current-username',
        keyCurrentTab = 'current-tab',
        keyBasePathnameUrl = 'base-pathname-url';


    $(document).ready(function () {

        $profileMenu = $(idProfileMenu);
        $profileInteractionArea = $(idInteractionArea);
        $profileMenuItems = $(keyProfileMenuItems);
        $loader = $('.loader').closest('.ui.segment');

        hideLoader();

        basePathnameURL = $profileMenu.data(keyBasePathnameUrl);
        currentTab = $profileMenu.data(keyCurrentTab);

        if (currentTab) {
            for (let i = 0; i < $profileMenuItems.length; i++) {
                let $item = $($profileMenuItems[i]);
                if ($item.data('value') == currentTab) {
                    $item.click();
                    break;
                }
            }
        }
        else {
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

        $.ajax({
            type: 'get',
            url: currentUrl,
            beforeSend: function (jqXHR, settings) {
                showLoader();
            },
            success: function (responseText) {
                updateSegment(responseText);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            },
            complete: function (jqXHR, textStatus) {
                hideLoader();
            },
        });
    });

    $(document).on('submit', '#edit_profile_form', function (e) {
        e.preventDefault();
        formSubmit('Profile updated!')
    });

    $(document).on('submit', '#password_change_form', function (e) {
        e.preventDefault();
        formSubmit('Feed settings updated!')
    });


    $(document).on('submit', '#edit_feed_settings_form', function (e) {
        e.preventDefault();
        formSubmit('Password updated!')
    });

    function formSubmit(successMessage = null) {
        let data, processData, contentType, enctype;

        const isEditProfileForm = $currentForm.is('#edit_profile_form');
        const formsWithFiles = isEditProfileForm;

        if (formsWithFiles) {
            data = new FormData($currentForm.get(0));
            processData = false;
            contentType = false;
        }
        else {
            data = $currentForm.serialize();
            processData = true;
            contentType = 'application/x-www-form-urlencoded; charset=UTF-8';
        }
        enctype = $currentForm.attr('enctype');

        $.ajax({
            type: 'post',
            url: currentUrl,
            data: data,
            processData: processData,
            contentType: contentType,
            enctype: enctype,
            beforeSend: function (jqXHR, settings) {
                showLoader();
            },
            success: function (responseText) {
                updateSegment(responseText, successMessage, isEditProfileForm);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            },
            complete: function (jqXHR, textStatus) {
                hideLoader();
            },
        });
    }

    function updateSegment(responseText, successMessage = null, runActionsUpdateUsername = false) {
        $profileInteractionArea.html(responseText);

        $currentForm = $profileInteractionArea.find('.ui.form');
        const isValid = $currentForm.find('.error').length === 0;

        if ($currentForm.length)
            $currentForm.form();

        if (!isValid)
            return;

        if (successMessage)
            showSuccessMessage(successMessage);

        if (runActionsUpdateUsername)
            updateUrlsWhenUsernameChanged();
    }

    function showLoader() {
        $profileInteractionArea.html('');
        $loader.show();
    }

    function hideLoader() {
        $loader.hide();
    }

    function updateUrlsWhenUsernameChanged() {
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