$(function (){
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

            let the_url =  $(is_show_tag).attr('data-url');

            $.ajax({
                type: 'get',
                url: the_url,
                data: {
                    'parent_id': comment_id,
                },
                success: function(data) {
                    $(comment_template).append(data.comment_children);
                    $(is_show_tag).val(true);
                    answers_text_tag.text(answers_text_text.replace("Show", "Hide"));
                },
                error: function(xhr, status, error) {

                }
            });

        }
    });

   //function get_name(tag)
   //{
   //      return $(tag).attr('name')
   // };
});