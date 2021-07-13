$(() => {
    let $editFeedSettingsForm = null,
        $searchElem = null,
        $excludedFeedTagsSegment = null,
        loadExcludedFeedTagsUrl = null,
        deleteExcludedFeedTagUrl = null,
        $settingsContent = $('#settings_content'),
        $avatarSegment = $('#avatar_segment'),
        $profileSegment = $('#profile_segment'),
        $feedSegment = $('#feed_segment'),
        $passwordChangeSegment = $('#password_change_segment'),
        editAvatarUrl = $avatarSegment.data('edit-avatar-url'),
        editProfileUrl = $profileSegment.data('edit-profile-url'),
        editFeedSettingsUrl = $feedSegment.data('edit-feed-settings-url'),
        searchTagsUrl = $feedSegment.data('search-tags-url'),
        passwordChangeUrl = $passwordChangeSegment.data('password-change-url');


    $(document).ready(function () {

        $.ajax({
            type: 'get',
            url: editAvatarUrl,
            success: function (responseText) {
                updateFormSegment(responseText, $avatarSegment, '#edit_avatar_form');
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });

        $.ajax({
            type: 'get',
            url: editProfileUrl,
            success: function (responseText) {
                updateFormSegment(responseText, $profileSegment, '#edit_profile_form');
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });

        $.ajax({
            type: 'get',
            url: passwordChangeUrl,
            success: function (responseText) {
                updateFormSegment(responseText, $passwordChangeSegment, '#password_change_form');
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });

        $.ajax({
            type: 'get',
            url: editFeedSettingsUrl,
            success: function (responseText) {

                $feedSegment.html(responseText);
                $editFeedSettingsForm = $('#edit_feed_settings_form');
                $editFeedSettingsForm.form();
                $searchElem = $('#id_search_tags_brain');
                $excludedFeedTagsSegment = $('#excluded_feed_tags_segment');
                loadExcludedFeedTagsUrl = $excludedFeedTagsSegment.data('load-excluded-feed-tags-url');
                deleteExcludedFeedTagUrl = $excludedFeedTagsSegment.data('delete-excluded-feed-tag-url');

                $('#id_categories .item .checkbox').map(function(index, item) {
                    $(item).checkbox({
                        onChange: function () {
                            $searchElem.search('set value', null);
                            updateFeedSettings();
                        },
                    });
                });

                $searchElem.search({
                    maxResults: 10,
                    apiSettings:{
                        data: {
                            search: function () { return $searchElem.search('get value'); },
                        },
                        url: searchTagsUrl,
                    },
                    fields: {
                        title: 'name'
                    },
                    onSelect: function (result, response) {
                        let query = result['name'].split("<i class=\"tag icon\"></i>").pop();
                        $searchElem.search('set value', query);
                        updateFeedSettings();
                    },
                });

                loadExcludedFeedTags();

            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });

    });


    $(document).on('change', '#id_avatar', function (e) {
        e.preventDefault();
        avatarFormSubmit();
    });

    $(document).on('change', '#avatar-clear_id', function (e) {
        e.preventDefault();
        avatarFormSubmit();
    });


    function avatarFormSubmit()
    {
        let $editAvatarForm = $('#edit_avatar_form');
        let data = new FormData($editAvatarForm.get(0));

        $.ajax({
            type: 'post',
            url: editAvatarUrl,
            data: data,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: function (responseText) {
                updateFormSegment(responseText, $avatarSegment, '#edit_avatar_form', 'Avatar updated!');
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });
    };

    $(document).on('submit', '#edit_profile_form', function (e) {
        e.preventDefault();
        formSubmit(editProfileUrl, $profileSegment, $(this), 'Profile updated!', true);
    });

    $(document).on('submit', '#password_change_form', function (e) {
        e.preventDefault();
        formSubmit(passwordChangeUrl, $passwordChangeSegment, $(this), 'Password updated!')
    });

    function formSubmit(url, segment, form, successMessage = null, runActionsUpdateUsername = false)
    {
        let deferred = $.post(url, form.serialize());
        deferred.done(function (responseText) {
            let formID = '#' + form.attr('id');
            updateFormSegment(responseText, segment, formID, successMessage, runActionsUpdateUsername);

        });
        deferred.fail(function (xhr, ajaxOptions, thrownError) {
            showErrorMessage(xhr, ajaxOptions, thrownError);
        });
    }

    function updateFormSegment(responseText, segment, formID, successMessage= null, runActionsUpdateUsername = false)
    {
        segment.html(responseText);

        let form = segment.find(formID);
        let isValid = form.find('.error').length === 0;

        if (form.length)
            form.form();

        if (!isValid)
            return;

        if (successMessage)
            showSuccessMessage(successMessage);

        if (runActionsUpdateUsername)
            updateUrlsWhenUsernameChanged();
    }

    $(document).on('click', '#tags .label .icon', function () {
        let data = {
            csrfmiddlewaretoken: $editFeedSettingsForm.find('input[name="csrfmiddlewaretoken"]').val(),
            tag: $(this).closest('.label').data('tag-name')
        };
        let deferred = $.post(deleteExcludedFeedTagUrl, data);
        deferred.done(function (responseText) {
            $excludedFeedTagsSegment.html(responseText);
            showSuccessMessage('Feed settings updated!');
        });
        deferred.fail(function (xhr, ajaxOptions, thrownError) {
            showErrorMessage(xhr, ajaxOptions, thrownError);
        });
    });


    function updateFeedSettings()
    {
        let deferred = $.post(editFeedSettingsUrl, $editFeedSettingsForm.serialize());
        deferred.done(function (responseText) {
            $searchElem.search('set value', null);
            $excludedFeedTagsSegment.html(responseText);
            showSuccessMessage('Feed settings updated!');
        });
        deferred.fail(function (xhr, ajaxOptions, thrownError) {
            showErrorMessage(xhr, ajaxOptions, thrownError);
        });
    }

    function loadExcludedFeedTags()
    {
        let deferred = $.get(loadExcludedFeedTagsUrl)
        deferred.done(function (responseText) {
            $excludedFeedTagsSegment.html(responseText);
        });
        deferred.fail(function (xhr, ajaxOptions, thrownError) {
            showErrorMessage(xhr, ajaxOptions, thrownError);
        });
    }

    function updateUrlsWhenUsernameChanged()
    {
        const keyCurrentUsername = 'current-username';

        let oldUsername = $settingsContent.data(keyCurrentUsername);
        let newUsername = $('#edit_profile_form').find('#id_username').val();

        if (oldUsername === newUsername)
            return;

        let newUrl = new URL(window.location);
        newUrl.pathname = newUrl.pathname.replace(oldUsername, newUsername);
        history.pushState(null, null, newUrl.href);

        setTimeout(() => { location.reload(); }, 1000);
    }
})