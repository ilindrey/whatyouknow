$(() => {
    let $avatarForm = null;
    let $feedForm = null;
    let $avatarSegment = $('#avatar_segment');
    let $feedSegment = $('#feed_segment');
    let avatarFormUrl = $avatarSegment.data('avatar-form-url');
    let feedFormUrl = $feedSegment.data('feed-form-url');

    $(document).ready(() => {

        $.ajax({
            type: 'get',
            url: avatarFormUrl,
            // data: $(this).serialize(),
            success: function (result) { // on success..
                $avatarSegment.append(result);
                $avatarForm = $('#avatar_form');
                $avatarForm.form();
            },
            error: function (xhr, ajaxOptions, thrownError) { // on error..
                $('body')
                    .toast({
                        class: 'error',
                        message: xhr.errorText
                    });
                console.log(xhr.errorText);
            }
        });


        $.ajax({
            type: 'get',
            url: feedFormUrl,
            // data: $(this).serialize(),
            success: function (result) { // on success..
                $feedSegment.append(result);
                $feedForm = $('#feed_form');
                $feedForm.form();
            },
            error: function (xhr, ajaxOptions, thrownError) { // on error..
                $('body')
                    .toast({
                        class: 'error',
                        message: xhr.errorText
                    });
                console.log(xhr.errorText);
            }
        });


        $('#profile_form').form();
    });

    $(document).on('change', '#id_avatar', () => {
        if ($avatarForm)
        {
            $avatarForm.submit();
        }
    });

    $(document).on('change', '#avatar-clear_id', () => {
        if ($avatarForm)
        {
            $avatarForm.submit();
        }
    });
})