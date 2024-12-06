$(document).ready(function () {
    if (window.jQuery) {
        if ($.fn.DataTable) {
            $('.dts').DataTable({
                language: {
                    url: '/static/libs/datatables/spanish.json'
                }
            });
        }
    }
});