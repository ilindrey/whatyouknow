
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
        keySearchSelectionsUrl = 'search-selections-url';

    let $controlPanel = null,
        $selections = null,
        $roll = null,
        $searchForm = null,
        $searchElem = null,
        basePathnameURL = null,
        postListLoadDataURL = null,
        searchSelectionsURL = null;

    $(document).ready(function () {

        $controlPanel = $(idControlPanel);
        $roll = $(idRoll);

        $searchForm = $controlPanel.find(idSearchForm);
        $selections = $controlPanel.find(idSelections);

        $searchElem = $searchForm.find(idSearchElem);

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
                    const multiple = result.type !== 'text';
                    changeGetParamLocationURL(result.type, result.value, multiple);
                    $searchElem.search('set value', null);
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

        if(window.location.search)
            updateContent();
    });

    $(document).on('submit', idSearchForm, function (e) {

        e.preventDefault();

        let value = $searchElem.search('get value');
        changeGetParamLocationURL('text', value, false);
        $searchElem.search('hide results');
        updateContent();
    });

    $(document).on('click', idSelections + ' .ui.labels .label .icon', function (e) {

        e.preventDefault();

        let $icon, $label, type, value;

        $icon = $(this);
        $label = $icon.closest('.label');

        type = $label.data('type');
        value = $label.data('value');

        const multiple = type !== 'text';
        deleteGetParamLocationURL(type, value, multiple);

        updateContent();
    });

    function updateContent()
    {
        changePathnameLocationURL(basePathnameURL, 1);

        let search = window.location.search;
        if(search)
        {
            $.ajax({
                type: 'get',
                url: searchSelectionsURL + search,
                beforeSend: function(jqXHR, settings)
                {
                    $selections.addClass('loading');
                },
                success: function (responseText) {
                    $selections.html(responseText);
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    showErrorMessage(xhr, ajaxOptions, thrownError);
                },
                complete: function (jqXHR, textStatus)
                {
                    $selections.removeClass('loading');
                },
            });

            $.ajax({
                type: 'get',
                url: postListLoadDataURL + search,
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
        else
        {
            $selections.html('');
            $roll.html('');
        }
    }
}