
safeWrap();

function safeWrap() {

    const imageFileName = 'image_element',
        imageFileID = '#' + imageFileName,
        uploadButtonID = '#upload_image_button',
        removeButtonID = '#remove_image_button';


    let $imageElement, height, width, placeholder, required = false;

    $(document).ready(function () {
        initialImageMenu();
    });

    $(document).ajaxComplete(function (event, xhr, settings) {
        if (xhr.statusText === 'OK' && xhr.responseText.includes(imageFileName)) {
            initialImageMenu();
        }
    });

    function initialImageMenu() {
        $imageElement = $(imageFileID);

        placeholder = $imageElement.data('placeholder');
        required = $imageElement.data('required');

        $imageElement.popup({
            popup: '#edit_image_menu',
            position: 'top center',
            inline: true,
            hoverable: true,
            setFluidWidth: true,
            variation: 'wide',
            delay: {
                show: 300,
                hide: 500
            }
        });

        visibilityRemoveButton();

        $(document).off('click', uploadButtonID);
        $(document).off('click', removeButtonID);

        $(document).on('click', uploadButtonID, uploadButtonHandler);
        $(document).on('click', removeButtonID, removeButtonHandler);
    }


    function imageUploadActions()
    {
        $imageElement.height(height).width(width);
        setCheckedRemoveButton(false);
        visibilityRemoveButton();
    }

    function uploadButtonHandler(e) {
        e.preventDefault();
        let $fileInput = $(this).closest('.item').find('input');


        if($fileInput.length)
        {
            $fileInput.one('change', function (e) {
                e.preventDefault();
                const [file] = $fileInput.get(0).files
                if (file)
                {
                    height = $imageElement.height();
                    width = $imageElement.width();
                    $imageElement.attr('src', URL.createObjectURL(file));
                    imageUploadActions();
                    $imageElement.onload = function() {
                        URL.revokeObjectURL(this.src);
                        imageUploadActions();
                    }
                }
                else
                {
                    clearImage();
                }
            });
            $fileInput.click();
        }
    }

    function removeButtonHandler(e) {
        e.preventDefault();

        $('body').modal({
            closable: false,
            class: 'mini',
            content: 'Are you sure you want to reset your current image?',
            actions: [{
                text: 'Cancel',
                class: 'cancel'
            }, {
                text: 'OK',
                class: 'primary ok'
            }],
            onApprove: function ()
            {
                clearImage();
            }
        }).modal('show');
    }

    function clearImage()
    {
        let $fileInput = $(uploadButtonID).closest('.item').find('input');
        let $clearInput = $(removeButtonID).closest('.item');

        $clearInput.one('click', function (e) {

            e.preventDefault();

            $fileInput.val('');
            $imageElement.attr('src', placeholder);

            setCheckedRemoveButton(true);
            visibilityRemoveButton();

        });
        $clearInput.click();
    }

    function visibilityRemoveButton()
    {
        if (required === true)
            return;

        let removeButton = $(removeButtonID);
        if (removeButton.length)
        {
            let image = $imageElement.attr('src');
            let removeButtonItem = removeButton.closest('.item');

            if(image && image !== placeholder)
            {
                removeButtonItem.show();
            }
            else
            {
                removeButtonItem.hide();
            }
        }
    }

    function setCheckedRemoveButton(checked = false)
    {
        if (required === true)
            return;

        let removeButton = $(removeButtonID);
        if (removeButton.length)
        {
            let removeButtonItem = removeButton.closest('.item');
            let removeButtonInput = removeButtonItem.find('input');
            removeButtonInput.prop('checked', checked);
        }
    }
}