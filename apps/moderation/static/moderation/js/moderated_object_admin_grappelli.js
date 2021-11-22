'use strict';
{
    window.addEventListener("load", function() {

        django.jQuery(function ($) {

            let $approvalElement, $publishedElement, $reasonElement, initialization;

            $(document).ready(function () {
                initialization = true;

                $approvalElement = $('.form-row.approval');
                $publishedElement = $('.form-row.published');
                $reasonElement = $('.form-row.reason');

                $approvalElement.find('input:checked').change();

                initialization = false;
            });

            $(document).on('change', '.form-row.approval input', function (e) {

                let $element = $(this);
                let value = $element.val();

                if (value.length > 0)
                {
                    if(value == 0)
                    {
                        if(!initialization)
                        {
                            $publishedElement.prop('checked', true);
                        }
                        $publishedElement.show();
                        $publishedElement.find('input').change();
                    }
                    else if (value == 1)
                    {
                        if(!initialization)
                        {
                            $publishedElement.prop('checked', false);
                        }
                        $publishedElement.hide();
                        $publishedElement.find('input').change();
                        $reasonElement.show();
                    }
                    else
                    {
                        hideAllElements();
                    }
                }
                else
                {
                    hideAllElements();
                }
            });

            $(document).on('change', '.form-row.published input', function (e) {

                let $element = $(this);

                let isVisible = $element.is(":visible");
                let value = $element.prop('checked');

                if(isVisible && value === true)
                {
                    $reasonElement.hide();
                }
                else
                {
                    $reasonElement.show();
                }
            })

            function hideAllElements()
            {
                $publishedElement.prop('checked', false);
                $publishedElement.hide();
                $reasonElement.hide();
                $publishedElement.click();
            }

        });


    });
}