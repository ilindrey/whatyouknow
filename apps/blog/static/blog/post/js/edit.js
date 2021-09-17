// $(() => {
const keyWriteForm = '#edit_post_form';

let $writeForm = null;

$(document).ready(function () {
    initWriteForm();
});

$(document).on('click', '#save_as_draft_button', function (e) {
    e.preventDefault();
    sendWriteForm(false);
});


$(document).on('click', '#look_at_preview_button', function (e) {
    e.preventDefault();
    sendWriteForm(true);
});

function sendWriteForm(preview = false) {
    let form = $writeForm.get(0);
    let data = new FormData(form);
    data.append('preview', preview);
    data.append('draft', true);

    $.ajax({
        type: 'post',
        url: form.action,
        data: data,
        processData: false,
        contentType: false,
        enctype: 'multipart/form-data',
        success: function (responseText) {
            // let $content = $(keyContent);
            if ($content) {
                $content.html(responseText);
                if (!preview) {
                    initWriteForm();
                }
                setCurrentUrl();
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            showErrorMessage(xhr, ajaxOptions, thrownError);
        }
    });
}

function initWriteForm() {
    $writeForm = $(keyWriteForm);
    if ($writeForm)
        $writeForm.form();
}
// });

