var main = (function (paginator, itemsPerPage) {

    var init = function () {

        if (paginator) {
            paginator.create('.main-content .entry', {
                'itemsPerPage': itemsPerPage
            });
        }
    };

    return { 'init': init };

})(typeof paginator === 'undefined' ? undefined : paginator,
    typeof itemsPerPage === 'undefined' ? undefined : itemsPerPage);

window.onload = main.init;