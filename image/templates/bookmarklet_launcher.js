(function() {
    if (window.image_service_bookmarklet != undefined){
        image_service_bookmarklet();
    }
    else {
        let bookmarkletScript_url = 'https://mysite.com:8000/static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 99999999999999999);
        let bookmarkletScript = document.createElement('script');
        document.body.appendChild(bookmarkletScript).src=bookmarkletScript_url;
    }
})();