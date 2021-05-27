$(document).ready(() =>
{

    const $avatarSegment = $('#avatar_segment');

    const avatarFormUrl = $avatarSegment.data('avatar-form-url');

    $.ajax({
        type: 'get',
        url: avatarFormUrl,
        // data: $(this).serialize(),
        success: function(result) { // on success..
            $avatarSegment.append(result);
        },
        error: function(xhr, ajaxOptions, thrownError) { // on error..
            $('body')
                .toast({
                    class: 'error',
                    message: xhr.errorText
                });
        }
    });
});

$(document).on('change', '#id_avatar', () =>
{
    $('#avatar_form').submit();
})

$(document).on('change', '#avatar-clear_id', () =>
{
    $('#avatar_form').submit();
})

// $(document).on('submit', '#avatar_form', function () {
//
//     const $avatarSegment = $('#avatar_segment');
//
//     const avatarFormUrl = $avatarSegment.data('avatar-form-url');
//
//     $.ajax({
//         type: $(this).attr('method'),
//         url: avatarFormUrl,
//         data: $(this).serialize(),
//         success: function(result) { // on success..
//             // $('#avatar_segment').html(result);
//             $('body')
//                 .toast({
//                     class: 'success',
//                     message: 'Avatar saved'
//                 });
//         },
//         error: function(xhr, ajaxOptions, thrownError) { // on error..
//             $('body')
//                 .toast({
//                     class: 'error',
//                     message: xhr.errorText
//                 });
//         }
//     });
// });