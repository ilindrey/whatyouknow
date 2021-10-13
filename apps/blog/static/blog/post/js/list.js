
safeWrap();

function safeWrap()
{
    const charID = '#',
        keyControlPanel = 'control_panel',
        keyRoll = 'roll',
        keyCategories = 'categories',
        keyRating = 'rating',
        keyPeriod = 'period',
        idControlPanel = charID + keyControlPanel,
        idRoll = charID + keyRoll,
        idCategories = charID + keyCategories,
        idRating = charID + keyRating,
        idPeriod = charID + keyPeriod,
        keyCategoriesItems = idCategories + ' .item',
        keyBasePathnameUrl = 'base-pathname-url',
        keyPostListLoadDataUrl = 'post-list-load-data-url';
        // keyAjaxSuffix = 'ajax-suffix';

    let $controlPanel = null,
        $roll = null,
        $categoriesMenu = null,
        $categoriesMenuItems = null,
        $periodDropdown = null,
        $ratingDropdown = null,
        isCategoryMenu = false,
        isPeriodDropdown = false,
        isRatingDropdown = false,
        basePathnameURL = null,
        postListLoadDataURL = null;
        // ajaxSuffix = null;


    const currentCategory = () => {
        if (isCategoryMenu && $categoriesMenuItems && $categoriesMenuItems.length) {
            return $categoriesMenuItems.filter('.active').data('value')
        } else {
            return null
        }
    }

    $(document).ready(function ()
    {
        $controlPanel = $(idControlPanel);
        $roll = $(idRoll);

        basePathnameURL = $controlPanel.data(keyBasePathnameUrl);
        postListLoadDataURL = $controlPanel.data(keyPostListLoadDataUrl);

        $categoriesMenu = $controlPanel.find(idCategories);
        $ratingDropdown = $controlPanel.find(idRating);
        $periodDropdown = $controlPanel.find(idPeriod);

        isCategoryMenu = $categoriesMenu.length > 0;
        isRatingDropdown = $ratingDropdown.length > 0;
        isPeriodDropdown = $periodDropdown.length > 0;

        let locationURL, category_param, rating_param, period_param;

        locationURL = new URL(window.location.href);

        if(isRatingDropdown)
        {
            $ratingDropdown.dropdown({
                clearable: true,
                onChange: function (value, text, $choice)
                {
                    dropdownOnChangeHandler(keyRating, value, text, $choice);
                }
            });
            rating_param = locationURL.searchParams.get('rating');
            if(rating_param)
            {
                $ratingDropdown.dropdown('set selected', rating_param);
            }
            else
            {
                $ratingDropdown.dropdown('clear');
            }
            // $ratingDropdown.closest('.ui.dropdown').hide();
        }

        if(isPeriodDropdown)
        {
            $periodDropdown.dropdown({
                clearable: true,
                onChange: function (value, text, $choice)
                {
                    dropdownOnChangeHandler(keyPeriod, value, text, $choice);
                }
            });
            period_param = locationURL.searchParams.get('period');
            if(period_param)
            {
                $periodDropdown.dropdown('set selected', period_param);
            }
            else
            {
                $periodDropdown.dropdown('clear')
                $periodDropdown.closest('.ui.dropdown').hide();
            }
        }

        if(isCategoryMenu)
        {
            category_param = locationURL.searchParams.get('category');

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
        }
    });

    $(document).on('click', keyCategoriesItems, function (e) {
        if(!isCategoryMenu)
            return;

        e.preventDefault();

        let $item = $(this);
        setMenuActiveItem($categoriesMenuItems, $item);

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

                changeGetParamLocationURLOverride(keyPeriod, null, false, false);
            }
            else
            {
                $periodDropdown.closest('.ui.dropdown').show();
            }
        }


        changeGetParamLocationURLOverride(paramKey, paramValue);
    }

    function paginationHandler(e, element)
    {
        e.preventDefault();

        let page = element.href.split('=')[1];

        updateContent(page);
    }

    function updateContent(page= 1)
    {
        changePathnameLocationURLOverride(page)

        let params, category, locationURL;
        params = {};
        category = currentCategory();
        locationURL = new URL(window.location.href);

        if (category)
        {
            params.category = category;
        }
        if(page)
        {
            params.page = page;
        }

        $.ajax({
            type: 'get',
            url: postListLoadDataURL + locationURL.search,
            data: params,
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
        changePathnameLocationURL(basePathnameURL, page, currentCategory());
    }

    function changeGetParamLocationURLOverride(paramKey, paramValue, multiple= false, runUpdateContext= true)
    {
        changeGetParamLocationURL(paramKey, paramValue, multiple);
        if(runUpdateContext)
        {
            updateContent(1);
        }
        else
        {
            changePathnameLocationURLOverride(1);
        }
    }
}