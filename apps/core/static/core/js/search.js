
safeWrap();

function safeWrap()
{
    $(document).ready(
        function () {
            let $controlPanel = $('#control_panel');
            let $roll = $('#roll');
            let $search = $controlPanel.find('#id_query_search');
            let $selections = $controlPanel.find('#selections');
            let $form = $search.closest('.ui.form');
            $search.search({
                    maxResults: 10,
                    apiSettings:{
                        data: {
                            query: () => { return $search.search('get value'); },
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
                        console.log(result);
                        console.log(response);
                        console.log(result.type);
                        const multiple = result.type !== 'text';
                        changeGetParamLocationURL(result.type, result.value, multiple);
                        $search.search('get value', null);

                        $.ajax({
                            type: 'get',
                            url: $controlPanel.data('search-selections-url') + window.location.search,
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
                            url: $controlPanel.data('post-list-load-data-url') + window.location.search,
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
        }
    );
}