$('a.like').click(function(e){
    e.preventDefault();
    $.post(request_url, {
        id: $(this).data('id'),
        action: $(this).data('action')
    }, 
    function (data) {
        if (data['status'] == 'ok') {
            let btn = $('a.like');
            let span = $('span.followers-count')
            let followers = parseInt(span.text())
            let action = btn.data('action');

            if (action == 'follow'){
                btn.removeClass('like-btn');
                btn.addClass('unlike-btn');
                btn.text('Unfollow');
                btn.data('action', 'unfollow');
                ++followers;
            }
            else {
                btn.removeClass('unlike-btn');
                btn.addClass('like-btn');
                btn.text('Follow');
                btn.data('action', 'follow');
                --followers;
            }
            span.text(followers + ' follower' + (followers == 1 ? '' : 's'));
        }
    })
});