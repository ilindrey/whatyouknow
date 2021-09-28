safeWrap();

function safeWrap()
{
    const keyInitial = 'semantic="dropdown"',
        keySearch = 'search',
        keyAllowAdditions = 'allow-additions',
        keyClearable = 'clearable',
        keyPlaceholder = 'placeholder';

    $(document).ready(function () {
        initialDropdown();
    });

    $(document).ajaxComplete(function( event, xhr, settings ) {
        if (xhr.statusText === 'OK' && xhr.responseText.includes(keyInitial))
        {
            initialDropdown();
        }
    });

    function initialDropdown()
    {
        let $element = $('select[' + keyInitial + ']');

        if($element.data(keySearch))
            $element.addClass('search');

        $element.dropdown({
            allowAdditions: $element.data(keyAllowAdditions),
            clearable: $element.data(keyClearable),
            placeholder: $element.data(keyPlaceholder)
        });

    }
}