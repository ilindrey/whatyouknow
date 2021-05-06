$(document).ready(function (){

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