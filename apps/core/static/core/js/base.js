

const isEmptyValue = (value) => {
    if (value === '' || value === null || value === undefined) {
        return true
    } else {
        return false
    }
}

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

function setMenuActiveItem(menuItems, currentItem)
{
    menuItems.map(function (index, item)
    {
        $(item).removeClass('active');
    });
    currentItem.addClass('active');
}