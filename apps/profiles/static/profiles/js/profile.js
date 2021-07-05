$(document).ready(function () {

    const $tabMenu = $('#user_profile_tab_menu');
    const $tabMenuItems = $tabMenu.find('.item');

    const keyCurrentTab = 'current-tab';
    const urlAjaxProfileTabLoadData =  $tabMenu.data('url-ajax-profile-tab-load-data');
    let currentTab = $tabMenu.data(keyCurrentTab);

    $tabMenuItems.tab('change tab', currentTab);

    $tabMenuItems.tab({
        onFirstLoad: function ()
        {
            $(this).visibility({

                once: false,

                observeChanges: true,

                onBottomVisible: function() {

                    let tab = $(this);
                    const tabName = tab.data('tab');

                    if(currentTab !== tabName)
                        return;

                    let tabItems = tab.find('.ui.items');

                    const keyIsFirstLoad = 'is-first-load';
                    const keyCurrentPage = 'current-page';
                    const keyTotalPage = 'total-page';

                    const isFirstLoad = tab.data(keyIsFirstLoad);
                    const tabCurrentPage = isFirstLoad ? 0 : tabItems.data(keyCurrentPage);
                    const tabTotalPage = isFirstLoad ? 1 : tabItems.data(keyTotalPage);

                    const loader = $('#tab_' + currentTab + ' .loader').closest('.segment');

                    let nextPage = tabCurrentPage + 1;

                    if (nextPage <= tabTotalPage)
                    {
                        $.ajax({
                            type: 'get',
                            url: urlAjaxProfileTabLoadData,
                            data: {
                                tab: tabName,
                                page: nextPage,
                            },
                            beforeSend: function () {
                                loader.show();
                            },
                            success: function (result) {
                                if(isFirstLoad)
                                {
                                    tab.prepend(result);
                                    tab.data(keyIsFirstLoad, false);
                                }
                                else
                                {
                                    tabItems.prepend(result);
                                    tabItems.data(keyCurrentPage, nextPage);
                                }
                            },
                            complete: function () {
                                loader.hide();
                            }

                        })
                    }
                },
            });
        },

        onVisible: function (tabPath)
        {
            // console.log(tabPath + ' onVisible');

            let newUrl = new URL(window.location);

            newUrl.pathname = newUrl.pathname.replace(currentTab, tabPath);

            history.pushState(null, null, newUrl.href);

            currentTab = tabPath;
            $tabMenu.data(keyCurrentTab, currentTab)

        }
    });

    $('#' + currentTab).tab('change tab', currentTab);

});
