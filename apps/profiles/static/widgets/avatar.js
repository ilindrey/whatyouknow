$(document).ready(() => {
    $('.ui.image')
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
    $('#avatar-clear_id').click();
});