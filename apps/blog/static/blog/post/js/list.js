
safeWrap();

function safeWrap()
{
    const charID = '#',
        keyCategories = 'categories',
        keyPeriod = 'period',
        keyRating = 'rating',
        keyControlPanel = 'control_panel',
        keyRoll = 'roll',
        idCategories = charID + keyCategories,
        idPeriod = charID + keyPeriod,
        idRating = charID + keyRating,
        idControlPanel = charID + keyControlPanel,
        idRoll = charID + keyRoll,
        keyCategoriesItems = idCategories + ' .item',
        keyBasePathnameUrl = 'base-pathname-url',
        keyAjaxSuffix = 'ajax-suffix';

    let $categoriesMenu = null,
        $categoriesMenuItems = null,
        $periodDropdown = null,
        $ratingDropdown = null,
        $controlPanel = null,
        $roll = null,
        basePathnameURL = null,
        ajaxSuffix = null;

    $(document).ready(function ()
    {
        $controlPanel = $(idControlPanel);
        $roll = $(idRoll);

        $categoriesMenu = $controlPanel.find(idCategories);
        $periodDropdown = $controlPanel.find(idPeriod);
        $ratingDropdown = $controlPanel.find(idRating);

        basePathnameURL = $controlPanel.data(keyBasePathnameUrl);
        ajaxSuffix = $controlPanel.data(keyAjaxSuffix);

        $periodDropdown.dropdown({
            clearable: true,
            onChange: function (value, text, $choice)
            {
                dropdownOnChangeHandler(keyPeriod, value, text, $choice);
            }
        });
        $ratingDropdown.dropdown({
            clearable: true,
            onChange: function (value, text, $choice)
            {
                dropdownOnChangeHandler(keyRating, value, text, $choice);
            }
        });

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
            $periodDropdown.dropdown('clear');
        }

        if(rating_param)
        {
            $ratingDropdown.dropdown('set selected', rating_param);
        }
        else
        {
            $ratingDropdown.dropdown('clear');
        }

        $periodDropdown.closest('.ui.dropdown').hide();
        // $ratingDropdown.closest('.ui.dropdown').hide();
    });

    $(document).on('click', keyCategoriesItems, function (e) {
        e.preventDefault();

        let $item = $(this);
        setMenuActiveItem($categoriesMenuItems, $item);

        changePathnameLocationURLOverride();
        updateContent();
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

    function dropdownOnChangeHandler(key, value, text, $choice)
    {
        let paramKey, paramValue;
        paramKey = key;
        paramValue = $choice ? value : null;

        if(key === keyRating)
        {
            if(isEmptyValue(paramValue))
            {
                $periodDropdown.closest('.ui.dropdown').hide();
                $periodDropdown.dropdown('clear');

                changeGetParamLocationURLOverride(keyPeriod, null);
            }
            else
            {
                $periodDropdown.closest('.ui.dropdown').show();
            }
        }


        changeGetParamLocationURLOverride(paramKey, paramValue);
        updateContent();
    }

    function paginationHandler(e, element)
    {
        e.preventDefault();

        let page = element.href.split('=')[1];

        changePathnameLocationURLOverride(page);
        updateContent();
    }

    function updateContent()
    {
        let locationURL, loadDataURL;

        locationURL = new URL(window.location.href);
        loadDataURL = locationURL.pathname + ajaxSuffix + locationURL.search;

        $.ajax({
            type: 'get',
            url: loadDataURL,
            beforeSend: function(jqXHR, settings)
            {
                $roll.addClass('loading');
            },
            success: function (responseText) {
                $roll.html(responseText);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                showErrorMessage(xhr, ajaxOptions, thrownError);
            },
            complete: function (jqXHR, textStatus)
            {
                $roll.removeClass('loading');
            },
        });
    }

    function changePathnameLocationURLOverride(page=1)
    {
        let category = $categoriesMenuItems.filter('.active').data('value');
        changePathnameLocationURL(basePathnameURL, page, category);
    }

    function changeGetParamLocationURLOverride(paramKey, paramValue, multiple)
    {
        changePathnameLocationURLOverride(1);
        return changeGetParamLocationURL(paramKey, paramValue, multiple);
    }
}