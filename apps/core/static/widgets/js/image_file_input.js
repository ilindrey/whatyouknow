$(document).ready(function () {
    initialImageMenu();
});

$(document).ajaxComplete(function( event, xhr, settings ) {
    if (xhr.statusText === 'OK' && xhr.responseText.search('image_img') > -1)
    {
        initialImageMenu();
    }
});

$(document).on('ready', '#upload_image_button', function ()
{
    $('#image_img').popup({
        popup: '#edit_image_menu',
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

$(document).on('click', '#upload_image_button', function ()
{
    let $fileInput = $(this).closest('.item').find('input');
    $fileInput.one('change', function (e)
    {
        console.log('file changed');
        let input = $(this).get(0);
        const [file] = input.files
        if (file)
        {
            $('#image_img').attr('src', URL.createObjectURL(file));
        }
    });
    $fileInput.click();
});

$(document).on('click', '#remove_image_button', function (e)
{
    e.preventDefault();
    let $fileInput = $(this).closest('.item').find('input');
    $('body').modal({
        closable: false,
        class: 'mini',
        content: 'Are you sure you want to reset your current image?',
        actions: [{
            text: 'Cancel',
            class: 'cancel'
        },  {
            text: 'OK',
            class: 'primary ok'
        }],
        onApprove: function () {
            $fileInput.click();
        }
    }).modal('show');
});


function initialImageMenu()
{
    $('#image_img').popup({
        popup: '#edit_image_menu',
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