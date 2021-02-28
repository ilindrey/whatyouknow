$(function (){

    $(document).ready(function () {

        let obj_data = get_obj_data();
        let urls =  $('#comment_urls').data();

        $.ajax({
            type: 'get',
            url: urls.getCommentParentsList,
            data: obj_data,
            success: function(data) {
                $('#comment_list_row').append(data);
            },
            error: function(xhr, status, error) {

            }
        });

        // $.ajax({
        //     type: 'get',
        //     url: urls.getCommentHeader,
        //     data: obj_data,
        //     success: function(data) {
        //         $('#comment_header_row').append(data);
        //     },
        //     error: function(xhr, status, error) {
        //
        //     }
        // });


    });

    $(document).on('click', '.answers', function (e)
    {
        e.preventDefault();

        let answers_tag  = $(this);

        let is_show_tag = $(answers_tag).find('input');
        let answers_text_tag = $(answers_tag).find('.ui.text');

        let answers_text_text = $(answers_text_tag).text();

        let comment_template = $(this).closest('.comment');

        let is_show = $(is_show_tag).val() === 'true';

        if (is_show)
        {
            comment_template.find('.ui.comments').remove('.ui.comments');

            $(is_show_tag).val(false);
            answers_text_tag.text(answers_text_text.replace("Hide", "Show"));
        }
        else
        {

            let comment_id_tag = $(comment_template).find('input');

            if ($(comment_id_tag).attr('name') != 'comment_id')
                throw 'comment_id tag not found.'

            let comment_id = $(comment_id_tag).val();

            let obj_data =  $('#comment_obj_info').data();
            let urls =  $('#comment_urls').data();

            $.ajax({
                type: 'get',
                url: urls.getCommentChildrenList,
                data: {
                    'app_label': obj_data.appLabel,
                    'model_name': obj_data.modelName,
                    'model_pk': obj_data.modelPk,
                    'parent_id': comment_id,
                },
                success: function(data) {
                    $(comment_template).append(data);
                    $(is_show_tag).val(true);
                    answers_text_tag.text(answers_text_text.replace("Show", "Hide"));
                },
                error: function(xhr, status, error) {

                }
            });

        }
    });

    function get_obj_data()
    {
        let obj_data =  $('#comment_obj_info').data();
        return {
                'app_label': obj_data.appLabel,
                'model_name': obj_data.modelName,
                'model_pk': obj_data.modelPk,
            };
    };
    //function get_name(tag)
    //{
    //      return $(tag).attr('name')
    // };
});