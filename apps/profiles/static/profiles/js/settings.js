$(() => {
    let $editFeedSettingsForm = null,
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
                updateFormSegment(responseText, $avatarSegment, '#edit_avatar_form');
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });
    };

    $(document).on('submit', '#edit_profile_form', function (e) {
        e.preventDefault();
        formSubmit(editProfileUrl, $profileSegment, $(this));
    });

    $(document).on('submit', '#password_change_form', function (e) {
        e.preventDefault();
        formSubmit(passwordChangeUrl, $passwordChangeSegment, $(this))
        // $(this).closest('.segment').get(0).scrollIntoView({block: 'start'});
    });

    function formSubmit(url, segment, form)
    {
        let deferred = $.post(url, form.serialize());
        deferred.done(function (responseText) {
            updateFormSegment(responseText, segment, '#' + form.attr('id'));
            showSuccessMessage('Settings updated!');
        });
        deferred.fail(function (xhr, ajaxOptions, thrownError) {
            showErrorMessage(xhr, ajaxOptions, thrownError);
        });
    }

    function updateFormSegment(responseText, segment, form_id)
    {
        segment.html(responseText);
        let form = segment.find(form_id);
        if(form.length)
        {
            form.form();
        }
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

    function showSuccessMessage(text)
    {
        $('body').toast({
            class: 'success',
            message: text
        });
        console.log(text);
    }

    function showErrorMessage(xhr, ajaxOptions, thrownError)
    {
        let error_message = xhr.status + ' ' + xhr.statusText;
        $('body').toast({
            class: 'error',
            message: error_message
        });
        console.log(error_message);
    }
})