$(document).ready(function () {
     initialAvatarMenu();
});

$(document).ajaxComplete(function( event, xhr, settings ) {
  if (xhr.statusText === 'OK' && xhr.responseText.search('avatar_img') > -1)
  {
    initialAvatarMenu();
  }
});

$(document).on('ready', '#upload_avatar_button', function ()
{
    $('#avatar_img').popup({
        popup: '#edit_avatar_menu',
        position: 'top center',
        inline     : true,
        hoverable  : true,
        setFluidWidth: true,
        variation: 'wide',
        delay: {
            show: 300,
            hide: 500
        }
    });
});

$(document).on('click', '#upload_avatar_button', function ()
{
    $('#id_avatar').click();
});

$(document).on('click', '#remove_avatar_button', function (e)
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


function initialAvatarMenu()
{
    $('#avatar_img').popup({
        popup: '#edit_avatar_menu',
        position: 'top center',
        inline     : true,
        hoverable  : true,
        setFluidWidth: true,
        variation: 'wide',
        delay: {
            show: 300,
            hide: 500
        }
    });
}