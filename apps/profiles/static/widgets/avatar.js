$(document).ready(() => {
    $('#avatar_file_input')
        .dimmer({
            on: 'hover'
        });
});

$(document).on('click', '#upload_avatar_button', () =>
{
    $('#id_avatar').click();
});

$(document).on('click', '#remove_avatar_button', () =>
{
    $('#avatar_call_remove').modal({
        closable: false,
        onApprove: function () {
            $('#avatar-clear_id').click();
    }
    }).modal('show');
});