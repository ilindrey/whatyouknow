$(function (){

    const infoCommentsTag = $('#info-comments');
    const commentListRowTag = $('#comment-list-row');


    const infoCommentsData = infoCommentsTag.data();

    const objParams = getObjParams();
    const urls = getUrls();


    commentListRowTag.infiniteScroll({
        path: function ()
        {
            let url_string = getUrlWithParamsAsString(urls.urlParentCommentList, objParams)
            return  url_string + '&page=' + this.pageIndex;
        },
        append: '.comment',
        status: '#loader',
        checkLastPage: false,
        prefill: true,
        history: false,
        debug: true
    });


    $(document).on('click', '.answers', function (e)
    {
        e.preventDefault();

        let answersTag = $(this);
        let answersTextTag = answersTag.find('.ui.text');
        let answersTextString = $(answersTextTag).text();

        const isShowDataKey = 'is-show';
        const isShow = answersTag.data(isShowDataKey) === true;

        let nodeCommentTag = answersTag.closest('.comment');

        if(isShow)
        {
            const uiCommentsTagKey = '.ui.comments';
            nodeCommentTag.find(uiCommentsTagKey).remove(uiCommentsTagKey);

            answersTag.data(isShowDataKey, false);
            answersTextTag.text(answersTextString.replace("Hide", "Show"));
        }
        else
        {
            let params = objParams;
            params['parent_id'] = nodeCommentTag.data('node-id');

            const loaderDescendantTag = $('#loader').clone().attr('id', 'loader-descendant');

            $.ajax({
                type: 'get',
                url: urls.urlDescendantCommentList,
                data: params,
                beforeSend: function ()
                {
                    nodeCommentTag.append(loaderDescendantTag);
                },
                success: function (result)
                {
                    nodeCommentTag.append(result);
                    answersTag.data(isShowDataKey, true);
                    answersTextTag.text(answersTextString.replace("Show", "Hide"));
                },
                complete: function ()
                {
                    loaderDescendantTag.remove();
                }
            });

        };
    });



    function getUrlWithParamsAsString(url, params)
    {
        let string_of_params = '';
        for (let [key, value] of Object.entries(params))
        {
            string_of_params += (string_of_params ? '&' : '?') + key + '=' + value
        }
        return url + string_of_params;
    }


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
            'urlParentCommentList': infoCommentsData.urlParentCommentList,
            'urlDescendantCommentList': infoCommentsData.urlDescendantCommentList,
        };
    };

});