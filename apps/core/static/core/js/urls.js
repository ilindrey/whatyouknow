
const slash = '/';

function setSlash(value)
{
    if(value.slice(-1) !== slash)
        value += slash;
}

function checkSlashes(value)
{
    if(value.slice(0, 1) === slash)
        value = value.slice(1, value.length);
    if(value.slice(-1) !== slash)
        value += slash;
    return value;
}

function getURL(url = null, page = null, ...theArgs)
{
    let newURL = new URL(url ? url : location.href);

    newURL.pathname = '';
    for (let i = 0; i < theArgs.length; i++)
    {
        let value = theArgs[i];
        if(value)
            newURL.pathname += checkSlashes(theArgs[i]);
    }

    if(page && page > 1)
        newURL.pathname += page + slash;

    return newURL;
}

function getParam(key, url = location.href)
{
    let u = new URL(url);
    return u.searchParams.get(key);
}

function getParams(key, url = location.href)
{
    let u = new URL(url);
    return u.searchParams.getAll(key);
}

function changeParamsURL(paramKey = '', paramValue, multiple = false, startingURL = location.href)
{
    if (!paramKey)
        return null;

    let newURL = new URL(startingURL);

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
        if(multiple !== true)
            newURL.searchParams.delete(paramKey);
    }

    return newURL;
}

function setParamURL(paramKey = '', paramValue, startingURL = location.href)
{
    return changeParamsURL(paramKey, paramValue, false, startingURL);
}

function appendParamURL(paramKey = '', paramValue, startingURL = location.href)
{
    return changeParamsURL(paramKey, paramValue, true, startingURL);
}

function deleteParamURL(paramKey = '', paramValue, startingURL = location.href)
{
    if (!paramKey)
        return null;

    let newURL = new URL(startingURL);

    let list = newURL.searchParams.getAll(paramKey);
    if (list.length > 1)
    {
        const index = list.indexOf(paramValue);
        if (list.indexOf(paramValue) > -1) {
            list.splice(index, 1);
        }

        newURL.searchParams.delete(paramKey);
        list.map(function(item, index) {
                    newURL.searchParams.append(paramKey, item);
                });
    }
    else
    {
        newURL.searchParams.delete(paramKey);
    }

    return newURL;
}

