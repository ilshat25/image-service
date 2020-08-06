
function image_service_bookmarklet() {
    let site_url = 'https://mysite.com:8000/';
    let static_url = site_url + 'static/'
    let min_height = 100
    let min_width = 100
    
    // load css
    let css = document.createElement('link');
    css.setAttribute('type', 'text/css');
    css.setAttribute('rel', 'stylesheet')
    css.setAttribute('href', static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*999999999999));
    document.head.appendChild(css);

    // load HTML
    box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>'

    document.body.innerHTML += box_html

    // close event
    document.getElementById('close').onclick = function() {
        document.getElementById('bookmarklet').remove()
    }

    // find images and display them
    document.querySelectorAll('img[src$=".jpg"]').forEach(function(image){
        if (image.width >= min_width && image.height >= min_height) {
            image_url = image.src;
            document.querySelector('#bookmarklet .images').innerHTML += '<a href="#"><img src="' + image_url + '"></a>';
        }
    });

    // when an image is selected open URL with it
    document.querySelectorAll('#bookmarklet .images img').forEach(function(e) {
        e.onclick = function() {

            selected_image = e.src;
            image_title = document.title;
            // hide bookmarklet
            document.getElementById("bookmarklet").remove();
            console.log(selected_image);
            // open new window to submit the image
            window.open(site_url + 
                'images/add/?url=' + 
                encodeURIComponent(selected_image) +
                "&title=" + 
                encodeURIComponent(image_title),
                '_blank');
        }
    });
}

image_service_bookmarklet();