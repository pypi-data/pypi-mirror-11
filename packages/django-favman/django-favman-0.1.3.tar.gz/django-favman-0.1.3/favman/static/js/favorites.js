$(function() {
    $(".fav-icon").on('click', function() {
        var form = $(this).find('form');
        var elt = $(this);
        $('.favman-message').remove();
        $.ajax({
            type: "POST",
            url: form.attr('action'),
            dataType: 'json',
            data: form.serialize(),
            success: function(data) {
                if (data.success) {
                    elt.removeClass('in-fav').removeClass('out-fav').addClass(data.status);
                } else {
                    var html_msg = '<div class="favman-message">'+data.message+'</div>';
                    elt.append(html_msg);
                    elt.find('.favman-message').click(function(event) {
                        if ($(event.target).is('a')) {
                            window.location = $(event.target).attr('href');
                        } else {
                            $(this).remove();
                        }
                        return false;
                    })
                }
            }
        });
        return false;
    })
})