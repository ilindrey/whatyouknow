
safeWrap();

function safeWrap()
{
    const keyContent = '#content',
        keyStepContent = '#step_content',
        keyWriteForm = '#edit_post_form',
        keyCurUrl = 'cur-url',
        keyCurAction = 'cur-action',
        keyActionUrl = 'action-url';

    let $content,
        $stepContent,
        $writeForm,
        $loader;

    $(document).ready(function ()
    {
        $content = $(keyContent);
        $loader = $content.find('.loader').closest('.segment');
        $stepContent = $content.find(keyStepContent);

        hideLoader();

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
            beforeSend: function(jqXHR, settings)
            {
                showLoader();
            },
            success: function (responseText)
            {
                loadingStepContent(responseText, nextAction);
            },
            error: function (xhr, ajaxOptions, thrownError)
            {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            },
            complete: function (jqXHR, textStatus)
            {
                hideLoader();
            },
        });
    }

    function runAction(button, nextAction)
    {
        $.ajax({
            type: 'get',
            url: button.data(keyActionUrl),
            data: {
                'next_action': nextAction
            },
            beforeSend: function(jqXHR, settings)
            {
                showLoader();
            },
            success: function (responseText)
            {
                loadingStepContent(responseText);
            },
            error: function (xhr, ajaxOptions, thrownError)
            {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            },
            complete: function (jqXHR, textStatus)
            {
                hideLoader();
            },
        });
    }

    function loadingStepContent(responseText, nextAction)
    {
        if ($content) {
            $content.html(responseText);
            $stepContent = $content.find(keyStepContent);
            if (nextAction === 'edit') {
                initWriteForm();
            }
            setCurrentUrl();
        }
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

    function showLoader()
    {
        $stepContent.html('');
        $loader.show();
    }

    function hideLoader()
    {
        $loader.hide();
    }
}