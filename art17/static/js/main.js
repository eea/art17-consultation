// TODO: split this file

$(function () {

    if($('#filterform').length == 1) {

        var group = $('#group');
        group.remoteChained('#period', group.data('href'));

        var country = $('#country');
        country.remoteChained('#period', country.data('href'));

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

        var country = $('#country');
        country.remoteChained('#period', country.data('href'));

        if(country.find('option:selected').val() == '') {
            region.prop('disabled', true);
        }

    }

    if($('#progress-filterform').length == 1) {

        var group = $('#group');
        var conclusion = $('#conclusion');
        var assessor = $('#assessor');

        group.remoteChained('#period', group.data('href'));
        assessor.remoteChained('#period, #group', assessor.data('href'));
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

    $('body').on('click', '#show-map', function(evt) {
        var url = $(this).data('url');
        if (url != "") {
            title = "Map";
            var params = "left=400,top=100,width=800,height=650," +
                            "toolbar=0,resizable=0,scrollbars=0";
            window.open(url, title, params).focus();
        }
    });
});

$(function() {
    $('.comment-section').on('click', '.btn-text', function(evt) {
        evt.preventDefault();
        var clicked_button = $(this);
        var comment = clicked_button.parent().parent();
        var url = clicked_button.attr('href');
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
                        comment.find('.edit-btn').hide()
                        break;
                    case 'cmnt-deleted':
                        comment.attr('class', 'cmnt-owned');
                        comment.find('.cmnt-type').html('Your comment');
                        clicked_button.html('Delete');
                        comment.find('.edit-btn').show()
                        comment.find('.cancel-edit').hide()
                        break;
                    case 'cmnt-notread':
                        comment.attr('class', 'cmnt-read');
                        comment.find('.cmnt-type').html('Read');
                        clicked_button.html('Mark as unread');
                        break;
                    case 'cmnt-read':
                        comment.attr('class', 'cmnt-notread');
                        comment.find('.cmnt-type').html('Unread');
                        clicked_button.html('Mark as read');
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

// Confirm permanently delete
$(document).ready(function () {
    $('.perm-del').on('click', function (evt) {
        evt.preventDefault();
        var confirm_del = confirm("Are you sure you want to permanently delete this record?");
        if (confirm_del) {
            var href = $(this).attr('href');
            window.location = href;
        }
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
        var previewValue = $(preview).data('value');
        var prevSecondClick = $(radios).filter(':checked');
        var currentClass = $(preview).data('initial');

        var updateSelect = function () {
            if ($(this).val()) {
                $(preview).children('.selected-value').removeClass('hidden').html( $(this).val() );
            } else {
                $(preview).children('.selected-value').addClass('hidden').html( $(this).val() );
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
            // update value
            if (previewValue == 'radio') {
                var checked = $(radios).filter(':checked');
                if ($(checked).val())
                    $(preview).children('.selected-value').removeClass('hidden').html($(checked).val());
                else
                    $(preview).children('.selected-value').addClass('hidden').html('');
            }
            prevSecondClick = this;
        };

        // Value
        if (previewValue == 'method') {
            $(method).on('change', updateSelect);
        }

        // Radios
        $(radios).on('click', updateRadio);
    });

    // Size and unit
    $('.popout.size_unit').each(function () {
        var complementary_favourable_range_q = "#complementary_favourable_range_q";
        var complementary_favourable_range_size = "#complementary_favourable_range_size";
        var complementary_favourable_population_size = "#complementary_favourable_population_size";
        var complementary_favourable_population_q = "#complementary_favourable_population_q";
        var complementary_favourable_area_size = "#complementary_favourable_area_size";
        var complementary_favourable_area_q = "#complementary_favourable_area_q";
        var preview = $(this).closest('.popout-wrapper').find(".select");
        var update = function (size, unit) {
            if ($(size).val() || $(unit).val()) {
                var concat = $(unit).val() +" " + $(size).val() + " ";
                $(preview).children('.selected-value').removeClass('hidden').html( concat );
                $(preview).children('.fa').addClass('hidden');
            } else {
                $(preview).children('.selected-value').addClass('hidden').html("");
                $(preview).children('.fa').removeClass('hidden');
            }
        };
        $(this).on('change', complementary_favourable_range_size,
                             function(){update(complementary_favourable_range_size, complementary_favourable_range_q);});
        $(this).on('change', complementary_favourable_range_q,
                             function(){update(complementary_favourable_range_size, complementary_favourable_range_q);});
        $(this).on('change', complementary_favourable_population_size,
                             function(){update(complementary_favourable_population_size, complementary_favourable_population_q);});
        $(this).on('change', complementary_favourable_population_q,
                             function(){update(complementary_favourable_population_size, complementary_favourable_population_q);});
        $(this).on('change', complementary_favourable_area_size,
                             function(){update(complementary_favourable_area_size, complementary_favourable_area_q);});
        $(this).on('change', complementary_favourable_area_q,
                             function(){update(complementary_favourable_area_size, complementary_favourable_area_q);});
    });

    // Size and unit
    $('.popout.size_unit.min_max_best').each(function () {
        var hab_condition_good_min = "#hab_condition_good_min";
        var hab_condition_good_max = "#hab_condition_good_max";
        var hab_condition_good_best = "#hab_condition_good_best";
        var hab_condition_notgood_min = "#hab_condition_notgood_min";
        var hab_condition_notgood_max = "#hab_condition_notgood_max";
        var hab_condition_notgood_best = "#hab_condition_notgood_best";
        var hab_condition_unknown_min = "#hab_condition_unknown_min";
        var hab_condition_unknown_max = "#hab_condition_unknown_max";
        var hab_condition_unknown_best = "#hab_condition_unknown_best";
        var preview = $(this).closest('.popout-wrapper').find(".select");
        var update = function (min, max, best) {
            if ($(min).val() || $(max).val() || $(best).val()) {
                var concat =  $(min).val() + " | " + $(max).val() + " | " + $(best).val() ;
                $(preview).children('.selected-value').removeClass('hidden').html( concat );
                $(preview).children('.fa').addClass('hidden');
            } else {
                $(preview).children('.selected-value').addClass('hidden').html("");
                $(preview).children('.fa').removeClass('hidden');
            }
        };
        $(this).on('change', hab_condition_good_min,
                                function(){update(hab_condition_good_min, hab_condition_good_max, hab_condition_good_best);});
        $(this).on('change', hab_condition_good_max,
                                function(){update(hab_condition_good_min, hab_condition_good_max, hab_condition_good_best);});
        $(this).on('change', hab_condition_good_best,
                                function(){update(hab_condition_good_min, hab_condition_good_max, hab_condition_good_best);});

        $(this).on('change', hab_condition_notgood_min,
                                function(){update(hab_condition_notgood_min, hab_condition_notgood_max, hab_condition_notgood_best);});
        $(this).on('change', hab_condition_notgood_max,
                                function(){update(hab_condition_notgood_min, hab_condition_notgood_max, hab_condition_notgood_best);});
        $(this).on('change', hab_condition_notgood_best,
                                function(){update(hab_condition_notgood_min, hab_condition_notgood_max, hab_condition_notgood_best);});

        $(this).on('change', hab_condition_unknown_min,
                                function(){update(hab_condition_unknown_min, hab_condition_unknown_max, hab_condition_unknown_best);});
        $(this).on('change', hab_condition_unknown_max,
                                function(){update(hab_condition_unknown_min, hab_condition_unknown_max, hab_condition_unknown_best);});
        $(this).on('change', hab_condition_unknown_best,
                                function(){update(hab_condition_unknown_min, hab_condition_unknown_max, hab_condition_unknown_best);});
    });
    var inputs = document.querySelectorAll('.extend-input input');
    if (inputs) {
      for(var i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('input', resizeInput);
        resizeInput.call(inputs[i]);
      }
      function resizeInput() {
        this.style.width = (this.value.length + 2) + "ch";
      }
    }
});


// Filter form
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
                var br = $(this).find('.br').text();
                if (br != undefined) {
                    br = br.replace(/\n/g, '<br />'); // Replace line break with <br />
                }
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

// Dataset compare (progress)
$(document).ready(function () {
    $('.load-comparison').on('click', function (evt) {
        evt.preventDefault();

        var container = $(this).closest('.popout');
        var url = $(this).data('url');

        $(this).after("<i class='fa fa-spinner fa-spin'></i>");
        $.ajax({
            type: "GET",
            url: url,
            dataType: "html"
        }).done(function (msg) { container.html(msg); });
    });
});
