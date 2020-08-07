// let xhr = new XMLHttpRequest();

// let data = 'action=like';

// console.log(data)

// xhr.open('POST', request_url);
// xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
// xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
// xhr.send(JSON.stringify({
//     action: 'like'
// }));

// xhr.onload = function() {
//     let responseObj = xhr.response;
//     alert(responseObj);
// }

$('a.like').click(function(e) {
    e.preventDefault();
    $.post(request_url, {
        id: $(this).data('id'),
        action: $(this).data('action')
    },
    function(data){
        if (data['status'] == 'ok'){
            let btn = $('a.like');
            let action = btn.data('action');

            // toggle data-action
            btn.data('action', (action == 'like' ? 'unlike' : 'like'))
            // toggle link text
            btn.text(action == 'like' ? 'Unlike' : 'Like')
            // toggle classes
            btn.removeClass(action + '-btn');
            btn.addClass((action == 'like' ? 'unlike' : 'like') + '-btn');


            // update total likes
            let span = $('span.like-view');
            let likes = parseInt(span.text());
            span.text((action == 'like' ? likes + 1 : likes - 1) + ' likes');
        }
    });
})