safeWrap();

function safeWrap()
{
    $(document).ready(function () {
        initialDropdown();
    });

    $(document).ajaxComplete(function( event, xhr, settings ) {
        if (xhr.statusText === 'OK' && xhr.responseText.includes('tags_selection'))
        {
            initialDropdown();
        }
    });

    function initialDropdown()
    {
        const separator = ', ',
            quotes = '\"',
            $element = $('#tags_selection'),
            keyNameTagsInput = 'name-tags-input',
            keyAllowAdditions = 'allow-additions',
            keyClearable = 'clearable';

        const nameTagsInput = $element.data(keyNameTagsInput),
            allowAdditions = $element.data(keyAllowAdditions),
            clearable = $element.data(keyClearable);

        let tagsInput = $element.find('#id_' + nameTagsInput);

        let tagsInputValue = tagsInput.val();
        if(tagsInputValue)
        {
            let arrayOfValue = tagsInputValue.split(separator);
            arrayOfValue.map(function(item, index) {
                arrayOfValue[index] = item.replaceAll(quotes, '');
            });
            $element.dropdown('set selected', arrayOfValue);
        }

        $element.dropdown({
                onAdd: function (addedValue, addedText, $addedChoice)
                {
                    let tagsInputValue = tagsInput.val();

                    let formattedText;
                    let arrayOfText = addedText.split(' ');
                    if (arrayOfText.length > 1)
                    {
                        formattedText = quotes + addedText + quotes;
                    }
                    else {
                        formattedText = addedText;
                    }

                    if(tagsInputValue)
                    {
                        let arrayOfValue = tagsInputValue.split(separator);
                        arrayOfValue.push(formattedText);
                        tagsInputValue = arrayOfValue.join(separator);
                    }
                    else
                    {
                        tagsInputValue = formattedText;
                    }

                    tagsInput.val(tagsInputValue);
                },
                onRemove: function (removedValue, removedText, $removedChoice)
                {
                    let tagsInputValue = tagsInput.val();

                    let arrayOfInputValue = tagsInputValue.split(separator);
                    arrayOfInputValue.map(function(item, index) {
                        arrayOfInputValue[index] = item.replaceAll(quotes, '');
                    });

                    const index = arrayOfInputValue.indexOf(removedText);
                    if (index > -1) {
                        arrayOfInputValue.splice(index, 1);
                    }

                    arrayOfInputValue.map(function(item, index) {

                        let value = item;
                        let arrayOfItem = item.split(' ');
                        if (arrayOfItem.length > 1)
                        {
                            value = quotes + item + quotes;
                        }
                        arrayOfInputValue[index] = value;
                    });

                    tagsInputValue = arrayOfInputValue.join(separator);
                    tagsInput.val(tagsInputValue);
                },
                clearable: clearable,
                allowAdditions: allowAdditions,
            }
        );
    }
}