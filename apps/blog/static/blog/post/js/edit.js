$(() => {

    let $stepContent = null,
        $content = null,
        $writeForm = null,
        keyContent = '#content',
        keyStepContent = '#step_content',
        keyWriteForm = '#edit_post_form',
        keyCurUrl = 'cur-url';

    $(document).ready(function() {
        $content = $(keyContent);
        initWriteForm();
    });

    $(document).on('click', '#save_as_draft_button', function (e) {
        e.preventDefault();
        sendWriteForm(false)
    });


    $(document).on('click', '#look_at_preview_button', function (e) {
        e.preventDefault();
        sendWriteForm(true)
    });


    function initWriteForm()
    {
        $writeForm = $(keyWriteForm);
        if ($writeForm)
            $writeForm.form();
    }

    function sendWriteForm(preview = false)
    {
        let form = $writeForm.get(0);
        let data = new FormData(form);
        data.append('preview', Number(preview));
        data.append('draft', 1);

        $.ajax({
            type: 'post',
            url: form.action,
            data: data,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: function (responseText) {
                if($content)
                {
                    $content.html(responseText);
                    if (!preview)
                    {
                        initWriteForm();
                    }
                    $stepContent = $(keyStepContent);
                    const curUrl = $stepContent.data(keyCurUrl);
                    let newUrl = new URL(window.location.origin + curUrl);
                    history.pushState(null, null, newUrl.href);

                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });
    }

});

