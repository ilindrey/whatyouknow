
safeWrap();

function safeWrap()
{
    const keyContent = '#content',
        keyStepContent = '#step_content',
        keyWriteForm = '#edit_post_form',
        keyCurUrl = 'cur-url',
        keyCurAction = 'cur-action',
        keyActionUrl = 'action-url';

    let $content = null,
        $stepContent = null,
        $writeForm = null;

    $(document).ready(function () {
        $content = $(keyContent);
        $stepContent = $content.find(keyStepContent);
        const curAction = $stepContent.data(keyCurAction);
        if(curAction === 'create' || curAction === 'edit') {
            initWriteForm();
        }
    });

    $(document).on('click', '#save_as_draft_button', function (e) {
        e.preventDefault();
        sendWriteForm('edit');
    });


    $(document).on('click', '#look_at_preview_button', function (e) {
        e.preventDefault();
        sendWriteForm('preview');
    });


    $(document).on('click', '#back_to_editing', function (e) {
        e.preventDefault();
        runAction($(this), 'edit');
    });


    $(document).on('click', '#done', function (e) {
        e.preventDefault();
        runAction($(this), 'done');
    });

    function sendWriteForm(nextAction) {
        let form = $writeForm.get(0);
        let data = new FormData(form);
        data.append('next_action', nextAction);

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
                    if (nextAction === 'edit') {
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

    function runAction(button, nextAction) {
        const actionUrl = button.data(keyActionUrl);
        let deferred = $.get(actionUrl, {'next_action': nextAction});
        deferred.done(function (responseText) {
            if ($content)
            {
                $content.html(responseText);
                $stepContent = $content.find(keyStepContent);
                if(nextAction === 'edit')
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