function findGetParameter(parameterName) {
    let result = null, tmp = [];
    location.search
        .slice(1)
        .split("&")
        .forEach(function (item) {
            tmp = item.split("=");
            if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}


function getSelectValues(select) {
    const result = [];
    const options = select && select.options;
    for (let i = 0; i < options.length; i++) {
        if (options[i].selected) result.push(options[i].value);
    }
    return result;
}