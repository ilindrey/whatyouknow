$(document).ready(function () {

    // $.fn.api.settings.api = {
    //     'profile' : '{% url 'profile' object.username %}',
    //     'profile_tab' : '{% url 'profile_tab' object.username current_tab %}',
    //     'profile_tab_data_load' : '{% url 'profile_tab_data_load' object.username %}',
    // };


    let profileTabsContainer =  $('#profile_tabs_container');

    const urlAjaxProfileTabDataLoad =  profileTabsContainer.data('url-ajax-profile-tab-data-load');

    const keyCurrentTab = 'current-tab';
    let currentTab = profileTabsContainer.data(keyCurrentTab);


    const tab_menu = $('#user_profile_tab_menu .item');


    tab_menu.tab('change tab', currentTab);

    tab_menu.tab({

        onFirstLoad: function ()
        {
            $(this).visibility({

                once: false,

                observeChanges: true,

                onBottomVisible: function() {

                    let tab = $(this);
                    const tabName = tab.data('tab');

                    // console.log(tabName + ' - onBottomVisible');

                    if(currentTab !== tabName)
                        return;

                    let tabItems = tab.find('.ui.items');

                    const isFirstLoad = tabItems.length === 0;

                    // console.log('isFirstLoad - ' + isFirstLoad);

                    const keyCurrentPage = 'current-page';
                    const keyTotalPage = 'total-page';

                    const tabCurrentPage = isFirstLoad ? 0 : tabItems.data(keyCurrentPage);
                    const tabTotalPage = isFirstLoad ? 1 : tabItems.data(keyTotalPage);

                    let nextPage = tabCurrentPage + 1;

                    if (nextPage <= tabTotalPage)
                    {
                        $.ajax({
                            type: 'get',
                            url: urlAjaxProfileTabDataLoad,
                            data: {
                                tab: tabName,
                                page: nextPage,
                            },
                            success: function (result) {

                                if(isFirstLoad)
                                {
                                    tab.append(result);
                                }
                                else
                                {
                                    tabItems.append(result);
                                    tabItems.data(keyCurrentPage, nextPage);
                                }
                                // console.log('added ' + tab.data('tab') + ' items');
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
            profileTabsContainer.data(keyCurrentTab, currentTab)

        }
    });

    tab_menu.tab('change tab', currentTab);

});
