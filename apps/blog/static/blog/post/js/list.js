
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
        keyPostListLoadDataUrl = 'post-list-load-data-url',
        keyCurrentCategory = 'current-category',
        keyCurrentPage = 'current-page';

    let initialization = false,
        $controlPanel = null,
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

    $(document).ready(function ()
    {
        initialization = true;

        $controlPanel = $(idControlPanel);
        $roll = $(idRoll);

        const currentPage = $roll.data(keyCurrentPage);
        if(!currentPage) {
            $roll.data(keyCurrentPage, 1);
        }

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
                $periodDropdown.dropdown('clear');
            }
        }

        if(isCategoryMenu)
        {
            category_param = locationURL.searchParams.get('category') || $controlPanel.data(keyCurrentCategory);

            $categoriesMenuItems = $(keyCategoriesItems);

            if(category_param)
            {
                for (let i = 0; i < $categoriesMenuItems.length; i++)
                {
                    let $item = $($categoriesMenuItems[i]);
                    if($item.data('value') == category_param)
                    {
                        $item.click();
                        break;
                    }
                }
            }
            else
            {
                $categoriesMenuItems.get(0).click();
            }
        }

        initialization = false;
    });

    $(document).on('click', keyCategoriesItems, function (e) {
        if(!isCategoryMenu)
            return;

        e.preventDefault();

        let $item = $(this);
        setMenuActiveItem($categoriesMenuItems, $item);

        if(!initialization)
        {
            $roll.data(keyCurrentPage, 1);
            $controlPanel.data(keyCurrentCategory, $item.data('value'));
        }

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

                if(!initialization)
                    changeParamURL(keyPeriod, null, false);
            }
            else
            {
                $periodDropdown.closest('.ui.dropdown').show();
            }
        }


        if(!initialization)
            changeParamURL(paramKey, paramValue);
    }

    function paginationHandler(e, element)
    {
        e.preventDefault();

        const page = element.href.split('=')[1];
        $roll.data(keyCurrentPage, page);

        updateContent();
    }

    function updateContent()
    {
        let currentCategory, currentPage, params,  locationURL;

        currentPage = $roll.data(keyCurrentPage);
        currentCategory = $controlPanel.data(keyCurrentCategory);

        if(!initialization)
        {
            const url = getURL(null, currentPage, basePathnameURL, currentCategory);
            history.replaceState(null, null, url.href);
        }

        params = {};
        locationURL = new URL(window.location.href);

        if(currentPage) {
            params.page = currentPage;
        }
        if (currentCategory) {
            params.category = currentCategory;
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

    function changeParamURL(paramKey, paramValue, runUpdateContext= true)
    {
        const url = setParamURL(paramKey, paramValue);
        history.replaceState(null, null, url.href);
        if(!initialization)
            $roll.data(keyCurrentPage, 1);
        if(runUpdateContext)
        {
            updateContent();
        }
        else
        {
            const currentPage = $roll.data(keyCurrentPage);
            const currentCategory = $controlPanel.data(keyCurrentCategory);
            const url = getURL(null, currentPage, basePathnameURL, currentCategory);
            history.replaceState(null, null, url);
        }
    }
}