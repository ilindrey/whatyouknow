
function changePathnameLocationURL(basePathname='', page = 1, suffix='')
{
    const slash = '/';
    let newURL, baseURL;

    newURL = new URL(window.location.href);
    baseURL = new URL(window.location.origin + basePathname);

    if(suffix)
        newURL.pathname = baseURL.pathname + suffix;

    if(newURL.pathname.slice(-1) !== slash)
        newURL.pathname += slash;

    if(page != 1)
         newURL.pathname += page + slash;

    history.replaceState(null, null, newURL.href);
}

function changeGetParamLocationURL(paramKey = String, paramValue, multiple = false)
{
    if (!paramKey)
        return null;

    let newURL = new URL(window.location.href);

    if(!isEmptyValue(paramValue))
    {
        if(multiple === true)
        {
            let list = newURL.searchParams.getAll(paramKey);
            let tag_exists = list.find(item => item === paramValue);
            if (!tag_exists)
            {
                newURL.searchParams.append(paramKey, paramValue);
            }
        }
        else
        {
            newURL.searchParams.set(paramKey, paramValue);
        }
    }
    else
    {
        newURL.searchParams.delete(paramKey);
    }

    history.replaceState(null, null, newURL.href);
}