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


                },
                complete: function ()
                {
                    console.log('pre - ' + answersTag.data(isShowDataKey));

                    answersTag.data(isShowDataKey, true);

                    console.log('after - ' + answersTag.data(isShowDataKey));
                    answersTextTag.text(answersTextString.replace("Show", "Hide"));

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






















































































































// $(function (){
//
//     let objParams = getObjParams();
//     let urls = getUrls();
//
//
//     $(document).ready(function () {
//
//         let params = objParams;
//         params['page'] = 1;
//
//
//         $.get(urls.urlCommentList, params, (data) => {
//             $('#comment-list-row').html(data);
//         });
//
//
//         // $(document).one("scroll", function() {
//         //
//         //       let commentsTag  = $('.ui.threaded.comments');
//         //
//         //       commentsTagOffset = commentsTag.offset().top;
//         //
//         // });
//         //
//         //   $(document).on('scroll', (e) =>
//         //   {
//         //       e.preventDefault();
//         //
//         //       let win = $(window);
//         //       let commentsTag  = $('.ui.threaded.comments');
//         //
//         //       // let commentsTagOffset = commentsTag.offset();
//         //
//         //       let commentsTagHeight = commentsTag.height();
//         //
//         //       let commentsTagScrollBottom = commentsTagOffset + commentsTagHeight;
//         //       let scrollBottom = win.scrollTop() + win.height();
//         //
//         //       let value = commentsTagScrollBottom - scrollBottom;
//         //
//         //       if (value < 0)
//         //       {
//         //           console.log('.ui.threaded.comments scroll bottom: ' + value);
//         //           // commentsTag.append(getLoaderCode());
//         //       }
//         //       }
//         //   );
//     });
//
//     // $('.ui.threaded.comments').jscroll({
//     //     loadingHtml: getloadingHtml(),
//     //     padding: 2,
//     // });
//
//     $('.ui.threaded.comments').infiniteScroll({
//         // options
//         path: function ()
//         {
//             let url = getUrls().urlCommentList;
//         },
//         append: '.post',
//         history: false,
//     });
//
//     //
//     // $(document).on('click', '.answers', function (e)
//     // {
//     //     e.preventDefault();
//     //
//     //     let answers_tag  = $(this);
//     //
//     //     let is_show_tag = $(answers_tag).find('input');
//     //     let answers_text_tag = $(answers_tag).find('.ui.text');
//     //
//     //     let answers_text_text = $(answers_text_tag).text();
//     //
//     //     let comment_template = $(this).closest('.comment');
//     //
//     //     let is_show = $(is_show_tag).val() === 'true';
//     //
//     //     if (is_show)
//     //     {
//     //         comment_template.find('.ui.comments').remove('.ui.comments');
//     //
//     //         $(is_show_tag).val(false);
//     //         answers_text_tag.text(answers_text_text.replace("Hide", "Show"));
//     //     }
//     //     else
//     //     {
//     //
//     //         let comment_id_tag = $(comment_template).find('input');
//     //
//     //         if ($(comment_id_tag).attr('name') != 'comment_id')
//     //             throw 'comment_id tag not found.'
//     //
//     //         let comment_id = $(comment_id_tag).val();
//     //
//     //         let data =  $('#comment_obj_info').data();
//     //         let urls =  $('#comment_urls').data();
//     //
//     //
//     //         data['parent_id'] = comment_id;
//     //
//     //         $.ajax({
//     //             type: 'get',
//     //             url: urls.getCommentChildrenList,
//     //             data: data,
//     //             success: function(data) {
//     //                 $(comment_template).append(data);
//     //                 $(is_show_tag).val(true);
//     //                 answers_text_tag.text(answers_text_text.replace("Show", "Hide"));
//     //             },
//     //             error: function(xhr, status, error) {
//     //
//     //             }
//     //         });
//     //
//     //     }
//     // });
//
//     // function load_more()
//     // {
//     //     let params = get_obj_data();
//     //     let urls =  $('#comment_urls').data();
//     //     let nextPageNumber = $('#loading_comments_link').data('next-page-number');
//     //
//     //     params['page'] = nextPageNumber;
//     //
//     //     $.ajax({
//     //         type: 'get',
//     //         url: urls.urlCommentLoader,
//     //         data: params,
//     //         success: function(data) {
//     //             $('.ui.threaded.comments').append(data.html_string);
//     //         },
//     //         error: function(xhr, status, error) {
//     //
//     //         }
//     //     });
//     // };
//
//     function getUrlViaParams(url, params)
//     {
//         params = {}
//         for (let i = 0; i < params.lenght(); i++)
//         {
//
//         }
//     }
//
//     function getObjParams()
//     {
//         let data =  $('#info_comments').data();
//         return {
//             'app_label': data.paramAppLabel,
//             'model_name': data.paramModelName,
//             'model_pk': data.paramModelPk,
//         };
//     };
//
//     function getUrls()
//     {
//         let data =  $('#info_comments').data();
//         return {
//             'urlCommentList': data.urlCommentList,
//         };
//     };
//
//     function getloadingHtml()
//     {
//         return '<div className="ui basic center aligned segment" id="loader">' +
//             '<div class="ui text inline elastic primary active loader">Loading comments...</div>' +
//             '</div>';
//     };
//
//     //function get_name(tag)
//     //{
//     //      return $(tag).attr('name')
//     // };
// });