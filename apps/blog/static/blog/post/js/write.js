$(() => {
    const keyContent = '#content',
        keyStepContent = '#step_content',
        keyWriteForm = '#edit_post_form',
        keyCurUrl = 'cur-url',
        keyActionUrl = 'action-url';

    let $content = null,
        $writeForm = null;

    $(document).ready(function () {
        $content = $(keyContent);
        initWriteForm();
    });

    $(document).on('click', '#save_as_draft_button', function (e) {
        e.preventDefault();
        sendWriteForm(false);
    });


    $(document).on('click', '#look_at_preview_button', function (e) {
        e.preventDefault();
        sendWriteForm(true);
    });


    $(document).on('click', '#back_to_editing', function (e) {
        e.preventDefault();
        runAction($(this), false);
    });


    $(document).on('click', '#send_to_moderation', function (e) {
        e.preventDefault();
        runAction($(this), true);
    });

    function sendWriteForm(preview = false) {
        let form = $writeForm.get(0);
        let data = new FormData(form);
        data.append('preview', preview);
        data.append('draft', true);

        $.ajax({
            type: 'post',
            url: form.action,
            data: data,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: function (responseText) {
                // let $content = $(keyContent);
                if ($content) {
                    $content.html(responseText);
                    if (!preview) {
                        initWriteForm();
                    }
                    setCurrentUrl();
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            }
        });
    }

    function runAction(button, sendToModeration = false) {
        const actionUrl = button.data(keyActionUrl);
        let deferred = $.get(actionUrl);
        deferred.done(function (responseText) {
            // let $content = $(keyContent);
            if ($content)
            {
                $content.html(responseText);
                if(!sendToModeration)
                {
                    initWriteForm();
                }
                setCurrentUrl();
            }
        });
        deferred.fail(function (xhr, ajaxOptions, thrownError) {
            showErrorMessage(xhr, ajaxOptions, thrownError);
        });
    }

    function initWriteForm() {
        $writeForm = $(keyWriteForm);
        if ($writeForm)
            $writeForm.form();
    }

    function setCurrentUrl() {
        let $stepContent = $(keyStepContent);
        if ($stepContent) {
            const curUrl = $stepContent.data(keyCurUrl);
            if (curUrl) {
                let newUrl = new URL(window.location.origin + curUrl);
                history.replaceState(null, null, newUrl.href);
            }
        }
    }
});