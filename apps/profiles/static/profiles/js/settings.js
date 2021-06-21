$(() => {
    let $editAvatarForm = null,
        $editProfileForm = null,
        $editFeedSettingsForm = null,
        $searchElem = null,
        $excludedFeedTagsSegment = null,
        loadExcludedFeedTagsUrl = null,
        deleteExcludedFeedTagUrl = null,
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
                $avatarSegment.html(responseText);
                $editAvatarForm = $('#avatar_form');
                $editAvatarForm.form();
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });



        $.ajax({
            type: 'get',
            url: editProfileUrl,
            success: function (responseText) {
                $profileSegment.html(responseText);
                $editProfileForm = $('#profile_form');
                $editProfileForm.form();
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
                        onChange: () => {
                            updateFeedSettings();
                        },
                    });
                });

                $searchElem.search({
                    maxResults: 10,
                    apiSettings:{
                        data: {
                            search: () => { return $searchElem.search('get value'); },
                        },
                        url: searchTagsUrl,
                    },
                    fields: {
                        title: 'name'
                    },
                    onSelect: () => {
                        updateFeedSettings();
                    },
                });

                loadExcludedFeedTags();

            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });


        $.ajax({
            type: 'get',
            url: passwordChangeUrl,
            success: function (responseText) {
                updatePasswordChangeSegment(responseText);1
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });

    });


    $(document).on('submit', '#password_change_form', function (e) {
        e.preventDefault();
        let deferred = $.post(passwordChangeUrl, $(this).serialize());
        deferred.done(function (responseText) {
            updatePasswordChangeSegment(responseText);
        });
        deferred.fail(function (xhr, ajaxOptions, thrownError) {
            showErrorMessage(xhr, ajaxOptions, thrownError);
        });
    });

    function updatePasswordChangeSegment(responseText)
    {
        $passwordChangeSegment.html(responseText);
        let form = $passwordChangeSegment.find('#password_change_form');
        if(form.length)
        {
            form.form();
        }
        $passwordChangeSegment.first().scrollIntoView({block: 'start'});
    }


    $(document).on('change', '#id_avatar', () => {
        if ($editAvatarForm)
        {
            $editAvatarForm.submit();
        }
    });

    $(document).on('change', '#avatar-clear_id', () => {
        if ($editAvatarForm)
        {
            $editAvatarForm.submit();
        }
    });

    $(document).on('click', '#tags .label .icon', function () {
        $.ajax({
            type: 'post',
            url: deleteExcludedFeedTagUrl,
            data: {
                csrfmiddlewaretoken: $editFeedSettingsForm.find('input[name="csrfmiddlewaretoken"]').val(),
                tag: $(this).closest('.label').data('tag-name')
            },
            success: function (responseText) {
                $excludedFeedTagsSegment.html(responseText);
                showSuccessMessage('Feed settings updated!');
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });
    });


    function updateFeedSettings()
    {
        $.ajax({
            type: 'post',
            url: editFeedSettingsUrl,
            data: $editFeedSettingsForm.serialize(),
            success: function (responseText) {
                $searchElem.search('set value', null);
                $excludedFeedTagsSegment.html(responseText);
                showSuccessMessage('Feed settings updated!');
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });
    }

    function loadExcludedFeedTags()
    {
        $.ajax({
            type: 'get',
            url: loadExcludedFeedTagsUrl,
            success: function (responseText) {
                $excludedFeedTagsSegment.html(responseText);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });
    }

    function showSuccessMessage(text)
    {
        $('body')
            .toast({
                class: 'success',
                message: text
            });
        console.log(text);
    }

    function showErrorMessage(xhr, ajaxOptions, thrownError)
    {
        let error_message = xhr.status + ' ' + xhr.statusText;
        $('body')
            .toast({
                class: 'error',
                message: error_message
            });
        console.log(error_message);
    }
})