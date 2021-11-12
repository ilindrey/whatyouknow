'use strict';
{
    window.addEventListener("load", function() {

        django.jQuery(function ($) { // stuff

            $(document).ready(function () {

                let $approvalElement = $('.form-row.field-approval');
                let $reasonElement = $('.form-row.field-reason');

                $reasonElement.hide();
                $approvalElement.find('input:checked').click();
            });

            $(document).on('click', '#id_approval input', function (e) {
                let $currentElement = $(this);
                let $reasonElement = $('.form-row.field-reason');

                let value = $currentElement.val();

                if (value == 1) {
                    $reasonElement.show();
                } else {
                    $reasonElement.hide();
                }
            });

        });

    });
}