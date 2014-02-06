$(function () {

    if($('#filterform').length == 1) {

        var group = $('#group');
        group.remoteChained('#period', group.data('href'));

        var subject = $('#subject');
        subject.remoteChained('#period, #group', subject.data('href'));

        var region = $('#region');
        region.remoteChained('#period, #group, #subject', region.data('href'));

        if(group.find('option:selected').val() == '') {
            subject.prop('disabled', true);
        }

        if(subject.find('option:selected').val() == '') {
            region.prop('disabled', true);
        }

    }

    if($('#report-filterform').length == 1) {

        var region = $('#region');
        region.remoteChained('#period, #country', region.data('href'));

        var group = $('#group');
        group.remoteChained('#period', group.data('href'));
    }

    if($('#progress-filterform').length == 1) {

        var group = $('#group');
        var conclusion = $('#conclusion');

        group.remoteChained('#period', group.data('href'));
    }
});

$(function() {
    $('body').on('click', '.comments-btn', function(evt) {
      evt.preventDefault();
      var link = $(this);
      var url = link.attr('href');
      var title = "Comments";
      var params = 'height=600,width=600,screenX=300,screenY=100,scrollbars=1';
      var popup = window.open(url, title, params);
      popup.focus();
    });

    $('.close-popup').on('click', function (evt) {
      evt.preventDefault();
      window.close();
    });

    $('body').on('click', '.delete-btn', function (evt) {
        evt.preventDefault();
        var url = $(this).attr('href');
        var request = $.ajax({
            type: "GET",
            url: url,
            dataType: "script"
        }).done(function (msg) { location.reload(); });
    });

    $('body').on('click', '.popup-btn', function(evt) {
      evt.preventDefault();
      var link = $(this);
      var url = link.attr('href');
      var title = link.data('title');
      var params = 'height=600,width=600,screenX=300,screenY=100,scrollbars=1';
      var popup = window.open(url, title, params);
      popup.focus();
    });

});

$(function() {
    $('body').on('click', '#wikibutton', function(evt) {
        evt.preventDefault();
        var btn = $(this);
        var url = btn.attr('url');
        var title = 'Data Sheet Info';
        var params = 'scrollbars=1, resizable=1, height=600, width=600';
        var popup = window.open(url, title, params);
        popup.focus();
    });
});

$(function() {
    $('body').on('click', '.button_text', function(evt) {
        evt.preventDefault();
        var clicked_button = $(this);
        var comment = clicked_button.parent().parent();
        var url = clicked_button.attr('href');
        var url_parts = url.split("?");
        var request = $.ajax({
            type: "GET",
            url: url,
            dataType: "script",
            success: function(result) {
                switch (comment.attr('class')) {
                    case 'cmnt-owned':
                        comment.attr('class', 'cmnt-deleted');
                        comment.find('.cmnt-type').html('Deleted');
                        clicked_button.html('Undo');
                        clicked_button.attr('href', url_parts[0] + '?comment_id=' + comment.attr('id') + '&toggle=del');
                        comment.find('#edit-btn').hide()
                        break;
                    case 'cmnt-deleted':
                        comment.attr('class', 'cmnt-owned');
                        comment.find('.cmnt-type').html('Your comment');
                        clicked_button.html('Delete');
                        clicked_button.attr('href', url_parts[0] + '?comment_id=' + comment.attr('id') + '&toggle=del');
                        comment.find('#edit-btn').show()
                        break;
                    case 'cmnt-notread':
                        comment.attr('class', 'cmnt-read');
                        comment.find('.cmnt-type').html('Read');
                        clicked_button.html('Mark as not read');
                        clicked_button.attr('href', url_parts[0] + '?comment_id=' + comment.attr('id') + '&toggle=read');
                        break;
                    case 'cmnt-read':
                        comment.attr('class', 'cmnt-notread');
                        comment.find('.cmnt-type').html('Not read');
                        clicked_button.html('Mark as read');
                        clicked_button.attr('href', url_parts[0] + '?comment_id=' + comment.attr('id') + '&toggle=read');
                        break;
                }
            }
        });
    });

    $('body').on('click', '#edit-btn', function(evt) {
        evt.preventDefault()
        window.location = $(this).attr('href');
    });
});

$(function () {


  $('#history').on('click', 'li', function () {
    event.stopPropagation();
    $(this).addClass('selected')
    .siblings('.selected').removeClass('selected');
  });

  $('html').click( function () {
    $('#history .selected').removeClass('selected');
  });
});