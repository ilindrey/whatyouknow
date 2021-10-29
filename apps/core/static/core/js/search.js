
safeWrap();

function safeWrap()
{
    const charID = '#',
        keyControlPanel = 'control_panel',
        keySelections = 'selections',
        keyRoll = 'roll',
        keySearchForm = 'search_form',
        keySearchElem = 'id_query_search',
        idControlPanel = charID + keyControlPanel,
        idSelections = charID + keySelections,
        idRoll = charID + keyRoll,
        idSearchForm = charID + keySearchForm,
        idSearchElem = charID + keySearchElem,
        keyBasePathnameUrl = 'base-pathname-url',
        keyPostListLoadDataUrl = 'post-list-load-data-url',
        keySearchSelectionsUrl = 'search-selections-url',
        keyCurrentPage = 'current-page';

    let initialization = false,
        $controlPanel,
        $selections,
        $roll,
        $searchForm,
        $searchElem,
        $loader,
        basePathnameURL,
        postListLoadDataURL,
        searchSelectionsURL;

    $(document).ready(function () {

        initialization = true;

        $controlPanel = $(idControlPanel);
        $roll = $(idRoll);
        $loader = $('.loader').closest('.ui.segment');

        $searchForm = $controlPanel.find(idSearchForm);
        $selections = $controlPanel.find(idSelections);

        $searchElem = $searchForm.find(idSearchElem);

        hideLoader();

        basePathnameURL = $controlPanel.data(keyBasePathnameUrl);
        postListLoadDataURL = $controlPanel.data(keyPostListLoadDataUrl);
        searchSelectionsURL = $controlPanel.data(keySearchSelectionsUrl);

        $searchElem.search({
                maxResults: 10,
                apiSettings:{
                    data: {
                        query: () => { return $searchElem.search('get value'); },
                    },
                    url: $controlPanel.data('search-suitable-results-url'),
                },
                fields: {
                    icon: 'icon',
                    value: 'value',
                    title: 'title',
                    type: 'type'
                },
                type: 'custom',
                onSelect: function(result, response) {
                    $searchElem.search('set value', null);
                    const multiple = result.type !== 'text';
                    const url = changeParamsURL(result.type, result.value, multiple);
                    history.replaceState(null, null, url.href);
                    updateContent();
                },
                templates: {
                    custom: function(response, fields, preserveHTML) { // based on standard
                      let
                        html = '',
                        escape = $.fn.search.settings.templates.escape
                      ;
                      if(response[fields.results] !== undefined) {

                        // each result
                        $.each(response[fields.results], function(index, result) {
                          if(result[fields.url]) {
                            html  += '<a class="result" href="' + result[fields.url].replace(/"/g,"") + '">';
                          }
                          else {
                            html  += '<a class="result">';
                          }
                          if(result[fields.image] !== undefined) {
                            html += ''
                              + '<div class="image">'
                              + ' <img src="' + result[fields.image].replace(/"/g,"") + '">'
                              + '</div>'
                            ;
                          }
                          html += '<div class="content">';
                          if(result[fields.icon] !== undefined && result[fields.icon]) { // added in custom template
                              html += '<i class="' + escape(result[fields.icon], preserveHTML) + ' icon"></i>';
                          }
                          if(result[fields.price] !== undefined) {
                            html += '<div class="price">' + escape(result[fields.price], preserveHTML) + '</div>';
                          }
                          if(result[fields.title] !== undefined) {
                            // html += '<div class="title">' + escape(result[fields.title], preserveHTML) + '</div>';
                            html += '<span class="title">' + escape(result[fields.title], preserveHTML) + '</span>'; // changed in custom template
                          }
                          if(result[fields.description] !== undefined) {
                            html += '<div class="description">' + escape(result[fields.description], preserveHTML) + '</div>';
                          }
                          html  += ''
                            + '</div>'
                          ;
                          html += '</a>';
                        });
                        if(response[fields.action]) {
                          if(fields.actionURL === false) {
                            html += ''
                            + '<div class="action">'
                            +   escape(response[fields.action][fields.actionText], preserveHTML)
                            + '</div>';
                          } else {
                            html += ''
                            + '<a href="' + response[fields.action][fields.actionURL].replace(/"/g,"") + '" class="action">'
                            +   escape(response[fields.action][fields.actionText], preserveHTML)
                            + '</a>';
                          }
                        }
                        return html;
                      }
                      return false;
                    }
                }
            });

        $searchForm.form();

        if(location.search)
            updateContent();

        initialization = false;
    });

    $(document).on('submit', idSearchForm, function (e) {

        e.preventDefault();

        $searchElem.search('hide results');
        const value = $searchElem.search('get value');
        const url = setParamURL('text', value);
        history.replaceState(null, null, url.href);
        updateContent();
    });

    $(document).on('click', idSelections + ' .ui.labels .label .icon', function (e) {

        e.preventDefault();

        let $icon, $label;

        $icon = $(this);
        $label = $icon.closest('.label');

        const url = deleteParamURL($label.data('type'), $label.data('value'));
        history.replaceState(null, null, url.href)
        updateContent();
    });

    function updateContent()
    {
        if(!initialization) {
            const currentPage = 1;
            const url = getURL(null, currentPage, basePathnameURL);
            $roll.data(keyCurrentPage, currentPage);
            history.replaceState(null, null, url.href);
        }

        if(location.search)
        {
            $.ajax({
                type: 'get',
                url: searchSelectionsURL + location.search,
                beforeSend: function(jqXHR, settings)
                {
                    showLoader();
                },
                success: function (responseText) {
                    $selections.html(responseText);
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    showErrorMessage(xhr, ajaxOptions, thrownError);
                },
                complete: function (jqXHR, textStatus)
                {
                    hideLoader();
                },
            });

            $.ajax({
                type: 'get',
                url: postListLoadDataURL + location.search,
                data: {
                        page: $roll.data(keyCurrentPage),
                    },
                beforeSend: function(jqXHR, settings)
                {
                    showLoader();
                },
                success: function (responseText) {
                    $roll.html(responseText);
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    showErrorMessage(xhr, ajaxOptions, thrownError);
                },
                complete: function (jqXHR, textStatus)
                {
                    hideLoader();
                },
            });
        }
        else
        {
            $selections.html('');
            $roll.html('');
            hideLoader();
        }
    }

    function showLoader()
    {
        $roll.html('');
        $loader.show();
    }

    function hideLoader()
    {
        $loader.hide();
    }
}