// TODO: split this file

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
      var name = "Comments";
      var params = 'height=600,width=600,screenX=300,screenY=100,scrollbars=1';
      var popup = window.open(url, name, params);
      popup.focus();
    });

});

$(function() {
    $('.comment-section').on('click', '.btn-text', function(evt) {
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
                        clicked_button.html('Undelete');
                        clicked_button.attr('href', url_parts[0] + '?comment_id=' + comment.attr('id') + '&toggle=del');
                        comment.find('.edit-btn').hide()
                        break;
                    case 'cmnt-deleted':
                        comment.attr('class', 'cmnt-owned');
                        comment.find('.cmnt-type').html('Your comment');
                        clicked_button.html('Delete');
                        clicked_button.attr('href', url_parts[0] + '?comment_id=' + comment.attr('id') + '&toggle=del');
                        comment.find('.edit-btn').show()
                        comment.find('.cancel-edit').hide()
                        break;
                    case 'cmnt-notread':
                        comment.attr('class', 'cmnt-read');
                        comment.find('.cmnt-type').html('Read');
                        clicked_button.html('Mark as unread');
                        clicked_button.attr('href', url_parts[0] + '?comment_id=' + comment.attr('id') + '&toggle=read');
                        break;
                    case 'cmnt-read':
                        comment.attr('class', 'cmnt-notread');
                        comment.find('.cmnt-type').html('Unread');
                        clicked_button.html('Mark as read');
                        clicked_button.attr('href', url_parts[0] + '?comment_id=' + comment.attr('id') + '&toggle=read');
                        break;
                }
            }
        });
    });

    $('body').on('click', '.edit-btn', function(evt) {
        if (! $(this).hasClass('disabled')) {
            window.location = $(this).attr('href');
        }
    });

});

$(function () {
  $('#history').on('click', 'li:not(.active)', function (event) {
    event.stopPropagation();
    $(this).addClass('selected')
    .siblings('.selected').removeClass('selected');
    revision_id = $(this).attr('id');
    url = $(this).attr('href');
    var request = $.ajax({
        type: "GET",
        url: url,
        dataType: "html",
        success: function(result) {
            $('#active-wiki').hide()
            $('#preview-wiki').html(result).show()
        }
    });
  });

  $('html').click( function () {
    $('#history .selected').removeClass('selected');
    $('#active-wiki').show()
    $('#preview-wiki').hide()
  });
});

$(function () {
    $('body').on('change', '.decision-select', function (event) {
        event.stopPropagation();
        var select = $(this);
        var url = select.data('href');
        var decision = select.val();

        var jqxhr = $.ajax({
            type: "POST",
            url: url,
            data: { decision : decision},
            dataType: "json"
        }).done(function (msg) {
            if (!msg.success) {
                alert(msg.error);
            }
        }).fail(function (msg) {

        });
    });
});

// Handle error display in form registration
$(function () {
    $('.form-error').delegate('', 'focus', function () {
        $(this).removeClass('form-error');
    });

    $('.form-error').delegate('', 'blur', function () {
        if (this.value) {
            $(this).siblings('.form-error-msg').addClass('hidden');
        } else {
            $(this).addClass('form-error');
        }
    });
});

// Modal window
var openModal = function (iframe_url) {
    $('iframe').attr('src', iframe_url)
    $('.modal-bg').removeClass('hidden');
    $('body').addClass('stop_scroll');
};

var closeModal = function () {
    $('iframe').attr('src', '');
    $('.modal-bg').addClass('hidden');
    $('body').removeClass('stop_scroll');
};

// Flash Messages
$(function () {

    var msg = $('.message');

    var show_flash = function () {
        $(msg).addClass('show');
    }

    var hide_flash = function () {
        $(msg).removeClass('show');
    }

    window.setTimeout(show_flash, 600);
    window.setTimeout(hide_flash, 3600);

    $(msg).on('mouseenter', show_flash)//function () {
//        window.clearTimeout(hide_flash);
  //  });

    $(msg).on('mouseleave', function () {
        window.setTimeout(hide_flash, 600);
    });
});

// Table column hover
/*$(function () {
    $(".complex_datatable").on('mouseenter mouseleave', "td", function (event) {
        event.stopPropagation();
        index = this.cellIndex;
        if (index) {
            $(this).parent().siblings().each ( function () {
                $(this.cells[index]).toggleClass("hover");
            });
        }
    });
});*/
