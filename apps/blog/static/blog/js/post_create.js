$(() => {

    let stepContent = null,
        stepContentData = null,
        loader = null,
        urls = null,
        keyWriteForm = '#write_form';

    $(document).ready(function() {

        stepContent = $('#step_content');
        stepContentData = stepContent.data();
        loader = $('.loader')
        urls = getUrls();

        $.ajax({
            type: 'get',
            url: urls.postWriteUrl,
            beforeSend: function () {
                loader.show();
            },
            success: function (responseText) {
                stepContent.html(responseText);
                $(keyWriteForm).form();
            },
            complete: function () {
                loader.hide();
            }
        });

    });

    $(document).on('submit', keyWriteForm, function (e) {
        e.preventDefault();
        // let form = $(this);
        // let deferred = $.post(urls.postWriteUrl, form.serialize());
        // deferred.done(function (responseText) {
        //     if(stepContent)
        //     {
        //         stepContent.html(responseText);
        //         $(keyWriteForm).form();
        //     }
        // });
        // deferred.fail(function (xhr, ajaxOptions, thrownError) {
        //     showErrorMessage(xhr, ajaxOptions, thrownError);
        // });

        // let $editAvatarForm = $('#edit_avatar_form');
        let data = new FormData($(this).get(0));

        $.ajax({
            type: 'post',
            url: urls.postWriteUrl,
            data: data,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: function (responseText) {
                if(stepContent)
                {
                    stepContent.html(responseText);
                    $(keyWriteForm).form();
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });
    });

    function getUrls()
    {
        return {
            'postWriteUrl': stepContentData.postWriteUrl,
        };
    };
});

