
safeWrap();

function safeWrap()
{
    const keyContent = '#content',
        keyStepContent = '#step_content',
        keyWriteForm = '#edit_post_form',
        keyCurUrl = 'cur-url',
        keyActionUrl = 'action-url';

    let $content = null,
        $stepContent = null,
        $writeForm = null;

    $(document).ready(function () {
        $content = $(keyContent);
        $stepContent = $content.find(keyStepContent);
        initWriteForm();
    });

    $(document).on('click', '#save_as_draft_button', function (e) {
        e.preventDefault();
        sendWriteForm(true);
    });


    $(document).on('click', '#look_at_preview_button', function (e) {
        e.preventDefault();
        sendWriteForm(false);
    });


    $(document).on('click', '#back_to_editing', function (e) {
        e.preventDefault();
        runAction($(this), false);
    });


    $(document).on('click', '#send_to_moderation', function (e) {
        e.preventDefault();
        runAction($(this), true);
    });

    function sendWriteForm(save_as_draft = false) {
        let form = $writeForm.get(0);
        let data = new FormData(form);
        data.append('save_as_draft', save_as_draft);

        $.ajax({
            type: 'post',
            url: form.action,
            data: data,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: function (responseText) {
                if ($content) {
                    $content.html(responseText);
                    $stepContent = $content.find(keyStepContent);
                    if (save_as_draft) {
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
        let deferred = $.get(actionUrl, {'send_to_moderation': sendToModeration});
        deferred.done(function (responseText) {
            if ($content)
            {
                $content.html(responseText);
                $stepContent = $content.find(keyStepContent);
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
        if ($stepContent) {
            $writeForm = $stepContent.find(keyWriteForm);
            if ($writeForm)
            {
                $writeForm.form();
            }
        }
    }

    function setCurrentUrl() {
        if ($stepContent) {
            const curUrl = $stepContent.data(keyCurUrl);
            if (curUrl) {
                const url = getURL(null, null, curUrl);
                history.replaceState(null, null, url.href);
            }
        }
    }
}