const keyContent = '#content',
    keyStepContent = '#step_content',
    keyCurUrl = 'cur-url',
    keyActionUrl = 'action-url';
// let keyContent,
//     keyStepContent,
//     keyCurUrl,
//     keyActionUrl;

let $content = null;

$(document).ready(function () {
    $content = $(keyContent);
    // keyContent = '#content';
    // keyStepContent = '#step_content';
    // keyCurUrl = 'cur-url';
    // keyActionUrl = 'action-url';
});

function setCurrentUrl()
{
    let $stepContent = $(keyStepContent);
    if ($stepContent)
    {
        const curUrl = $stepContent.data(keyCurUrl);
        if(curUrl)
        {
            let newUrl = new URL(window.location.origin + curUrl);
            history.replaceState(null, null, newUrl.href);
        }
    }
}