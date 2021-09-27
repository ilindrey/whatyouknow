
safeWrap();

function safeWrap() {

    const keyTab = 'tab',
        keyCurrentTabPath = 'current-tab-path',
        keyCurrentProfileLink = 'current-profile-link',
        keyIsDescendantMenu = 'is-descendant-menu',
        keyLinkLoadData = 'link-load-data',
        keyLinkLazyLoad = 'link-lazy-load',
        keyIsLazyLoad = 'is-lazy-load',
        keyStepContext = 'step-context',
        keyCurrentPage = 'current-page',
        keyTotalPage = 'total-page';

    $(document).ready(function ()
    {
        const $profileTabs = $('#profile_tabs');

        const currentProfileLink = $profileTabs.data(keyCurrentProfileLink);
        let currentTabPath = $profileTabs.data(keyCurrentTabPath);

        const $tabMenu = $('.menu .item');

        $tabMenu.tab('change tab', currentTabPath);
        let newUrl = new URL(window.location.origin + currentProfileLink + currentTabPath + '/');
        history.pushState(null, null, newUrl.href);

        $tabMenu.tab({

            onFirstLoad: function (tabPath, parameterArray, historyEvent) {
                let $tab = $(this);

                const linkLoadData = $tab.data(keyLinkLoadData);
                const linkLazyLoad = $tab.data(keyLinkLazyLoad);
                const isLazyLoad = $tab.data(keyIsLazyLoad)
                const stepContext = $tab.data(keyStepContext);
                const isDescendantMenu = $tab.data(keyIsDescendantMenu);

                let loader = $tab.find('.loader').closest('.segment');
                loader.hide();

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
                        if (isLazyLoad) {
                            let $tabStepContext = $tab.find(stepContext);

                            $tab.visibility({

                                once: false,

                                observeChanges: true,

                                onBottomVisible: function () {

                                    const currentPage = $tabStepContext.data(keyCurrentPage);
                                    const totalPage = $tabStepContext.data(keyTotalPage);
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
                if (isDescendantMenu) {
                    let descendantTab = $tab.find('.menu .item').get(0);
                    urlTabPath = $(descendantTab).data(keyTab);
                } else {
                    urlTabPath = tabPath;
                }

                let newUrl = new URL(window.location.origin + currentProfileLink + urlTabPath + '/');

                history.pushState(null, null, newUrl.href);

                currentTabPath = urlTabPath
                $profileTabs.data(keyCurrentTabPath, currentTabPath);
            },
        });

        $tabMenu.first().tab('change tab', currentTabPath);
    });
}å