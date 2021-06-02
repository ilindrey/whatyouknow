$(() => {
    let $editAvatarForm = null,
        $editFeedSettingsForm = null,
        $searchElem = null,
        $excludedFeedTagsSegment = null,
        loadExcludedFeedTagsUrl = null,
        deleteExcludedFeedTagUrl = null,
        $avatarSegment = $('#avatar_segment'),
        $feedSegment = $('#feed_segment'),
        editAvatarUrl = $avatarSegment.data('edit-avatar-url'),
        editFeedSettingsUrl = $feedSegment.data('edit-feed-settings-url'),
        searchTagsUrl = $feedSegment.data('search-tags-url');


    $(document).ready(() => {

        $.ajax({
            type: 'get',
            url: editAvatarUrl,
            success: function (result) {
                $avatarSegment.html(result);
                $editAvatarForm = $('#avatar_form');
                $editAvatarForm.form();
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });


        $.ajax({
            type: 'get',
            url: editFeedSettingsUrl,
            success: function (result) {

                $feedSegment.html(result);
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


        $('#profile_form').form();
    });

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
            success: function (result) {
                $excludedFeedTagsSegment.html(result);
                showSuccessMessage('Feed settings updated!');
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });
    })

    function updateFeedSettings()
    {
        $.ajax({
            type: 'post',
            url: editFeedSettingsUrl,
            data: $editFeedSettingsForm.serialize(),
            success: function (result) {
                $searchElem.search('set value', null);
                $excludedFeedTagsSegment.html(result);
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
            success: function (result) {
                $excludedFeedTagsSegment.html(result);
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