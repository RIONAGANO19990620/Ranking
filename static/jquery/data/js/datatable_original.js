$(document).ready(function () {
    var table = $('#my-table').DataTable({
        // 横スクロールバーを有効にする (scrollXはtrueかfalseで有効無効を切り替えます)
        scrollX: false,
        // 縦スクロールバーを有効にする (scrollYは200, "200px"など「最大の高さ」を指定します)
        scrollY: 500,
        // 列設定
        "bAutoWidth": false,
        paging: false,
        "language": {
        "search": "",            // Removes the 'Search' field label
        "searchPlaceholder": "Search"   // Placeholder for the search box
    }
    });
});