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

    $('body').delegate('.delete-btn', 'click', function (evt) {
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

    $('body').on('click', '#wikibutton', function(evt) {
      evt.preventDefault();
      var button = $(this);
      var url = button.attr('href');
      var name = ''
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

// Disable buttons
$(document).ready(function () {
    $('.disabled').on('click', function (event) {
        event.preventDefault();
    })
}); // Please review


// Wiki History
var toggleHistory = function () {
    $('#history').toggleClass('hidden');
    $('.wiki').toggleClass('history-visible');
}

$(document).ready(function () {
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

$(document).ready(function () {
    $('body').on('change', '.decision-select', function (event) {
        event.stopPropagation();
        var select = $(this);
        var url = select.data('href');
        var decision = select.val();

        var jqxhr = $.ajax({
            type: "POST",
            url: url,
            data: { decision : decision},
            dataType: "json",
            noCache: true
        }).done(function (msg) {
            var row = $(select).closest('tr');
            if (!msg.success) {
                $(row).addClass('highlight-error');
                alert(msg.error);
            }
            else {
                $(row).addClass('highlight-success')
                      .removeClass('highlight-error');

                setTimeout( function () {
                    $(row).addClass('fade')
                          .removeClass('highlight-success');
                }, 500);

                $(row).removeClass('fade');
            }
        }).fail(function (msg) {

        });
    });
});

// Handle error display in form registration
$(document).ready(function () {
    $('.form-error').on('focus', function () {
        $(this).removeClass('form-error');
    });

    $('.form-error').on('blur', function () {
        if (this.value) {
            $(this).siblings('.form-error-msg').addClass('hidden');
        } else {
            $(this).addClass('form-error');
            $(this).siblings('.form-error-msg').removeClass('hidden');
        }
    });
});

// Modal window
var openModal = function (iframe_url) {
    $('iframe').attr('src', iframe_url);
    $('.modal-bg').removeClass('hidden');
    $('body').addClass('stop_scroll');
};
var closeModal = function () {
    $('iframe').attr('src', '');
    $('.modal-bg').addClass('hidden');
    $('body').removeClass('stop_scroll');
};

// Flash Messages
$(document).ready( function () {

    var msg = $('.flashmessage');

    var show_flash = function () {
        $(msg).addClass('show');
    }

    var hide_flash = function () {
        $(msg).removeClass('show');
    }

    window.setTimeout(show_flash, 600);
    window.setTimeout(hide_flash, 3600);

    $(msg).on('mouseenter', show_flash);

    $(msg).on('mouseleave', function () {
        window.setTimeout(hide_flash, 600);
    });
});

$('#menucontainer').click(function(event){
    event.stopPropagation();
});

// Toggle button message
$(document).ready( function () {
    $('[data-toggle]').each( function () {
        var text = $(this).text();
        var comma = text.indexOf(',');
        var msg_1 = text.substring(0, comma);
        var msg_2 = text.substring(comma + 1, text.length);
        $(this).text(msg_1);
        $(this).click( function () {
            if ( $(this).text() == msg_1 ) {
                $(this).text(msg_2);
            } else {
                $(this).text(msg_1);
            }
        });
    });
});

// Popout
$(document).ready(function () {
    var popouts = $(".popout");
    var popoutButtons = $("[data-popout]");

    // Open popout
    $(popoutButtons).on('click', function (event) {
        event.stopPropagation();
        var similar = $(this).data('popout');
        var intendedTarget = $(this).closest('.popout-wrapper').find(".popout");
        if ( $(intendedTarget).hasClass('open') ) {
            $(intendedTarget).removeClass('open');    
        } else {
            // $(".popout." + similar).removeClass('open'); // to close similar
            $(".popout").removeClass('open');
            $(intendedTarget).addClass('open');
        }
    });

    // Close popout
    $('.popout').on('click', '.close', function () {
        $(this).closest('.popout').toggleClass('open');
    });
    $('.popout').on('click', function (event) {
        event.stopPropagation();
    });
    $('html').on('click', function() {
        $(popouts).removeClass('open');
    });    

    // Assesment
    $('.popout.assesment').each(function () {
        var method = $(this).find("select");
        var radios = $(this).find("input[type='radio']");
        var preview = $(this).closest('.popout-wrapper').find(".conclusion.select");
        var prevSecondClick;
        var currentClass = $(preview).data('initial');

        var updateSelect = function () {
            if ($(this).val()) {
                $(preview).children('.selected-value').removeClass('hidden').html( $(this).val() );
                $(preview).children('.fa').addClass('hidden');
            } else {
                $(preview).children('.selected-value').addClass('hidden').html( $(this).val() );
                $(preview).children('.fa').removeClass('hidden');
            }
        };

        var updateRadio = function (event) {
            event.stopPropagation();
            conclusionClass = $(this).data('class');
            // Match selected conclusion
            $(preview).removeClass(currentClass);
            if (currentClass != conclusionClass) {
                currentClass = conclusionClass;
                $(preview).addClass(currentClass);
            } else {
                currentClass = false;
                $(preview).removeClass(currentClass);
            }
            // Uncheck radio button
            var secondClick = $(this).attr('secondClick');
            if (secondClick == "false" || secondClick == undefined) {
                $(prevSecondClick).attr('secondClick', false);
                $(this).attr('secondClick', true);
            } else {
                $(this).attr('secondClick', false);
                this.checked = false;
            }
            prevSecondClick = this;
        };

        // Select
        //updateSelect(); // Initialize
        $(method).on('change', updateSelect);

        // Radios
        //updateRadio(); // Initialize
        $(radios).on('click', updateRadio);
    });

    // Size and unit
    $('.popout.size_unit').each(function () {
        var size = "#population_size";
        var unit = "#population_size_unit";
        var preview = $(this).closest('.popout-wrapper').find(".select");
        
        var update = function () {
            if ($(size).val() || $(unit).val()) {
                var concat = $(size).val() + " " + $(unit).val();
                $(preview).children('.selected-value').removeClass('hidden').html( concat );
                $(preview).children('.fa').addClass('hidden');
            } else {
                $(preview).children('.selected-value').addClass('hidden').html("");
                $(preview).children('.fa').removeClass('hidden');
            }
        };
        //update(); // Initialize
        $(this).on('change', size, update);
        $(this).on('change', unit, update);
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

$(function() {
     $('#filterform').on('submit', function(e) {
         window.location.hash = '';
         history.pushState('', document.title, window.location.pathname);
     });
 });

// jQuery Power Tip
$(document).ready(function() {
    $(".complex_datatable td, .complex_datatable th").each(function() {
        var type = $(this).data('tooltip');
        var place = $(this).data('tooltip-place');
        if (place == undefined) {
            place = "sw-alt";
        }

        switch (type) {
            case 'mouseover':
                var tooltip = $(this).attr('title');
                if (tooltip) {
                    tooltip = tooltip.replace(/\n/g, '<br />'); // Replace line break with <br />
                    $(this).data('powertip', tooltip);
                    $(this).powerTip({
                        placement: place,
                        smartPlacement: true,
                        mouseOnToPopup: true,
                        offset: 0,
                    });
                }
                $(this).removeAttr('title');
                break;
                
            case 'html':
                var tooltip = $(this).find('.tooltip-html').html();
                $(this).data('powertip', tooltip);
                $(this).powerTip({
                    placement: place,
                    mouseOnToPopup: true,
                    offset: 0,
                });
                break;

            default:
                var tooltip = $(this).attr('title');
                if (tooltip) {
                    tooltip = tooltip.replace(/\n/g, '<br />'); // Replace line break with <br />
                    $(this).data('powertip', tooltip);
                    $(this).powerTip({
                        placement: place,
                        smartPlacement: true,
                        offset: 0,
                    });
                    $(this).removeAttr('title');
                }
        }
    });
});