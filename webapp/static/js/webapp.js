/*
* KALUKALU WebAPP
*/

WebApp = {
    server: null,
    call: function(method, params, callback) {
        """
            Methods: discover, search, playsong, cache.
        """
        url = WebApp.server + method;
        $.get(url, params, callback);
    }
    discover: function () {
        this.call('discover', function(data) {
            console.log(data);
        });
    }
}