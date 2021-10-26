
safeWrap();

function safeWrap() {

    const charID = '#',
        keyInfoComments = 'info-comments',
        keyCommentsListRow = 'comment-list-row',
        keyEditCommentForm = 'edit_comment_form',
        keyCancelEditCommentButton = 'cancel_edit_comment_button',
        idInfoComments = charID + keyInfoComments,
        idCommentsListRow = charID + keyCommentsListRow,
        idEditCommentForm = charID + keyEditCommentForm,
        idCancelEditCommentButton = charID + keyCancelEditCommentButton;

    let $infoComments, $commentListRow, $loader, infoCommentsData,  objParams, urls;

    $(document).ready(function () {

        $infoComments = $(idInfoComments);
        $commentListRow = $(idCommentsListRow);

        $loader = $infoComments.find('.loader').closest('.segment');

        infoCommentsData = $infoComments.data();

        objParams = getObjParams();
        urls = getUrls();

        $.ajax({
            type: 'get',
            url: urls.urlCommentList,
            data: objParams,
            beforeSend: function () {
                $commentListRow.html('');
                $loader.show();
            },
            success: function (responseText) {
                $commentListRow.html(responseText);
            },
            complete: function () {
                $loader.hide();

                const keyCommentParams = 'comment';
                const url = new URL(window.location);
                const param = url.searchParams.get(keyCommentParams);

                if (param) {
                    let comment = $('#comment_' + param);
                    if (comment.length) {
                        comment[0].scrollIntoView({block: 'start'});
                        const url = deleteParamURL(keyCommentParams);
                        history.pushState(null, null, url.href);
                    }
                }
            }
        });
    });

    $(document).on('click', '.href', function (e)
    {
        e.preventDefault();
        navigator.clipboard.writeText(this.href);
    });

    $(document).on('click', '#add_comment', function (e)
    {
        actionAddReplyEditCommentHandler(e, 'add', this);
    });

    $(document).on('click', '.comments .comment .reply', function (e)
    {
        actionAddReplyEditCommentHandler(e, 'reply', this);
    });

    $(document).on('click', '.comments .comment .edit', function (e)
    {
        actionAddReplyEditCommentHandler(e, 'edit', this);
    });

    $(document).on('click', idCancelEditCommentButton, function (e)
    {
        e.preventDefault();

        let $form = $(idEditCommentForm);
        if($form.length) {
            $form.remove();
        }
    });

    $(document).on('submit', idEditCommentForm, function (e) {

        e.preventDefault();

        let $form = $(this);
        if(!$form.length)
            return;

        let actionURL = $form.attr('action');

        let actionType = $form.data('action-type');
        let targetID = $form.data('target-id');

        let formData = new FormData(this);
        formData.append('action_url', actionURL);
        formData.append('action_type', actionType);
        formData.append('target_id', targetID);
        formData.append('app_label', objParams.app_label);
        formData.append('model_name', objParams.model_name);
        formData.append('model_pk', objParams.model_pk);

        $.ajax({
            type: 'post',
            url: actionURL,
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function () {
                $('#cancel_edit_comment_button').addClass('disabled');
                $form.addClass('loading');
            },
            success: function (responseText) {

                if (responseText.includes(keyEditCommentForm))
                {
                    let $comment = $form.closest('.comment');
                    outputEditCommentForm(responseText, actionType, $comment);
                }
                else
                {
                    $form.remove();
                    $commentListRow.html(responseText);
                }
            },
            complete: function () {
                if($form.length)
                {
                    $('#cancel_edit_comment_button').removeClass('disabled');
                    $form.removeClass('loading');
                }
            }
        });

    });

    function actionAddReplyEditCommentHandler(e, actionType, element)
    {
        e.preventDefault();

        let cancelButton = $(idCancelEditCommentButton);
        if(cancelButton.length) {
            cancelButton.click();
        }

        let $element = $(element);
        let $comment = $element.closest('.comment');

        let url = $element.data('action-url');
        let id = $comment.data('id');

        let params = {}
        params.action_type = actionType;
        params.action_url = url;
        if(id)
            params.target_id = id;
        Object.assign(params, objParams);

        $.ajax({
            type: 'get',
            url: url,
            data: params,
            success: function (responseText) {
                outputEditCommentForm(responseText, actionType, $comment);
            },
        });
    };

    function outputEditCommentForm(responseText, actionType, $comment)
    {
        let $form = $(idEditCommentForm);
        if($form.length) {
            $form.remove();
        }
        if(actionType === 'add')
        {
            $commentListRow.prepend(responseText);
        }
        else
        {
            let descendant_comments = $comment.find('.comments').first();
            if(descendant_comments.length)
            {
                descendant_comments.before(responseText);
            }
            else
            {
                $comment.append(responseText);
            }
        }
        $form = $(idEditCommentForm);
        if($form.length) {
            $form.form();
        }
    };

    function getObjParams() {
        return {
            'app_label': infoCommentsData.paramAppLabel,
            'model_name': infoCommentsData.paramModelName,
            'model_pk': infoCommentsData.paramModelPk,
        };
    };


    function getUrls() {
        return {
            'urlCommentList': infoCommentsData.urlCommentList,
        };
    };
}