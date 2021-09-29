
safeWrap();

function safeWrap()
{
    const keyCategories = 'categories',
        keyPeriod = 'period',
        keyRating = 'rating',
        keyControlPanel = 'control_panel',
        idCategories = '#' + keyCategories,
        idPeriod = '#' + keyPeriod,
        idRating = '#' + keyRating,
        idControlPanel = '#' + keyControlPanel,
        keyCategoriesItems = idCategories + ' .item',
        keyLoadDataUrl = 'load-data-url';

    let $categoriesMenu = null,
        $categoriesMenuItems = null,
        $periodDropdown = null,
        $ratingDropdown = null,
        $controlPanel = null,
        loadDataURL = null;

    $(document).ready(function ()
    {
        $controlPanel = $(idControlPanel);

        $categoriesMenu = $controlPanel.find(idCategories);
        $periodDropdown = $controlPanel.find(idPeriod);
        $ratingDropdown = $controlPanel.find(idRating);

        loadDataURL = $controlPanel.data(keyLoadDataUrl);

        let dropdown_params_default = {clearable: true};

        $periodDropdown.dropdown(Object.assign(dropdown_params_default, {
            onChange: function (value, text, $choice)
            {
                dropdownOnChangeHandler(keyPeriod, value, text, $choice);
            }
        }));
        $ratingDropdown.dropdown(Object.assign(dropdown_params_default, {
            onChange: function (value, text, $choice)
            {
                dropdownOnChangeHandler(keyRating, value, text, $choice);
            }
        }));

        let locationURL, category_param, period_param, rating_param;

        locationURL = new URL(window.location.href);

        category_param = locationURL.searchParams.get('category');
        period_param = locationURL.searchParams.get('period');
        rating_param = locationURL.searchParams.get('rating');

        $categoriesMenuItems = $(keyCategoriesItems);

        if(category_param)
        {
            $categoriesMenuItems.map(function (index, item)
            {
                let $item = $(this);
                if($item.data('value') == category_param)
                {
                    $item.click();
                    return;
                }
            });
        }
        else
        {
            $categoriesMenuItems.get(0).click();
        }

        if(period_param)
        {
            $periodDropdown.dropdown('set selected', period_param);
        }
        else
        {
            $periodDropdown.dropdown('restore default value');
        }

        if(rating_param)
        {
            $ratingDropdown.dropdown('set selected', rating_param);
        }
        else
        {
            $ratingDropdown.dropdown('restore default value');
        }

    });

    $(document).on('click', keyCategoriesItems, function (e) {
        e.preventDefault();

        let $item = $(this);
        setMenuActiveItem($categoriesMenuItems, $item);

        let paramKey, paramValue;
        paramKey = 'category';
        paramValue = $item.data('value');

        updateContent(paramKey, paramValue);
    });

    $(document).on('click', '#previous_page', function (e)
    {
        paginationHandler(e, this);
    });

    $(document).on('click', '#next_page', function (e)
    {
        paginationHandler(e, this);
    });


    $(document).on('click', '#pagination_menu .item', function (e)
    {
        paginationHandler(e, this);
    });

    function dropdownOnChangeHandler(key,value, text, $choice)
    {
        console.log(value + ' | ' + text + ' | ' + $choice)

        let paramKey, paramValue;
        paramKey = key;
        paramValue = $choice ? value : null;

        updateContent(paramKey, paramValue);
    }

    function paginationHandler(e, element)
    {
        e.preventDefault();

        let paramKey, paramValue;
        paramKey = 'page';
        paramValue = element.href.split('=')[1];

        updateContent(paramKey, paramValue);
    }

    function updateContent(paramKey = String, paramValue)
    {
        let locationURL, loadDataURLWithParams, deferred;

        locationURL = getLocationURL(paramKey, paramValue);
        loadDataURLWithParams = loadDataURL + locationURL.search;

        deferred = $.get(loadDataURLWithParams);
        deferred.done(function (responseText) {
            $('#content').html(responseText);
            history.replaceState(null, null, locationURL.href);
        });
        deferred.fail(function (xhr, ajaxOptions, thrownError) {
            showErrorMessage(xhr, ajaxOptions, thrownError);
        });
    }

    function getLocationURL(paramKey = String, paramValue)
    {
        if (!paramKey)
            return null;

        let newURL = new URL(window.location.href);

        if(!isEmptyValue(paramValue))
        {
            if(paramKey === 'tags')
            {
                let list = newURL.searchParams.getAll(paramKey)
                let tag_exists = list.find(item => item === paramValue)
                if (!tag_exists)
                {
                    newURL.searchParams.append(paramKey, paramValue);
                }
            }
            else
            {
                newURL.searchParams.set(paramKey, paramValue);
            }
        }
        else
        {
            newURL.searchParams.delete(paramKey);
        }

        if(paramKey !== 'page')
        {
            newURL.searchParams.delete('page');
        }

        if(paramKey === 'category' && paramValue == 'my')
        {
            newURL.searchParams.delete(paramKey);
        }

        let pathnameLastChar = newURL.pathname.slice(-1);
        if(newURL.search && pathnameLastChar === '/')
        {
              newURL.pathname = newURL.pathname.slice(0, -1);
        }
        else if(!newURL.search && pathnameLastChar !== '/')
        {
            newURL.pathname += '/';
        }

        return newURL;
    }
}