$(document).ready(
    function () {

        let blockNameList = ["roof", "content", "floor"];

        for (let blockName of blockNameList)
        {
            let block = $('#' + blockName);
            if (block.children().length === 0)
            {
                block.closest('.row').remove();
            }
        }

        let authTitle = $('#auth_title');
        if(authTitle.length !== 0 && !authTitle.text())
        {
            authTitle.closest('.row').remove();
        }

    }
);

function showMessage(text, class_message='success')
{
    $('body').toast({
        class: class_message,
        position: 'bottom right',
        message: text
    });
    console.log(class_message + ': ' + text);
}

function showSuccessMessage(text)
{
    showMessage(text, 'success');
}

function showInfoMessage(text)
{
    showMessage(text, 'info');
}

function showErrorMessage(xhr, ajaxOptions, thrownError)
{
    let text = xhr.status + ' ' + xhr.statusText;
    showMessage(text, 'error');
}