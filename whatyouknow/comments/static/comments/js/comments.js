$(document).ready(function() {
// $(window).on('load', function() {

    const infoCommentsTag = $('#info-comments');
    const commentListRowTag = $('#comment-list-row');
    const loader = $('#loader');

    const infoCommentsData = infoCommentsTag.data();

    const objParams = getObjParams();
    const urls = getUrls();


    $.ajax({
        type: 'get',
        url: urls.urlCommentList,
        data: objParams,
        beforeSend: function () {
            loader.show();
        },
        success: function (result) {
            commentListRowTag.append(result);
        },
        complete: function () {
            loader.hide();

            let url = new URL(window.location);

            const keyCommentParams = 'comment';
            let comment_params = url.searchParams.getAll(keyCommentParams);

            if (comment_params.length > 0) {

                let param = comment_params[0];
                let comment = $('#comment_' + param);

                if (comment.length > 0) {

                    comment[0].scrollIntoView({block: 'start'});

                    url.searchParams.delete(keyCommentParams);
                    history.pushState(null, null, url.href);

                }
            }
        }
    });



    function getObjParams()
    {
        return {
            'app_label': infoCommentsData.paramAppLabel,
            'model_name': infoCommentsData.paramModelName,
            'model_pk': infoCommentsData.paramModelPk,
        };
    };


    function getUrls()
    {
        return {
            'urlCommentList': infoCommentsData.urlCommentList,
        };
    };

});