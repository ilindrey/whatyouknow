$(document).ready(function () {
    $('#avatar_file_input')
        .dimmer({
            on: 'hover'
        });
});

$('#upload_avatar_button').on('click', function ()
{
    $('#id_avatar').click();
});

$('#remove_avatar_button').on('click', function (e)
{
    e.preventDefault();
    $('body').modal({
        closable: false,
        class: 'mini',
        content: 'Are you sure you want to reset your current avatar?',
        actions: [{
            text: 'Cancel',
            class: 'cancel'
        },  {
            text: 'OK',
            class: 'primary ok'
        }],
        onApprove: function () {
            $('#avatar-clear_id').click();
        }
    }).modal('show');
});