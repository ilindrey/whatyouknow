
safeWrap();

function safeWrap() {

    const keyTab = 'tab',
        keyIsDescendantMenu = 'is-descendant-menu',
        keyIsLazyLoad = 'is-lazy-load',
        keyIsFirstLoad = 'is-first-load',
        keyBasePathnameUrl = 'base-pathname-url',
        keyCurrentTabPath = 'current-tab-path',
        keyLinkLoadData = 'link-load-data',
        keyLinkLazyLoad = 'link-lazy-load',
        keyStepContext = 'step-context',
        keyCurrentPage = 'current-page',
        keyTotalPage = 'total-page';

    $(document).ready(function ()
    {
        const $profileTabs = $('#profile_tabs');

        const basePathnameUrl = $profileTabs.data(keyBasePathnameUrl);
        let currentTabPath = $profileTabs.data(keyCurrentTabPath);

        const $tabMenu = $('.menu .item');

        $tabMenu.tab('change tab', currentTabPath);
        const url = getURL(null, null, basePathnameUrl, currentTabPath);
        history.replaceState(null, null, url.href);

        $tabMenu.tab({

            onFirstLoad: function (tabPath, parameterArray, historyEvent) {
                let $tab = $(this);

                const stepContext = $tab.data(keyStepContext);
                const isDescendantMenu = $tab.data(keyIsDescendantMenu);
                const isFirstLoad = $tab.data(keyIsFirstLoad);
                const isLazyLoad = $tab.data(keyIsLazyLoad);
                const linkLoadData = $tab.data(keyLinkLoadData);
                const linkLazyLoad = $tab.data(keyLinkLazyLoad);

                let loader = $tab.find('.loader').closest('.segment');
                loader.hide();

                if(isFirstLoad)
                    return;

                if (isDescendantMenu)
                    return;

                $.ajax({
                    type: 'get',
                    url: linkLoadData,
                    beforeSend: function () {
                        loader.show();
                    },
                    success: function (responseText) {
                        $tab.prepend(responseText);
                        $tab.data(keyIsFirstLoad, true);
                        if (isLazyLoad) {
                            let $tabStepContext = $tab.find(stepContext);

                            $tab.visibility({

                                once: false,

                                observeChanges: true,

                                onBottomVisible: function () {

                                    const cp = $tabStepContext.data(keyCurrentPage);
                                    const tp = $tabStepContext.data(keyTotalPage);

                                    const currentPage  = cp ? cp : 1;
                                    const totalPage = tp ? tp : 1;
                                    const nextPage = currentPage + 1;

                                    if (nextPage > totalPage) {
                                        $tab.visibility('disable callbacks');
                                    } else {
                                        $.ajax({
                                            type: 'get',
                                            url: linkLazyLoad,
                                            data: {
                                                'page': nextPage,
                                            },
                                            beforeSend: function () {
                                                loader.show();
                                            },
                                            success: function (responseText) {
                                                $tabStepContext.append(responseText);
                                                $tabStepContext.data(keyCurrentPage, nextPage);
                                            },
                                            error: function (xhr, ajaxOptions, thrownError) {
                                                showErrorMessage(xhr, ajaxOptions, thrownError);
                                            },
                                            complete: function () {
                                                loader.hide();
                                            }
                                        });
                                    }
                                },
                            });
                        }
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        showErrorMessage(xhr, ajaxOptions, thrownError);
                    },
                    complete: function () {
                        loader.hide();
                    }
                });
            },

            onVisible: function (tabPath) {
                let $tab = $(this);
                let urlTabPath = ''

                const isDescendantMenu = $tab.data(keyIsDescendantMenu);
                if (isDescendantMenu)
                {
                    let descendantTab = $tab.find('.menu .item').get(0);
                    urlTabPath = $(descendantTab).data(keyTab);
                }
                else
                {
                    urlTabPath = tabPath;
                }

                currentTabPath = urlTabPath
                $profileTabs.data(keyCurrentTabPath, currentTabPath);

                const url = getURL(null, null, basePathnameUrl, currentTabPath);
                history.replaceState(null, null, url.href);
            },
        });

        $tabMenu.first().tab('change tab', currentTabPath);
    });

    function ajaxLoad($tab, $context)
    {

    }
}